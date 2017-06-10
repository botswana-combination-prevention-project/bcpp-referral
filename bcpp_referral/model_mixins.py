from django.db import models

from .choices import REFERRAL_CODES, REFERRAL_CLINIC_TYPES


class SubjectReferralModelMixin(models.Model):

    referral_clinic = models.CharField(
        max_length=50,
        editable=False,
        help_text='The full name of the current community, e.g lentsweletau.'
    )

    gender = models.CharField(
        max_length=10,
        null=True,
        editable=False,
        help_text='M=Male, F=Female'
    )

    citizen = models.NullBooleanField(
        default=None,
        null=True,
        editable=False,
        help_text='True if citizen, False if not, None if unknown or N/A'
    )

    citizen_spouse = models.NullBooleanField(
        default=None,
        null=True,
        editable=False,
        help_text='True if citizen_spouse, False if not, None if unknown or N/A'
    )

    hiv_result = models.CharField(
        max_length=50,
        null=True,
        editable=False,
        help_text=('HIV status (POS, NEG, IND) as determined by the field RA'
                   ' either by testing or using a combination '
                   'of verbal response and documentation. None if '
                   'no result available. See also new_pos. (derived)'),
    )

    hiv_result_datetime = models.DateTimeField(
        max_length=50,
        null=True,
        editable=False,
        help_text=('HIV result datetime either from today\'s test or '
                   'documentation provided by the subject or None. '
                   'See also new_pos. (derived)'),
    )

    todays_hiv_result = models.CharField(
        max_length=50,
        null=True,
        editable=False,
        help_text=('from HIV result of test performed by the field '
                   'RA (POS, NEG, IND) or None if not performed. '
                   'The datetime of the result is hiv_result_datetime.'),
    )

    new_pos = models.NullBooleanField(
        default=None,
        null=True,
        editable=False,
        help_text=(
            'True if subject is newly diagnosed POS, false if'
            ' known positive otherwise None (derived)')
    )

    last_hiv_result = models.CharField(
        max_length=50,
        null=True,
        editable=False,
        help_text=(
            "Documented result from a participant's "
            "past record of HIV testing or valid documentation of "
            "positive status (derived)")
    )

    verbal_hiv_result = models.CharField(
        max_length=50,
        null=True,
        editable=False,
        help_text=('from HivTestingHistory.verbal_result. '
                   'HIV status as verbally provided by subject'
                   ' or None. See also '
                   ' if a positive result is supported by '
                   'direct and indirect documentation.')
    )

    direct_hiv_documentation = models.NullBooleanField(
        null=True,
        editable=False,
        help_text=('from HivTestingHistory.has_record. '
                   'True if a document was seen that confirms the subject\'s '
                   'verbally provided result, False if not, '
                   'None if unknown. See also last_hiv_result.'),
    )

    indirect_hiv_documentation = models.NullBooleanField(
        null=True,
        editable=False,
        help_text=('from HivTestingHistory.other_record and '
                   'from HivCareAdherence.arv_evidence. True if a document '
                   'was seen that suggests the subject is '
                   'HIV positive, False if not, None if unknown.'),
    )

    last_hiv_result_date = models.DateTimeField(
        null=True,
        editable=False,
        help_text=('Recorded date of previous HIV test or of the '
                   'document that provides supporting evidence of HIV '
                   'infection (derived)'),
    )

    on_art = models.NullBooleanField(
        default=None,
        null=True,
        editable=False,
        help_text=('from HivCareAdherence.on_art() method. '
                   'True if subject claims to be on ARV, False if not, None if '
                   'unknown. See also art_documentation. (derived)'),
    )

    arv_documentation = models.NullBooleanField(
        null=True,
        editable=False,
        help_text=('from HivCareAdherence.arv_evidence. True '
                   'if Field RA has seen documents that shows subject is on '
                   'ARV\'s, False if not, None if unknown. If '
                   'True, overrides HivCareAdherence.on_arv=False'),
    )

    arv_clinic = models.CharField(
        max_length=50,
        default=None,
        null=True,
        editable=False,
        help_text=("from HivCareAdherence.clinic_receiving_from. "
                   "The ARV clinic where subject currently receives care")
    )

    next_arv_clinic_appointment_date = models.DateField(
        default=None,
        null=True,
        editable=False,
        help_text=("from HivCareAdherence.next_appointment_date. "
                   "Next appointment date at the subject's ARV clinic.")
    )

    cd4_result = models.DecimalField(
        null=True,
        max_digits=6,
        decimal_places=2,
        editable=False,
        help_text=(
            'from Pima. Result of today\'s CD4 test '
            'performed in the household'),
    )

    cd4_result_datetime = models.DateTimeField(
        null=True,
        editable=False,
        help_text='from Pima. datetime CD4 drawn.',
    )

    vl_sample_drawn = models.NullBooleanField(
        default=None,
        null=True,
        editable=False,
        help_text=('from SubjectRequisition. '
                   'True if a viral load sample was drawn in the household'),
    )

    vl_sample_drawn_datetime = models.DateTimeField(
        null=True,
        editable=False,
        help_text='from SubjectRequisition. Datetime of viral load drawn.',
    )

    pregnant = models.NullBooleanField(
        default=None,
        null=True,
        editable=False,
        help_text=('from ReproductiveHealth.currently_pregnant. '
                   'True if currently pregnant, False if not, None '
                   'if unknown.'),
    )

    circumcised = models.NullBooleanField(
        default=None,
        null=True,
        editable=False,
        help_text=("from Circumcison.circumcised. True "
                   "if circumcised, False if not, None if unknown"),
    )

    part_time_resident = models.NullBooleanField(
        default=None,
        null=True,
        editable=False,
        help_text=("from eligibility checklist.part_time_resident. "
                   "True if at least a part_time resident, False if "
                   "not, None if unknown")
    )

    permanent_resident = models.NullBooleanField(
        default=None,
        null=True,
        editable=False,
        help_text=('from residence and mobility.permanent_resident.'
                   ' True if permanent resident, False if not, None '
                   'if unknown')
    )

    tb_symptoms = models.CharField(
        max_length=100,
        null=True,
        editable=False,
        help_text=('list of symptoms from tb_symptoms. Any combination of '
                   'Fever, cough, cough_blood, fever, '
                   'night_sweat, lymph_nodes, weight_loss OR None'),
    )

    urgent_referral = models.NullBooleanField(
        default=None,
        null=True,
        editable=False,
        help_text=('True if one of MASA-DF, POS!-LO, POS#-LO, POS#-PR,'
                   ' POS!-PR, otherwise None (derived)'),
    )

    referral_code = models.CharField(
        verbose_name='Referral Code',
        max_length=50,
        choices=REFERRAL_CODES,
        default='pending',
        editable=False,
        help_text=("list of referral codes confirmed by "
                   "the edc, comma delimited if more than one (derived).")
    )

    in_clinic_flag = models.BooleanField(
        default=False,
        editable=False,
        help_text=('system field. flag indicating participant was seen '
                   'in clinic (from implementer data.) '
                   'Updated by export_transaction.'),
    )

    referral_clinic_type = models.CharField(
        max_length=25,
        choices=REFERRAL_CLINIC_TYPES,
        null=True,
        editable=False,
        help_text=('The clinic type of clinic the participant is '
                   'referred to for services, (IDCC, VCT, ANC or SMC)')
    )

    class Meta:
        abstract = True
