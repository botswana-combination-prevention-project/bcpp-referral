from datetime import datetime, timedelta, time
from dateutil.relativedelta import relativedelta, MO, TU, WE, TH, FR
from collections import namedtuple

from django.core.exceptions import ValidationError

from edc_appointment.models import Holiday

from .next_clinic_date import next_clinic_date
from .clinic_type import ClinicType
from arrow.arrow import Arrow
from bcpp_referral.referral_code.referral_category import ReferralCategory


class RoutineClinic:

    def __init__(self, report_datetime=None, scheduled_appt_date=None):
        report_date = Arrow.fromdatetime(report_datetime).date()
        if scheduled_appt_date <= (report_date + relativedelta(months=1)):
            self.appt_datetime = Arrow.fromdate(scheduled_appt_date).datetime
        else:
            self.appt_datetime = report_datetime + relativedelta(weeks=2)


class ReferralAppt:
    """A class to determine the referral appointment date.

    The referral code will determine the correct clinic,
    IDCC, ANC, SMC, SMC-ECC, to pass to the method

    either:
        smc appointment
        next clinic date for all newly diagnosed
        next scheduled appointment if they have one
        next clinic date if they dont have an appointment

        for masa-cc need to collect VL one or before next appointment
        if next appointment is within a month, keep it
        if not within a month, set an appointmnt for 2 weeks

    all appointments should land on facility days



    """

    clinic_type_cls = ClinicType
    routine_clinic_cls = RoutineClinic
    referral_category = ReferralCategory()

    def __init__(self, report_datetime=None, referral_code=None, scheduled_appt_date=None,
                 routine_facility=None, smc_facility=None, vct_facility=None, anc_facility=None):
        self._referral_appt_datetime = None
        self.report_datetime = report_datetime
        self.scheduled_appt_date = scheduled_appt_date
        self.referral_code = referral_code
        self.referral_clinic_type = self.clinic_type_cls(
            referral_code=self.referral_code)
        self.idcc_facility = routine_facility
        self.smc_facility = smc_facility
        self.vct_facility = vct_facility
        self.anc_facility = anc_facility

    @property
    def referral_appt_datetime(self):
        if not self._referral_appt_datetime:
            if self.referral_code in self.referral_category.idcc.urgent:
                appt_datetime = self.next_clinic_datetime
            elif self.referral_code in self.referral_category.anc.urgent:
                appt_datetime = self.next_clinic_datetime
            elif self.referral_code in self.smc_referrals:
                appt_datetime = self.smc_appt_datetime
            elif self.referral_code in self.routine_referrals:
                routine_clinic = self.routine_clinic_cls(
                    report_datetime=self.report_datetime,
                    scheduled_appt_date=self.scheduled_appt_date)
                appt_datetime = routine_clinic.appt_datetime
            self._referral_appt_datetime = self.facility.available_datetime(
                appt_datetime)
        return self._referral_appt_datetime

    def __repr__(self):
        return f'{self.__class__.__name__}({self.referral_code})'

    def __str__(self):
        return f'{self.referral_code}'

#     def referral_appt_datetime_other(self):
#         """ Docstring is required """
#         referral_appt_datetime = None
#         try:
#             if self.scheduled_appt_datetime <= self.base_datetime + relativedelta(months=1):
#                 referral_appt_datetime = self.scheduled_appt_datetime
#         except TypeError as error_msg:
#             if "can't compare datetime.datetime to NoneType" not in error_msg:
#                 raise TypeError(error_msg)
#             pass
#         if not referral_appt_datetime and 'MASA' in self.referral_code:
#             referral_appt_datetime = self.masa_appt_datetime

#     @property
#     def scheduled_appt_datetime(self):
#         """Returns a datetime as long as the date is within 1 month
#         of today otherwise leaves the date as None.
#         """
#     # TODO: use facility from edc_appointment
#         scheduled_appt_datetime = None
#         if self.original_scheduled_appt_date:
#             scheduled_appt_datetime = datetime(self.original_scheduled_appt_date.year,
#                                                self.original_scheduled_appt_date.month,
#                                                self.original_scheduled_appt_date.day, 7, 30, 0)
#             if self.base_datetime > scheduled_appt_datetime:
#                 raise ValidationError('Expected future date for scheduled appointment, '
#                                       'Got {0}'.format(self.original_scheduled_appt_date))
#             rdelta = relativedelta(scheduled_appt_datetime, self.base_datetime)
#             if rdelta.years == 0 and ((rdelta.months == 1
#                                        and rdelta.days == 0)
#                                       or (rdelta.months == 0)):
#                 scheduled_appt_datetime = next_clinic_date(self.clinic_days,
#                                                            scheduled_appt_datetime,
#                                                            allow_same_day=True)
#         return scheduled_appt_datetime

    @property
    def smc_appt_datetime(self):
        """Returns a datetime that is either the smc start date or the
        next smc clinic day depending on whether today is before or
        after smc_start_date.
        """
        if site_mappers.current_mapper.intervention:
            smc_appt_datetime = self.next_workday()
        else:
            return None
        return smc_appt_datetime

    def next_workday(self):
        """This method returns the next week day that is not a holyday and
        is not a weekend.
        """
        holidays = []
        next_workday = datetime(
            (datetime.today() + timedelta(days=1)).year,
            (datetime.today() + timedelta(days=1)).month,
            (datetime.today() + timedelta(days=1)).day, 7, 30, 0)
        for holyday in Holiday.objects.all():
            holidays.append(holyday.day)
        if next_workday.date() not in holidays:
            if next_workday.isoweekday() == 6:
                next_workday = datetime(
                    (next_workday + timedelta(days=1)).year,
                    (datetime.today() + timedelta(days=1)).month,
                    (datetime.today() + timedelta(days=3)).day, 7, 30, 0)
            elif next_workday.isoweekday() == 7 and next_workday.date() not in holidays:
                next_workday = datetime(
                    (next_workday + timedelta(days=1)).year,
                    (datetime.today() + timedelta(days=1)).month,
                    (datetime.today() + timedelta(days=1)).day, 7, 30, 0)
        else:
            next_workday = datetime(
                (datetime.today() + timedelta(days=1)).year,
                (datetime.today() + timedelta(days=1)).month,
                (datetime.today() + timedelta(days=1)).day, 7, 30, 0)
            next_workday()
        return next_workday
