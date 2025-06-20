from django.db import models


class MarkAPIUser(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField()
    last_synced_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'mark_api_users'
        managed = False  # Important: table is created manually


class CceEntry(models.Model):
    slno = models.DecimalField(
        max_digits=12, decimal_places=0, primary_key=True)
    admission = models.CharField(max_length=20, null=True, blank=True)
    class_field = models.CharField(
        max_length=20, null=True, blank=True, db_column='class')
    division = models.CharField(max_length=20, null=True, blank=True)
    subject = models.CharField(max_length=30, null=True, blank=True)
    assessmentitem = models.CharField(max_length=30, null=True, blank=True)
    term = models.CharField(max_length=20, null=True, blank=True)
    part = models.CharField(max_length=20, null=True, blank=True)
    mark = models.DecimalField(
        max_digits=12, decimal_places=3, null=True, blank=True)
    sortorder = models.IntegerField(null=True, blank=True)
    maxmark = models.DecimalField(
        max_digits=12, decimal_places=3, null=True, blank=True)
    grade = models.CharField(max_length=5, null=True, blank=True)
    last_updated = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'cce_entry'
        managed = False
        verbose_name = 'CCE Entry'
        verbose_name_plural = 'CCE Entries'
