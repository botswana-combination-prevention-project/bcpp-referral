from edc_registration.models import RegisteredSubject


class ReferralDataError(Exception):
    pass


class DataHelper:

    """A class to extract model field values needed for
    the referral class.
    """

    required_keys = ['cd4_result',
                     'cd4_result_datetime',
                     'scheduled_appt_date',
                     'circumcised',
                     'pregnant']

    def __init__(self, subject_visit=None, data_updater_cls=None, **kwargs):
        self.data = {}
        self.data.update(**kwargs)
        self.data.update(subject_visit=subject_visit)
        if not self.data.get('report_datetime'):
            try:
                self.data.update(report_datetime=subject_visit.report_datetime)
            except AttributeError:
                pass
        try:
            self.data.update(
                subject_identifier=subject_visit.subject_identifier)
        except AttributeError:
            pass

        # get gender from RegisteredSubject while confirming
        # this is a known subject
        try:
            registered_subject = RegisteredSubject.objects.get(
                subject_identifier=subject_visit.subject_identifier)
        except RegisteredSubject.DoesNotExist as e:
            raise ReferralDataError(
                f'Subject is not registered. subject_identifier='
                f'\'{subject_visit.subject_identifier}\'. Got {e}')
        except AttributeError:
            pass
        else:
            self.data.update(gender=registered_subject.gender)

        if data_updater_cls:
            data_updater = data_updater_cls(**self.data)
            self.data.update(**data_updater.data)

        # ensure keys for required attrs exist
        for key in self.required_keys:
            if key not in self.data:
                self.data.update({key: None})
