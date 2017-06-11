from .referral_code import ReferralCode


class Referral:

    referral_code_cls = ReferralCode

    def __init__(self, status_helper_cls=None, data_helper_cls=None,
                 referral_facilities=None, **kwargs):

        data_helper = data_helper_cls(**kwargs)
        subject_status = status_helper_cls(
            subject_visit=data_helper.subject_visit)
        self.referral_code = self.referral_code_cls(
            subject_status=subject_status, **kwargs).referral_code
        facility = referral_facilities.get_facility(
            referral_code=self.referral_code)

        self.referral_appt_datetime = facility.available_datetime(
            referral_code=self.referral_code,
            report_datetime=data_helper.subject_visit.report_datetime,
            scheduled_appt_date=data_helper.scheduled_appt_date)
        self.urgent_referral = facility.is_urgent(
            referral_code=self.referral_code)
        self.subject_identifier = data_helper.subject_identifier

    def __repr__(self):
        return f'{self.__class__.__name__}'

    def __str__(self):
        return f'{self.subject_identifier}: {self.referral_code}'
