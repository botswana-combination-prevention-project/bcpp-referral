from django.apps import apps as django_apps

from edc_constants.constants import POS, FEMALE, NOT_APPLICABLE


from ..models import ResidencyMobility
from ..subject_helper import ON_ART, DEFAULTER


class CdcReferral:

    def __init__(self, referral, **kwargs):
        self.on_art = None
        self.arv_clinic = None
        self.arv_documentation = referral.subject_helper.arv_evidence
        if referral.hiv_care_adherence:
            self.arv_clinic = referral.hiv_care_adherence.clinic_receiving_from
        self.citizen = referral.subject_referral.subject_visit.household_member.citizen
        self.citizen_spouse = (
            referral.subject_referral.subject_visit.household_member.spouse_of_citizen)
        self.direct_hiv_documentation = referral.subject_helper.documented_pos
        self.gender = referral.gender
        self.hiv_result_date = referral.subject_helper.final_hiv_status_date
        self.last_hiv_result = referral.subject_helper.prev_result
        self.last_hiv_result_date = referral.subject_helper.prev_result_date
        self.new_pos = referral.subject_helper.newly_diagnosed

        self.part_time_resident = (
            referral.subject_referral.subject_visit.household_member.study_resident)
        self.subject_identifier = referral.subject_identifier
        self.todays_hiv_result = referral.subject_helper.today_hiv_result
        self.verbal_hiv_result = referral.subject_helper.self_reported_result
#         self.cd4_result = self.subject_helper.cd4_result
#         self.cd4_result_datetime = self.subject_helper.cd4_result_datetime
#         self.vl_sample_drawn = self.subject_helper.vl_sample_drawn
#         self.vl_sample_drawn_datetime = self.subject_helper.vl_sample_drawn_datetime
#         self.indirect_hiv_documentation = self.subject_helper.indirect_hiv_documentation
        self.hiv_result = referral.subject_helper.final_hiv_status
        if referral.subject_helper.final_hiv_status == POS:
            self.on_art = True if referral.subject_helper.final_arv_status in [
                ON_ART, DEFAULTER] else False
        self.defaulter = (
            True if referral.subject_helper.final_arv_status == DEFAULTER else False)

        self.original_scheduled_appt_date = (
            referral.referral_appt.original_scheduled_appt_date)
        self.referral_appt_datetime = referral.referral_appt.referral_appt_datetime
        self.referral_clinic = referral.referral_appt.community_name
        self.referral_clinic_type = referral.referral_appt.referral_clinic_type
        self.circumcised = NOT_APPLICABLE if self.gender == FEMALE else referral.circumcised
        TbSymptoms = django_apps.get_model(
            *'bcpp_subject.tbsymptoms'.split('.'))
        self.tb_symptoms = TbSymptoms.objects.get_symptoms(
            referral.subject_referral.subject_visit)
        try:
            residency_mobility_instance = ResidencyMobility.objects.get(
                subject_visit=self.subject_visit)
        except ResidencyMobility.DoesNotExist:
            self.permanent_resident = None
        else:
            self.permanent_resident = residency_mobility_instance.permanent_residen
