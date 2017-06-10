from edc_registration.models import RegisteredSubject

from .options_updater import OptionsUpdater


class ReferralDataError(Exception):
    pass


class DataHelper:

    """A class to extract model field values needed for
    the referral class.
    """

    options_updater_cls = OptionsUpdater

    def __init__(self, subject_visit=None, **options):
        self.subject_visit = subject_visit
        self.subject_identifier = subject_visit.subject_identifier

        # get gender from RegisteredSubject while confirming
        # this is a known subject
        try:
            registered_subject = RegisteredSubject.objects.get(
                subject_identifier=self.subject_identifier)
        except RegisteredSubject.DoesNotExist as e:
            raise ReferralDataError(
                f'Subject is not registered. subject_identifier='
                f'\'{self.subject_identifier}\'. Got {e}')
        self.gender = registered_subject.gender

        # update custom options from model values
        updated = self.options_updater_cls(
            subject_visit=subject_visit, options=options)
        self.options = updated.options

        # ensure keys for required attrs exist
        for key in ['cd4_result', 'cd4_result_datetime', 'scheduled_appt_date']:
            if key not in options:
                options.update({key: None})

        # set all options as self instance attrs
        for k, v in updated.options.items():
            setattr(self, k, v)
