from django.db import models
from django.utils import timezone


class Release(models.Model):
    release_id = models.SmallIntegerField(primary_key=True)
    name = models.TextField()

    class Meta:
        db_table = "release"
        managed = False
        app_label = "pvsadmin"


class StateType(models.Model):
    statetype_id = models.CharField(max_length=1, primary_key=True)
    name = models.TextField()

    class Meta:
        db_table = "statetype"
        managed = False
        app_label = "pvsadmin"


class State(models.Model):
    state_id = models.CharField(max_length=2, primary_key=True)
    statetype = models.ForeignKey(
        StateType, on_delete=models.RESTRICT, db_column="statetype_id"
    )
    statecode = models.SmallIntegerField()
    name = models.TextField(default="")
    modified = models.DateTimeField()

    class Meta:
        db_table = "state"
        managed = False
        app_label = "pvsadmin"


class CandidateStatus(models.Model):
    candidatestatus_id = models.SmallAutoField(primary_key=True)
    name = models.TextField()

    class Meta:
        db_table = "candidatestatus"
        managed = False
        app_label = "pvsadmin"


class CandidateTitle(models.Model):
    candidatetitle_id = models.SmallAutoField(primary_key=True)
    title = models.TextField()

    class Meta:
        db_table = "candidatetitle"
        managed = False
        app_label = "pvsadmin"


class CandidatePreferredName(models.Model):
    candidatepreferredname_id = models.CharField(max_length=1, primary_key=True)
    name = models.TextField()

    class Meta:
        db_table = "candidatepreferredname"
        managed = False
        app_label = "pvsadmin"


class Candidate(models.Model):
    candidate_id = models.AutoField(primary_key=True)
    state = models.ForeignKey(State, on_delete=models.RESTRICT, default="NA")
    release = models.ForeignKey(
        Release, on_delete=models.RESTRICT, db_column="release_id"
    )
    candidatestatus = models.ForeignKey(
        CandidateStatus, on_delete=models.RESTRICT, default=1
    )
    candidatetitle = models.ForeignKey(
        CandidateTitle, on_delete=models.RESTRICT, default=0
    )
    firstname = models.TextField(default="")
    middlename = models.TextField(default="")
    lastname = models.TextField(default="")
    nickname = models.TextField(default="")
    suffix = models.TextField(default="")
    candidatepreferredname = models.ForeignKey(
        CandidatePreferredName, on_delete=models.RESTRICT, default="F"
    )
    created = models.DateTimeField()
    modified = models.DateTimeField()

    class Meta:
        db_table = "candidate"
        managed = False
        app_label = "pvsadmin"


class SpeechType(models.Model):
    speechtype_id = models.SmallAutoField(primary_key=True)
    name = models.TextField(default="")

    class Meta:
        db_table = "speechtype"
        managed = False
        app_label = "pvsadmin"


class Speech(models.Model):
    speech_id = models.AutoField(primary_key=True)
    speechtype = models.ForeignKey(
        SpeechType, on_delete=models.RESTRICT, db_column="speechtype_id"
    )
    title = models.TextField(default="")
    speechdate = models.DateField(null=True, default=timezone.now, blank=True)
    location = models.TextField(default="", blank=True)
    speechtext = models.TextField()
    url = models.URLField(max_length=2000, default="", blank=True)
    release = models.ForeignKey(
        Release, on_delete=models.RESTRICT, db_column="release_id"
    )
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    # Many-to-Many relationship to Candidate through speech_candidate table
    candidates = models.ManyToManyField(Candidate, through="SpeechCandidate")

    class Meta:
        db_table = "speech"
        managed = False
        app_label = "pvsadmin"


class SpeechCandidate(models.Model):
    speech_candidate_id = models.AutoField(primary_key=True)
    speech = models.ForeignKey(Speech, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "speech_candidate"
        managed = False
        app_label = "pvsadmin"


class Category(models.Model):
    category_id = models.SmallAutoField(primary_key=True)
    name = models.TextField()
    release_id = models.SmallIntegerField(null=True)
    description = models.TextField(null=True)
    rank = models.SmallIntegerField(null=True)
    key = models.BooleanField(default=False)

    class Meta:
        db_table = "category"
        managed = False
        app_label = "pvsadmin"


class Tag(models.Model):
    tag_id = models.AutoField(primary_key=True)
    name = models.TextField(blank=False)
    deleted = models.BooleanField(default=False)
    modified = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = "tag"
        managed = False
        app_label = "pvsadmin"


class SpeechCategory(models.Model):
    speech_category_id = models.AutoField(primary_key=True)
    speech = models.ForeignKey(Speech, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)

    class Meta:
        db_table = "speech_category"
        managed = False
        app_label = "pvsadmin"


class SpeechTag(models.Model):
    speech_tag_id = models.AutoField(primary_key=True)
    speech = models.ForeignKey(Speech, on_delete=models.CASCADE, null=True)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = "speech_tag"
        managed = False
        app_label = "pvsadmin"
