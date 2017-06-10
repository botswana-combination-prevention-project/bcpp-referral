from django.core.exceptions import ObjectDoesNotExist

from edc_registration.models import RegisteredSubject


class ReferralDataError(Exception):
    pass


class DataHelper:

    def __init__(self, subject_visit=None, **kwargs):
        self.subject_visit = subject_visit
        self.subject_identifier = subject_visit.subject_identifier
        try:
            registered_subject = RegisteredSubject.objects.get(
                subject_identifier=self.subject_identifier)
        except RegisteredSubject.DoesNotExist as e:
            raise ReferralDataError(
                f'Subject is not registered. subject_identifier='
                f'\'{self.subject_identifier}\'. Got {e}')
        self.gender = registered_subject.gender
        try:
            pima_cd4 = self.subject_visit.pimacd4
        except ObjectDoesNotExist:
            self.cd4_result = None
            self.cd4_result_datetime = None
        else:
            self.cd4_result = pima_cd4.result_value
            self.cd4_result_datetime = pima_cd4.result_datetime
        try:
            hiv_care_adherence = self.subject_visit.hivcareadherence
        except ObjectDoesNotExist:
            self.scheduled_appt_date = None
        else:
            self.scheduled_appt_date = hiv_care_adherence.next_appointment_date
        if not self.scheduled_appt_date:
            try:
                subject_referral = subject_visit.subjectreferral
            except ObjectDoesNotExist:
                self.scheduled_appt_date = None
            else:
                self.scheduled_appt_date = subject_referral.scheduled_appt_date
        for k, v in kwargs.items():
            try:
                value = getattr(self, k)
            except AttributeError:
                pass
            else:
                if not value:
                    setattr(self, k, v)
