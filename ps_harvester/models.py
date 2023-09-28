from django.db import models


class HarvestStatus(models.Model):
    # Names:
    # 1) COMPLETE
    # 2) INCOMPLETE
    # 3) PENDING REVIEW
    # 3) ERROR
    status_id = models.AutoField(primary_key=True)
    status_name = models.CharField(max_length=256)

    def __str__(self) -> str:
        return self.status_name


class HarvestProcess(models.Model):
    process_id = models.BigAutoField(primary_key=True)
    status = models.ForeignKey(HarvestStatus, on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class HarvestFile(models.Model):
    file_id = models.BigAutoField(primary_key=True)
    filepath = models.FileField(editable=False)
    process = models.ForeignKey(HarvestProcess, on_delete=models.CASCADE)
    upload_timestamp = models.DateTimeField(auto_now_add=True)


class HarvestWebDirect(models.Model):
    web_id = models.BigAutoField(primary_key=True)
    web_address = models.URLField()
    process = models.ForeignKey(HarvestProcess, on_delete=models.CASCADE)
    collected_timestamp = models.DateTimeField(auto_now_add=True)


class HarvestEntrySpeech(models.Model):
    entry_id = models.BigAutoField(primary_key=True)

    # The identifier for each statements entry on admin
    speech_id = models.BigIntegerField(editable=False)
    process = models.ForeignKey(HarvestProcess, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
