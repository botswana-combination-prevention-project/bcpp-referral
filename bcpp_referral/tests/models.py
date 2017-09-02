from django.db import models
from edc_appointment.models import Appointment
from edc_base.model_mixins.base_uuid_model import BaseUuidModel
from edc_base.utils import get_utcnow
from edc_constants.choices import YES_NO
from edc_constants.constants import YES
from edc_reference.model_mixins import ReferenceModelMixin


class CrfModelMixin(models.Model):

    @property
    def subject_identifier(self):
        return self.subject_visit.subject_identifier

    @property
    def visit_code(self):
        return self.subject_visit.visit_code


class SubjectVisit(ReferenceModelMixin, BaseUuidModel):

    appointment = models.ForeignKey(Appointment, null=True)

    subject_identifier = models.CharField(max_length=25)

    report_datetime = models.DateTimeField(default=get_utcnow)

    visit_code = models.CharField(max_length=25, default='T0')

    survey = models.CharField(max_length=25, default='survey')

    survey_schedule = models.CharField(
        max_length=25, default='survey_schedule')


class SubjectReferral(ReferenceModelMixin, CrfModelMixin, BaseUuidModel):

    report_datetime = models.DateTimeField(default=get_utcnow)

    subject_visit = models.OneToOneField(SubjectVisit)

    scheduled_appt_date = models.DateField(null=True)


class PimaCd4(ReferenceModelMixin, CrfModelMixin, BaseUuidModel):

    subject_visit = models.OneToOneField(SubjectVisit)

    report_datetime = models.DateTimeField(default=get_utcnow)

    result_value = models.IntegerField(null=True)

    result_datetime = models.DateTimeField(null=True)


class HivCareAdherence(ReferenceModelMixin, CrfModelMixin, BaseUuidModel):

    subject_visit = models.OneToOneField(SubjectVisit)

    report_datetime = models.DateTimeField(default=get_utcnow)

    next_appointment_date = models.DateField(null=True)

    arv_evidence = models.CharField(max_length=25, null=True)

    ever_taken_arv = models.CharField(max_length=25, null=True)

    on_arv = models.CharField(max_length=25, null=True)

    medical_care = models.CharField(max_length=25, default=YES)


class ReproductiveHealth(ReferenceModelMixin, CrfModelMixin, BaseUuidModel):

    subject_visit = models.OneToOneField(SubjectVisit)

    report_datetime = models.DateTimeField(default=get_utcnow)

    currently_pregnant = models.CharField(
        max_length=25, choices=YES_NO, null=True)


class Circumcision(ReferenceModelMixin, CrfModelMixin, BaseUuidModel):

    subject_visit = models.OneToOneField(SubjectVisit)

    report_datetime = models.DateTimeField(default=get_utcnow)

    circumcised = models.CharField(max_length=25, choices=YES_NO, null=True)

    @property
    def subject_identifier(self):
        return self.subject_visit.subject_identifier
