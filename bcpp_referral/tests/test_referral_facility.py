from arrow.arrow import Arrow
from datetime import datetime
from django.test import TestCase, tag
from dateutil.relativedelta import MO, TU, WE, weekday

from edc_appointment.facility import Facility

from ..referral_facility import ReferralFacilities, ReferralFacility, ReferralFacilityError
from ..referral_facility import ReferralFacilityDuplicateCode, ReferralFacilityAlreadyRegistered
from ..referral_facility import ReferralFacilityNotFound


@tag('referral_codes')
class TestReferralFacility(TestCase):

    def test_referral_facility_code_lists(self):
        facility = Facility(
            name='leiden', days=[MO, TU, WE], forward_only=True)
        referral_facility = ReferralFacility(facility=facility)
        self.assertIsInstance(referral_facility.routine_codes, list)
        self.assertIsInstance(referral_facility.urgent_codes, list)
        self.assertIsInstance(referral_facility.all_codes, list)
        self.assertEqual(
            len(referral_facility.routine_codes) +
            len(referral_facility.urgent_codes),
            len(referral_facility.all_codes))

    def test_referral_facility_repr(self):
        facility = Facility(
            name='leiden', days=[TU, WE], forward_only=True)
        referral_facility = ReferralFacility(
            facility=facility, urgent_codes=['MASA-DF'], routine_codes=['MASA-CC'])
        self.assertTrue(repr(referral_facility))

    def test_referral_facility_duplicate_referral_code(self):
        facility = Facility(
            name='leiden', days=[TU, WE], forward_only=True)
        self.assertRaises(
            ReferralFacilityError,
            ReferralFacility,
            facility=facility, urgent_codes=['MASA-DF'], routine_codes=['MASA-DF'])

    def test_referral_facility_is_urgent(self):
        facility = Facility(
            name='leiden', days=[TU, WE], forward_only=True)
        referral_facility = ReferralFacility(
            facility=facility, urgent_codes=['MASA-DF'], routine_codes=['MASA-CC'])
        self.assertTrue(referral_facility.is_urgent('MASA-DF'))
        self.assertFalse(referral_facility.is_urgent('MASA-CC'))

    def test_referral_facility_is_urgent_invalid_code(self):
        facility = Facility(
            name='leiden', days=[TU, WE], forward_only=True)
        referral_facility = ReferralFacility(
            facility=facility, urgent_codes=['MASA-DF'], routine_codes=['MASA-CC'])
        self.assertRaises(ReferralFacilityError,
                          referral_facility.is_urgent, 'BLAH')

    def test_referral_facility_available_datetime_day(self):
        facility = Facility(
            name='leiden', days=[TU, WE], forward_only=True)
        referral_facility = ReferralFacility(
            facility=facility, routine_codes=['MASA-CC'])
        scheduled_appt_datetime = Arrow.fromdate(
            datetime(2001, 12, 4, 7, 30)).datetime
        dt = referral_facility.available_datetime(
            referral_code='MASA-CC',
            scheduled_appt_datetime=scheduled_appt_datetime)
        self.assertEqual(weekday(dt.weekday()), TU)
        scheduled_appt_datetime = Arrow.fromdate(
            datetime(2001, 12, 5, 7, 30)).datetime
        dt = referral_facility.available_datetime(
            referral_code='MASA-CC',
            scheduled_appt_datetime=scheduled_appt_datetime)
        self.assertEqual(weekday(dt.weekday()), WE)
        scheduled_appt_datetime = Arrow.fromdate(
            datetime(2001, 12, 6, 7, 30)).datetime
        dt = referral_facility.available_datetime(
            referral_code='MASA-CC',
            scheduled_appt_datetime=scheduled_appt_datetime)
        self.assertEqual(weekday(dt.weekday()), TU)

    def test_referral_facility_urgent_available_datetime_raises(self):
        facility = Facility(
            name='leiden', days=[TU, WE], forward_only=True)
        referral_facility = ReferralFacility(
            facility=facility, routine_codes=['MASA-CC'], urgent_codes=['MASA-DF'])
        self.assertRaises(
            ReferralFacilityError,
            referral_facility.available_datetime, referral_code='MASA-DF')

    def test_referral_facility_routine_available_datetime_raises(self):
        facility = Facility(
            name='leiden', days=[TU, WE], forward_only=True)
        referral_facility = ReferralFacility(
            facility=facility, routine_codes=['MASA-CC'], urgent_codes=['MASA-DF'])
        self.assertRaises(
            ReferralFacilityError,
            referral_facility.available_datetime, referral_code='MASA-CC')

    def test_referral_facility_routine_available_datetime(self):
        """Asserts picks appt date near schedule appt date if routine.
        """
        facility = Facility(
            name='leiden', days=[TU, WE], forward_only=True)
        referral_facility = ReferralFacility(
            facility=facility, routine_codes=['MASA-CC'], urgent_codes=['MASA-DF'])
        # pick a tuesday
        scheduled_appt_datetime = Arrow.fromdate(
            datetime(2001, 12, 4, 7, 30)).datetime
        dt = referral_facility.available_datetime(
            referral_code='MASA-CC',
            scheduled_appt_datetime=scheduled_appt_datetime)
        self.assertEqual(dt, scheduled_appt_datetime)

    def test_referral_facility_urgent_available_datetime(self):
        """Asserts picks correct date.
        """
        facility = Facility(
            name='leiden', days=[TU, WE], forward_only=True)
        referral_facility = ReferralFacility(
            facility=facility, routine_codes=['MASA-CC'], urgent_codes=['MASA-DF'])
        # pick a tuesday
        scheduled_appt_datetime = Arrow.fromdate(
            datetime(2001, 12, 4, 7, 30)).datetime
        # pick a wednesday
        report_datetime = Arrow.fromdate(datetime(2001, 12, 5, 7, 30)).datetime
        dt = referral_facility.available_datetime(
            referral_code='MASA-CC',
            scheduled_appt_datetime=scheduled_appt_datetime,
            report_datetime=report_datetime)
        self.assertEqual(dt, scheduled_appt_datetime)
        dt = referral_facility.available_datetime(
            referral_code='MASA-DF',
            scheduled_appt_datetime=scheduled_appt_datetime,
            report_datetime=report_datetime)
        self.assertEqual(dt, report_datetime)


@tag('referral_codes')
class TestReferralFacilities(TestCase):

    def test_add_facility(self):
        facility = Facility(
            name='leiden', days=[TU, WE], forward_only=True)
        referral_facility = ReferralFacility(
            facility=facility, routine_codes=['MASA-CC'], urgent_codes=['MASA-DF'])
        facilities = ReferralFacilities(name='test')
        facilities.add_facility(facility=referral_facility)
        self.assertIn('leiden', facilities.facilities)

    def test_duplicate_facility(self):
        facility = Facility(
            name='leiden', days=[TU, WE], forward_only=True)
        referral_facility = ReferralFacility(
            facility=facility, routine_codes=['MASA-CC'], urgent_codes=['MASA-DF'])
        facilities = ReferralFacilities(name='test')
        facilities.add_facility(facility=referral_facility)
        self.assertRaises(
            ReferralFacilityAlreadyRegistered,
            facilities.add_facility, facility=referral_facility)

    def test_all_codes(self):
        facility1 = Facility(
            name='nijmegen', days=[TU, WE], forward_only=True)
        facility2 = Facility(
            name='leiden', days=[TU, WE], forward_only=True)
        referral_facility1 = ReferralFacility(
            facility=facility1, routine_codes=['A'], urgent_codes=['B'])
        referral_facility2 = ReferralFacility(
            facility=facility2, routine_codes=['C'], urgent_codes=['D'])
        facilities = ReferralFacilities(name='test')
        facilities.add_facility(facility=referral_facility1)
        facilities.add_facility(facility=referral_facility2)
        self.assertEqual(facilities.all_codes, ['A', 'B', 'C', 'D'])


@tag('referral_codes')
class TestReferralFacilities2(TestCase):

    def setUp(self):
        self.facility1 = Facility(
            name='nijmegen', days=[TU, WE], forward_only=True)
        self.facility2 = Facility(
            name='leiden', days=[TU, WE], forward_only=True)

    def test_get_all_codes_from_facilities(self):
        referral_facility1 = ReferralFacility(
            facility=self.facility1, routine_codes=['A'], urgent_codes=['B'])
        referral_facility2 = ReferralFacility(
            facility=self.facility2, routine_codes=['C'], urgent_codes=['D'])
        facilities = ReferralFacilities(name='test')
        facilities.add_facility(facility=referral_facility1)
        facilities.add_facility(facility=referral_facility2)
        self.assertEqual(facilities.all_codes, ['A', 'B', 'C', 'D'])

    def test_get_urgent_codes_from_facilities(self):
        referral_facility1 = ReferralFacility(
            facility=self.facility1, routine_codes=['A'], urgent_codes=['B'])
        referral_facility2 = ReferralFacility(
            facility=self.facility2, routine_codes=['C'], urgent_codes=['D'])
        facilities = ReferralFacilities(name='test')
        facilities.add_facility(facility=referral_facility1)
        facilities.add_facility(facility=referral_facility2)
        self.assertEqual(facilities.urgent_codes, ['B', 'D'])

    def test_get_routine_codes_from_facilities(self):
        referral_facility1 = ReferralFacility(
            facility=self.facility1, routine_codes=['A'], urgent_codes=['B'])
        referral_facility2 = ReferralFacility(
            facility=self.facility2, routine_codes=['C'], urgent_codes=['D'])
        facilities = ReferralFacilities(name='test')
        facilities.add_facility(facility=referral_facility1)
        facilities.add_facility(facility=referral_facility2)
        self.assertEqual(facilities.routine_codes, ['A', 'C'])

    def test_cannot_add_facility_with_duplicate_code(self):
        referral_facility1 = ReferralFacility(
            facility=self.facility1, routine_codes=['MASA-CC'], urgent_codes=['MASA-DF'])
        referral_facility2 = ReferralFacility(
            facility=self.facility2, routine_codes=['MASA-CC'], urgent_codes=['MASA-DF'])
        facilities = ReferralFacilities(name='test')
        facilities.add_facility(facility=referral_facility1)
        self.assertRaises(
            ReferralFacilityDuplicateCode,
            facilities.add_facility, facility=referral_facility2)

    def test_get_facility_from_facilities_by_code(self):
        referral_facility1 = ReferralFacility(
            facility=self.facility1, routine_codes=['A'], urgent_codes=['B'])
        referral_facility2 = ReferralFacility(
            facility=self.facility2, routine_codes=['C'], urgent_codes=['D'])
        facilities = ReferralFacilities(name='test')
        facilities.add_facility(facility=referral_facility1)
        facilities.add_facility(facility=referral_facility2)
        self.assertEqual(referral_facility1, facilities.get_facility('A'))
        self.assertEqual(referral_facility1, facilities.get_facility('B'))
        self.assertEqual(referral_facility2, facilities.get_facility('C'))
        self.assertEqual(referral_facility2, facilities.get_facility('D'))
        self.assertRaises(
            ReferralFacilityNotFound,
            facilities.get_facility, 'BLAH')
