from dateutil.relativedelta import MO, TU, WE, TH, FR
from edc_facility import Facility


class ReferralFacilityError(Exception):
    pass


class ReferralFacilityDateError(Exception):
    pass


class ReferralFacility:

    def __init__(self, name=None, days=None, facility=None, routine_codes=None, urgent_codes=None):
        if name:
            self.name = name
            self.facility = Facility(
                name=name, days=[MO, TU, WE, TH, FR],
                slots=[99999, 99999, 99999, 99999, 99999])
        else:
            self.name = facility.name
            self.facility = facility
        self.all_codes = []
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

    def available_datetime(self, referral_code=None, scheduled_appt_datetime=None,
                           report_datetime=None):
        """Returns a timezone aware datetime considering the referral_code.

        report_datetime: date to use if urgent
        scheduled_appt_datetime: date to use if not urgent
        """
        urgent_referral = self.is_urgent(referral_code=referral_code)
        if urgent_referral:
            if not report_datetime:
                raise ReferralFacilityDateError(
                    'Report datetime not specified for urgent referral. Report '
                    'datetime is needed to calculate an urgent referral '
                    'appointment date. Got None.')
            dt = report_datetime
        elif not urgent_referral:
            if not scheduled_appt_datetime:
                raise ReferralFacilityDateError(
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
