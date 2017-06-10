# from datetime import timedelta
# from dateutil.relativedelta import relativedelta
# from datetime import datetime
# from model_mommy import mommy
#
# from django.test import TestCase, tag
#
# from edc_constants.constants import YES, NO, NEG, IND, NOT_APPLICABLE
# from edc_map.site_mappers import site_mappers
#
# from bcpp.communities import is_intervention
# from bcpp_subject.constants import T1, T2
# from household.constants import ELIGIBLE_REPRESENTATIVE_PRESENT
# from member.constants import ABLE_TO_PARTICIPATE
# from member.models.household_member.household_member import HouseholdMember
#
# from ..constants import ELISA, MICROTUBE
# from ..models import Appointment
# from .test_mixins import SubjectMixin
#
#
# class TestReferral(TestCase):
#
#     def setUp(self):
#         self.consent_data = {
#             'identity': '31721515',
#             'confirm_identity': '31721515',
#         }
#         self.survey_schedule = self.get_survey_schedule(index=0)
#         self.bhs_subject_visit_male = self.make_subject_visit_for_consented_subject_male(
#             'T0', survey_schedule=self.survey_schedule, **self.consent_data)
#         self.circumcision_benefits = mommy.make_recipe(
#             'bcpp_subject.circumcision_benefits')
#
#     def hiv_result(self, status, subject_visit, report_datetime=None):
#         """ Create HivResult for a particular survey.
#         """
#         report_datetime = report_datetime or self.get_utcnow()
#         mommy.make_recipe(
#             'bcpp_subject.subjectrequisition',
#             subject_visit=subject_visit,
#             report_datetime=report_datetime,
#             panel_name=MICROTUBE,
#         )
#         hiv_result = mommy.make_recipe(
#             'bcpp_subject.hivresult',
#             subject_visit=subject_visit,
#             report_datetime=report_datetime,
#             hiv_result=status, insufficient_vol=NO
#         )
#         return hiv_result
#
#     def ahs_y2_subject_visit(self):
#         """Return an ahs subject visit."""
#         # Create an ahs member
#         old_member = self.bhs_subject_visit_male.household_member
#         next_household_structure = self.get_next_household_structure_ready(
#             self.bhs_subject_visit_male.household_member.household_structure, make_hoh=None)
#         new_member = old_member.clone(
#             household_structure=next_household_structure,
#             report_datetime=next_household_structure.enumerated_datetime)
#         new_member.save()
#
#         new_member.inability_to_participate = ABLE_TO_PARTICIPATE
#         new_member.study_resident = YES
#         new_member.save()
#
#         new_member = HouseholdMember.objects.get(pk=new_member.pk)
#         report_datetime = self.get_utcnow() + relativedelta(years=1, months=6)
#         report = datetime(2010, 3, 4)
#         mommy.make_recipe(
#             'household.householdlogentry',
#             report_datetime=report,
#             household_log=new_member.household_structure.householdlog,
#             household_status=ELIGIBLE_REPRESENTATIVE_PRESENT)
#         self.consent_data.update(report_datetime=report_datetime)
#         self.add_subject_consent(
#             new_member, **self.consent_data)
#         appointment = Appointment.objects.get(
#             subject_identifier=new_member.subject_identifier,
#             visit_code=T1)
#         return mommy.make_recipe(
#             'bcpp_subject.subjectvisit',
#             household_member=new_member,
#             subject_identifier=new_member.subject_identifier,
#             appointment=appointment,
#             report_datetime=report_datetime)
#
#     def ahs_y3_subject_visit(self, household_member):
#         """Return an ahs  year 3 subject visit."""
#
#         household_structure = household_member.household_structure
#         next_household_structure = (
#             self.get_next_household_structure_ready(household_structure, make_hoh=None))
#
#         new_household_member = household_member.clone(
#             household_structure=next_household_structure,
#             report_datetime=next_household_structure.enumerated_datetime)
#         new_household_member.save()
#
#         new_household_member.inability_to_participate = ABLE_TO_PARTICIPATE
#         new_household_member.study_resident = YES
#         new_household_member.save()
#
#         new_household_member = HouseholdMember.objects.get(
#             pk=new_household_member.pk)
#
#         report_datetime = self.get_utcnow() + relativedelta(years=2)
#         self.consent_data.update(report_datetime=report_datetime)
#         subject_consent = self.add_subject_consent(
#             new_household_member, **self.consent_data)
#         appointment = Appointment.objects.get(
#             subject_identifier=subject_consent.subject_identifier,
#             visit_code=T2)
#
#         return mommy.make_recipe(
#             'bcpp_subject.subjectvisit',
#             household_member=subject_consent.household_member,
#             subject_identifier=subject_consent.household_member.subject_identifier,
#             appointment=appointment,
#             report_datetime=report_datetime)
#
#     @property
#     def referral_smc1(self):
#         mommy.make_recipe(
#             'bcpp_subject.hivresult',
#             subject_visit=self.bhs_subject_visit_male,
#             hiv_result=NEG)
#         mommy.make_recipe(
#             'bcpp_subject.circumcision',
#             subject_visit=self.bhs_subject_visit_male,
#             circumcised=NO,
#             health_benefits_smc=[self.circumcision_benefits])
#         subject_referral = mommy.make_recipe(
#             'bcpp_subject.subjectreferral', subject_referred=YES,
#             subject_visit=self.bhs_subject_visit_male,
#             report_datetime=self.get_utcnow(),
#             scheduled_appt_date=self.get_utcnow())
#         self.assertIn('SMC-NEG', subject_referral.referral_code)
#         subject_visit_t1 = self.ahs_y2_subject_visit()
#         mommy.make_recipe(
#             'bcpp_subject.subjectrequisition',
#             subject_visit=subject_visit_t1,
#             report_datetime=subject_visit_t1.report_datetime,
#             panel_name=MICROTUBE)
#         mommy.make_recipe(
#             'bcpp_subject.hivresult',
#             subject_visit=subject_visit_t1,
#             hiv_result=NEG,
#             report_datetime=subject_visit_t1.report_datetime)
#         mommy.make_recipe(
#             'bcpp_subject.circumcision',
#             subject_visit=subject_visit_t1,
#             circumcised=NO, report_datetime=subject_visit_t1.report_datetime,
#             health_benefits_smc=[self.circumcision_benefits])
#         subject_referral = mommy.make_recipe(
#             'bcpp_subject.subjectreferral', subject_referred=YES,
#             subject_visit=subject_visit_t1,
#             report_datetime=subject_visit_t1.report_datetime,
#             scheduled_appt_date=subject_visit_t1.report_datetime)
#         return subject_referral
#
#     @property
#     def referral_smc2(self):
#         mommy.make_recipe(
#             'bcpp_subject.subjectrequisition',
#             subject_visit=self.bhs_subject_visit_male,
#             report_datetime=self.get_utcnow(),
#             panel_name='Microtube')
#         mommy.make_recipe(
#             'bcpp_subject.hivresult',
#             subject_visit=self.bhs_subject_visit_male,
#             hiv_result=NEG)
#         mommy.make_recipe(
#             'bcpp_subject.circumcision',
#             subject_visit=self.bhs_subject_visit_male,
#             circumcised=YES,
#             health_benefits_smc=[self.circumcision_benefits])
#         subject_referral = mommy.make_recipe(
#             'bcpp_subject.subjectreferral',
#             subject_referred=YES,
#             subject_visit=self.bhs_subject_visit_male,
#             report_datetime=self.get_utcnow(),
#             scheduled_appt_date=self.get_utcnow())
#         self.assertNotIn('SMC', subject_referral.referral_code)
#
#         subject_visit_t1 = self.ahs_y2_subject_visit()
#
#         subject_referral = mommy.make_recipe(
#             'bcpp_subject.subjectreferral',
#             subject_referred=YES,
#             subject_visit=subject_visit_t1,
#             report_datetime=subject_visit_t1.report_datetime,
#             scheduled_appt_date=subject_visit_t1.report_datetime)
#         return subject_referral
#
#     def hivtest_review(self, subject_visit, hiv_status, report_datetime=None):
#         report_datetime = report_datetime or self.get_utcnow()
#         hiv_test_review = mommy.make_recipe(
#             'bcpp_subject.hivtestreview',
#             report_datetime=report_datetime,
#             subject_visit=subject_visit,
#             hiv_test_date=self.get_utcnow() - timedelta(days=50),
#             recorded_hiv_result=hiv_status)
#         return hiv_test_review
#
#     def tests_referred_hiv(self):
#         """if IND refer for HIV testing"""
#         mommy.make_recipe(
#             'bcpp_subject.subjectrequisition',
#             subject_visit=self.bhs_subject_visit_male,
#             report_datetime=self.get_utcnow(),
#             panel_name=MICROTUBE)
#         mommy.make_recipe(
#             'bcpp_subject.subjectrequisition',
#             subject_visit=self.bhs_subject_visit_male,
#             report_datetime=self.get_utcnow(),
#             panel_name=ELISA)
#         mommy.make_recipe(
#             'bcpp_subject.hivresult',
#             subject_visit=self.bhs_subject_visit_male,
#             hiv_result=IND)
#         subject_referral = mommy.make_recipe(
#             'bcpp_subject.subjectreferral', subject_referred=YES,
#             subject_visit=self.bhs_subject_visit_male,
#             report_datetime=self.get_utcnow(),
#             scheduled_appt_date=self.get_utcnow())
#         self.assertIn('', subject_referral.referral_code)
#
#     def tests_referred_smc1(self):
#         """if NEG and male and NOT circumcised, refer for SMC in Y1 intervention
#         and also refer in Y2 intervention"""
#         if is_intervention(site_mappers.current_map_area):
#             subject_referral = self.referral_smc1
#             self.assertIn('SMC-NEG', subject_referral.referral_code)
#
#     def tests_referred_smc1a(self):
#         """if NEG and male and NOT circumcised, refer for SMC
#         in Y1 non-intervention and do not refer in Y2 non-intervention"""
#         if not is_intervention(site_mappers.current_map_area):
#             subject_referral = self.referral_smc1
#             self.assertEqual('', subject_referral.referral_code)
#
#     def tests_referred_smc2(self):
#         """if NEG and male and circumcised, do not refer for SMC,
#             both Y1 and Y2 intervention"""
#         if is_intervention(site_mappers.current_map_area):
#             subject_referral = self.referral_smc2
#             self.assertNotIn('SMC', subject_referral.referral_code)
#
#     def tests_circumsised_y2_not_smc(self):
#         """if NEG and male and not circumcised in Y1, then refer for SMC in Y1.
#             Then if male circumsised in Y2 then do not refer for SMC in Y2."""
#         self.hiv_result(NEG, self.bhs_subject_visit_male, self.get_utcnow())
#         mommy.make_recipe(
#             'bcpp_subject.hivresultdocumentation',
#             subject_visit=self.bhs_subject_visit_male,
#             result_recorded=NEG,
#             result_doc_type='Tebelopele')
#         self.hivtest_review(self.bhs_subject_visit_male, NEG)
#         mommy.make_recipe(
#             'bcpp_subject.hivtestinghistory',
#             subject_visit=self.bhs_subject_visit_male,
#             has_tested=YES,
#             verbal_hiv_result=NEG,)
#         mommy.make_recipe(
#             'bcpp_subject.circumcision',
#             subject_visit=self.bhs_subject_visit_male,
#             circumcised=NO,
#             health_benefits_smc=[self.circumcision_benefits])
#         subject_referral = mommy.make_recipe(
#             'bcpp_subject.subjectreferral',
#             subject_referred=YES,
#             subject_visit=self.bhs_subject_visit_male,
#             report_datetime=self.get_utcnow(),
#             scheduled_appt_date=self.get_utcnow())
#         self.assertIn('SMC', subject_referral.referral_code)
#
#         subject_visit_t1 = self.ahs_y2_subject_visit()
#
#         mommy.make_recipe(
#             'bcpp_subject.circumcision',
#             subject_visit=subject_visit_t1,
#             report_datetime=subject_visit_t1.report_datetime,
#             circumcised=YES,
#             health_benefits_smc=[self.circumcision_benefits])
#         subject_referral = mommy.make_recipe(
#             'bcpp_subject.subjectreferral',
#             subject_referred=YES,
#             subject_visit=subject_visit_t1,
#             report_datetime=subject_visit_t1.report_datetime,
#             scheduled_appt_date=subject_visit_t1.report_datetime)
#         self.assertNotIn('SMC', subject_referral.referral_code)
