from django.core.exceptions import ObjectDoesNotExist


class OptionsUpdater:
    """Update options from model field values using reverse
    relations on SubjectVisit.

    PimaCd4, HivCareAdherence, SubjectReferral
    """

    def __init__(self, subject_visit=None, options=None):
        self.subject_visit = subject_visit
        if not options.get('cd4_result'):
            try:
                options.update(cd4_result=subject_visit.pimacd4.result_value)
            except ObjectDoesNotExist:
                pass
        if not options.get('cd4_result_datetime'):
            try:
                options.update(
                    cd4_result_datetime=subject_visit.pimacd4.result_datetime)
            except ObjectDoesNotExist:
                pass
        if not options.get('scheduled_appt_date'):
            try:
                options.update(
                    scheduled_appt_date=subject_visit.hivcareadherence.next_appointment_date)
            except ObjectDoesNotExist:
                pass
        if not options.get('scheduled_appt_date'):
            try:
                options.update(
                    scheduled_appt_date=subject_visit.subjectreferral.scheduled_appt_date)
            except ObjectDoesNotExist:
                pass
        self.options = options
