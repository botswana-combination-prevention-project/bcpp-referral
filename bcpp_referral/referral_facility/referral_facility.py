
class ReferralFacilityError(Exception):
    pass


class ReferralFacility:

    def __init__(self, facility=None, routine_codes=None, urgent_codes=None):
        self.name = facility.name
        self.all_codes = []
        self.facility = facility
        self.routine_codes = routine_codes or []
        self.urgent_codes = urgent_codes or []
        self.all_codes.extend(self.routine_codes)
        self.all_codes.extend(self.urgent_codes)
        self.all_codes.sort()
        if len(list(set(self.all_codes))) != len(self.all_codes):
            raise ReferralFacilityError(
                f'Duplicate code. Codes must be unique. Got {self.all_codes}')

    def __repr__(self):
        return f'{self.__class__.__name__}({self.__dict__})'

    def __str__(self):
        return self.name

    def available_datetime(self, referral_code=None, scheduled_appt_datetime=None, report_datetime=None):
        """Returns a timezone aware datetime considering the referral_code.

        report_datetime: date to use if urgent
        scheduled_appt_datetime: date to use if not urgent
        """
        if self.is_urgent(referral_code=referral_code):
            if not report_datetime:
                raise ReferralFacilityError(
                    'Report datetime not specified for urgent referral. Report '
                    'datetime is needed to calculate an urgent referral '
                    'appointment date. Got None.')
            dt = report_datetime
        elif not self.is_urgent(referral_code=referral_code):
            if not scheduled_appt_datetime:
                raise ReferralFacilityError(
                    'Scheduled appointment datetime not specified for routine appointment. '
                    'A scheduled appointment datetime is needed to calculate a routine '
                    'referral appointment date. Got None.')
            dt = scheduled_appt_datetime
        return self.facility.available_datetime(suggested_datetime=dt)

    def is_urgent(self, referral_code=None):
        """Returns the priority, urgent or routine, given a referral code
        otherwise None.
        """
        if referral_code in self.urgent_codes:
            return True
        elif referral_code in self.routine_codes:
            return False
        raise ReferralFacilityError(
            f'Unknown referral code for facility. Got {referral_code}.')
