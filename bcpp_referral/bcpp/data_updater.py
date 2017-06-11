from django.core.exceptions import ObjectDoesNotExist

from edc_constants.constants import YES, FEMALE, MALE


class DataUpdater:
    """Update data from model field values using reverse
    relations on SubjectVisit.

    PimaCd4, HivCareAdherence, SubjectReferral, ReproductiveHealth, Circumcision
    """

    def __init__(self, **kwargs):
        self.data = {}
        self.data.update(**kwargs)
        self.subject_visit = self.data.get('subject_visit')
        gender = self.data.get('gender')
        if not self.data.get('cd4_result'):
            try:
                self.data.update(
                    cd4_result=self.subject_visit.pimacd4.result_value)
            except ObjectDoesNotExist:
                pass
        if not self.data.get('cd4_result_datetime'):
            try:
                self.data.update(
                    cd4_result_datetime=self.subject_visit.pimacd4.result_datetime)
            except ObjectDoesNotExist:
                pass
        if not self.data.get('scheduled_appt_date'):
            try:
                self.data.update(
                    scheduled_appt_date=self.subject_visit.hivcareadherence.next_appointment_date)
            except ObjectDoesNotExist:
                pass
        if not self.data.get('scheduled_appt_date'):
            try:
                self.data.update(
                    scheduled_appt_date=self.subject_visit.subjectreferral.scheduled_appt_date)
            except ObjectDoesNotExist:
                pass

        if gender == FEMALE and self.data.get('pregnant') is None:
            self.data.update(pregnant=self.pregnant)
        elif gender == MALE and self.data.get('circumcision') is None:
            self.data.update(circumcised=self.circumcised)

    @property
    def pregnant(self):
        try:
            reproductive_health = self.subject_visit.reproductivehealth
        except ObjectDoesNotExist:
            pregnant = None
        else:
            pregnant = (
                True if reproductive_health.currently_pregnant == YES else False)
        return pregnant

    @property
    def circumcised(self):
        try:
            circumcision = self.subject_visit.circumcision
        except ObjectDoesNotExist:
            circumcised = None
        else:
            circumcised = circumcision.__class__.objects.filter(
                subject_visit__subject_identifier=self.subject_visit.subject_identifier,
                subject_visit__report_datetime__lte=self.subject_visit.report_datetime,
                circumcised=YES).exists()
        return circumcised
