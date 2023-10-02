
import random

import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ps_interface.settings')
django.setup()

from ps_harvester.models import (
    HarvestStatus,
    HarvestProcess,
    HarvestFile,
    HarvestEntrySpeech,
    HarvestWebDirect)

review_messages = ('Candidate may not be matched correctly.',
                   'The speech entry does not contain any text')


def populate(number_of_process=2, max_entries=5):

    for _ in range(number_of_process):
        process = HarvestProcess.objects.create()
        reviews = []

        for _ in range(random.randint(1, max_entries)):
            speech_id = random.randint(1000000, 1500000)
            review = random.choice((True, False))

            if review:
                HarvestEntrySpeech.objects.create(process=process,
                                                  speech_id=speech_id,
                                                  review=review,
                                                  review_message=random.choice(review_messages))

            else:
                HarvestEntrySpeech.objects.create(process=process,
                                                  speech_id=speech_id,)
                
            reviews.append(review)
        
        status = random.choice(HarvestStatus.objects.filter(status_name__in=['COMPLETE', 'ERROR']))

        if any(reviews):
            process.status = HarvestStatus.objects.get(status_name='PENDING REVIEW')
        else:
            process.status = status

        process.save()

        source_type = random.choice((HarvestFile, HarvestWebDirect))

        if source_type == HarvestFile:
            source_type.objects.create(
                process=process, filepath='/Users/username/file.json')
        else:
            source_type.objects.create(
                process=process, web_address='https://votesmart.org')


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(prog='ps_interface_populate')
    parser.add_argument('-n', '--number_of_processes', type=int, default=2)
    parser.add_argument('-e', '--number_of_entries', type=int, default=5)

    args = parser.parse_args()

    populate(args.number_of_processes, args.number_of_entries)
