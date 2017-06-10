from django.test import TestCase, tag
from bcpp_referral.referral_code.referral_category import ReferralCategory


class TestReferralCategory(TestCase):

    def test_(self):
        obj = ReferralCategory()
        self.assertIsInstance(obj.idcc.routine, list)
        self.assertIsInstance(obj.idcc.urgent, list)
        self.assertIsInstance(obj.idcc.all, list)
        self.assertEqual(
            len(obj.idcc.routine) + len(obj.idcc.urgent), len(obj.idcc.all))
