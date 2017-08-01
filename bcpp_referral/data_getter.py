from django.core.exceptions import ObjectDoesNotExist

from edc_constants.constants import YES, FEMALE, MALE
from edc_registration.models import RegisteredSubject
from pprint import pprint


class ReferralDataGetterError(Exception):
    pass


class DataGetter:
    """Update data from model field values using reverse
    relations on SubjectVisit.

    PimaCd4, HivCareAdherence, SubjectReferral, ReproductiveHealth, Circumcision
    """

    def __init__(self, subject_visit=None):
        self._cd4_result = None
        self._cd4_result_datetime = None
        self._circumcised = None
        self._pregnant = None
        self._scheduled_appt_date = None
        self.subject_visit = subject_visit
        report_datetime = subject_visit.report_datetime
        subject_identifier = subject_visit.subject_identifier
        self._data = dict(
            subject_visit=self.subject_visit,
            report_datetime=report_datetime,
            subject_identifier=subject_identifier,
            cd4_result=self.cd4_result,
            cd4_result_datetime=self.cd4_result_datetime,
            scheduled_appt_date=self.scheduled_appt_date,
            gender=self.gender)
        if self.gender == FEMALE:
            self._data.update(pregnant=self.pregnant)
        elif self.gender == MALE:
            self._data.update(circumcised=self.circumcised)
        for k, v in self._data.items():
            try:
                setattr(self, k, v)
            except AttributeError:
                pass
            except ReferralDataGetterError:
                pass

    def __iter__(self):
        return iter(self._data.items())

    @property
    def pregnant(self):
        if self._pregnant is None:
            if self.gender != FEMALE:
                raise ReferralDataGetterError(
                    'Invalid attribute. Subject is not FEMALE.')
            try:
                reproductive_health = self.subject_visit.reproductivehealth
            except ObjectDoesNotExist:
                self._pregnant = None
            else:
                self._pregnant = (
                    True if reproductive_health.currently_pregnant == YES else False)
        return self._pregnant

    @property
    def circumcised(self):
        if self._circumcised is None:
            if self.gender != MALE:
                raise ReferralDataGetterError(
                    'Invalid attribute. Subject is not MALE.')
            try:
                self._circumcised = self.subject_visit.circumcision
            except ObjectDoesNotExist:
                self._circumcised = None
            else:
                self._circumcised = self.subject_visit.circumcision.__class__.objects.filter(
                    subject_visit__subject_identifier=self.subject_visit.subject_identifier,
                    subject_visit__report_datetime__lte=self.subject_visit.report_datetime,
                    circumcised=YES).exists()
        return self._circumcised

    @property
    def gender(self):
        gender = None
        try:
            registered_subject = RegisteredSubject.objects.get(
                subject_identifier=self.subject_visit.subject_identifier)
        except RegisteredSubject.DoesNotExist as e:
            raise ReferralDataGetterError(
                f'Subject is not registered. subject_identifier='
                f'\'{self.subject_visit.subject_identifier}\'. Got {e}')
        except AttributeError:
            gender = None
        else:
            gender = registered_subject.gender
        return gender

    @property
    def scheduled_appt_date(self):
        """Returns the next scheduled appointment date from either
        hivcareadherence or subjectreferral.
        """
        if not self._scheduled_appt_date:
            try:
                self._scheduled_appt_date = (
                    self.subject_visit.hivcareadherence.next_appointment_date)
            except ObjectDoesNotExist:
                pass
            if not self._scheduled_appt_date:
                try:
                    self._scheduled_appt_date = (
                        self.subject_visit.subjectreferral.scheduled_appt_date)
                except ObjectDoesNotExist:
                    self._scheduled_appt_date = None
        return self._scheduled_appt_date

    @property
    def cd4_result(self):
        if not self._cd4_result:
            try:
                self._cd4_result = self.subject_visit.pimacd4.result_value
            except ObjectDoesNotExist:
                self._cd4_result = None
        return self._cd4_result

    @property
    def cd4_result_datetime(self):
        if not self._cd4_result_datetime:
            try:
                self._cd4_result_datetime = self.subject_visit.pimacd4.result_datetime
            except ObjectDoesNotExist:
                self._cd4_result_datetime = None
        return self._cd4_result_datetime
