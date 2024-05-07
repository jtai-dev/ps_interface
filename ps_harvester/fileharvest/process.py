# Built-ins
import json
import traceback
from datetime import datetime
from collections import defaultdict

# External packages & libraries
import psycopg
from psycopg.errors import DatabaseError, InterfaceError
from decouple import config

from ps_harvester.fileharvest.json_model import HarvestArticles


class HarvestError(Exception):

    def __init__(self, message, parent=None, *args: object) -> None:
        super().__init__(message, *args)
        self._parent = parent

    @property
    def traceback(self):
        return "".join(traceback.format_exception(self._parent))


def insert_into_speech(cursor, *values):

    try:
        cursor.execute(
            "INSERT INTO speech (speechtype_id, title, speechdate, location, speechtext, url, created)"
            "VALUES (%s, %s, %s, %s, %s, %s, %s)"
            "RETURNING speech_id",
            values,
        ),

    except (DatabaseError, InterfaceError) as e:
        raise HarvestError("Failed to create speech entry.", parent=e)

    return cursor.fetchone()


def insert_into_speech_candidate(cursor, *values):

    try:
        cursor.execute(
            "INSERT INTO speech_candidate (speech_id, candidate_id, created)"
            "VALUES (%s, %s, %s)"
            "RETURNING speech_candidate_id",
            values,
        )

    except (DatabaseError, InterfaceError) as e:
        raise HarvestError("Failed to link candidates with speech entry.", parent=e)

    return cursor.fetchone()


def establish_connection():

    connection_info = {
        "host": config("VSDB_HOST", default="localhost"),
        "port": config("VSDB_PORT", default=5432, cast=int),
        "dbname": config("VSDB_NAME", default="postgres"),
        "user": config("VSDB_USER", default=""),
        "password": config("VSDB_PASSWORD", default=""),
    }
    try:
        # This would be the connection to the PVS database
        connection = psycopg.connect(**connection_info)
        return connection

    except (DatabaseError, InterfaceError) as e:
        raise HarvestError("Failed to establish database connection.", parent=e)


def process_json_strings(json_strings: list[str]):

    contents = []
    try:
        for js in json_strings:
            content = json.loads(js)
            if isinstance(content, list):
                contents += content

    except Exception as e:
        raise HarvestError("Failed to process JSON file.", parent=e)

    return contents


def main(file_contents):

    harvest_json = HarvestArticles(process_json_strings(file_contents))

    connection = establish_connection()

    cursor = connection.cursor()

    speech_to_candidate = defaultdict(set)

    for harvest in harvest_json.all:
        # speech_id is not shared at the moment
        speech_id = insert_into_speech(
            cursor,
            harvest.speechtype_id,
            harvest.title,
            harvest.speechdate,
            harvest.location,
            harvest.speechtext if harvest.speechtext else "",
            harvest.url,
            str(datetime.now()),
        )[0]

        speech_to_candidate[speech_id].add(harvest)

    speech_candidate_to_harvest = defaultdict(dict)

    for speech_id, harvests in speech_to_candidate.items():
        for harvest in harvests:
            for candidate_id in harvest.candidate_ids:

                speech_candidate_id = insert_into_speech_candidate(
                    cursor, speech_id, candidate_id, str(datetime.now())
                )[0]

                speech_candidate_to_harvest[speech_candidate_id][
                    "candidate_id"
                ] = candidate_id
                speech_candidate_to_harvest[speech_candidate_id]["review"] = harvest.review
                speech_candidate_to_harvest[speech_candidate_id][
                    "review_message"
                ] = harvest.review_message

    connection.commit()

    cursor.close()
    connection.close()

    return speech_candidate_to_harvest
