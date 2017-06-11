from .referral_code import ReferralCode


class Referral:

    referral_code_cls = ReferralCode

    def __init__(self, referral_facilities=None, subject_identifier=None,
                 subject_visit=None, report_datetime=None,
                 scheduled_appt_datetime=None, **kwargs):

        self.subject_visit = subject_visit
        self.subject_identifier = subject_identifier
        self.report_datetime = report_datetime
        self.scheduled_appt_datetime = scheduled_appt_datetime

        self.referral_code = self.referral_code_cls(**kwargs).referral_code
        self.facility = referral_facilities.get_facility(
            referral_code=self.referral_code)

        self.referral_appt_datetime = self.facility.available_datetime(
            referral_code=self.referral_code,
            report_datetime=self.report_datetime,
            scheduled_appt_datetime=self.scheduled_appt_datetime)
        self.urgent_referral = self.facility.is_urgent(
            referral_code=self.referral_code)
        self.subject_identifier = self.subject_identifier

    def __repr__(self):
        return f'{self.__class__.__name__}'

    def __str__(self):
        return f'{self.subject_identifier}: {self.referral_code}'
