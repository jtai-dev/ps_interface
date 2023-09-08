import random
from ps_harvester.models import (
    HarvestStatus,
    HarvestProcess,
    HarvestFile,
    HarvestEntrySpeech,
    HarvestWebDirect)
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ps_interface.settings')
django.setup()


def populate(number_of_process=2, max_entries=5):
    statuses = HarvestStatus.objects.all()
    # trigger = random.choice(HarvestTrigger.objects.all())

    for _ in range(number_of_process):
        status = random.choice(statuses)
        process = HarvestProcess.objects.create(status=status)

        for _ in range(random.randint(1, max_entries)):
            speech_id = random.randint(1000000, 1500000)

            HarvestEntrySpeech.objects.create(process=process,
                                              speech_id=speech_id)

        random.choice((HarvestFile, HarvestWebDirect)
                      ).objects.create(process=process)


if __name__ == '__main__':
    populate()
