from django.db import models

from edc_appointment.models import Appointment
from edc_base.model_mixins.base_uuid_model import BaseUuidModel
from edc_constants.choices import YES_NO
from edc_base.utils import get_utcnow


class SubjectVisit(BaseUuidModel):

    appointment = models.ForeignKey(Appointment, null=True)

    subject_identifier = models.CharField(max_length=25)

    report_datetime = models.DateTimeField(default=get_utcnow)


class SubjectReferral(BaseUuidModel):

    subject_visit = models.OneToOneField(SubjectVisit)

    scheduled_appt_date = models.DateField(null=True)


class PimaCd4(BaseUuidModel):

    subject_visit = models.OneToOneField(SubjectVisit)

    result_value = models.IntegerField(null=True)

    result_datetime = models.DateTimeField(null=True)


class HivCareAdherence(BaseUuidModel):

    subject_visit = models.OneToOneField(SubjectVisit)

    next_appointment_date = models.DateField(null=True)


class ReproductiveHealth(BaseUuidModel):

    subject_visit = models.OneToOneField(SubjectVisit)

    currently_pregnant = models.CharField(
        max_length=25, choices=YES_NO, null=True)


class Circumcision(BaseUuidModel):

    subject_visit = models.OneToOneField(SubjectVisit)

    circumcised = models.CharField(max_length=25, choices=YES_NO, null=True)
