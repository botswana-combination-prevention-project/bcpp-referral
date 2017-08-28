from django.apps import apps as django_apps
from django.db.models.aggregates import Max
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

from .data_getter import DataGetter


class ExportReferral:
    # TODO: does not work, code was taken from the subject referral model

    locator_model = 'bcpp_subject.subjectlocator'
    data_getter_cls = DataGetter

    def __init__(self, subject_visit=None):
        self.data = {}
        self.subject_visit = subject_visit
        if self.ready_to_export_transaction:
            self.data_getter = self.data_getter_cls(
                subject_visit=subject_visit)
            self.data = self.data_getter._data

    def locator_model_cls(self):
        return django_apps.get_model(self.locator_model)

    @property
    def ready_to_export_transaction(self):
        """Evaluates to True only if the instance has a referral code
        to avoid exporting referral data on someone who is not
        yet referred.

        This method is used by the model manager ExportHistoryManager.

        The assumption is that the referral instance CANNOT be created without
        an existing SubjectLocator instance.

        The subject's subject_locator instance is exported as well.

        If there is no subject_locator, the subject_referral is not exported.

        ...see_also:: SubjectReferral
        """
        export_subject_referral = False
        try:
            # check if there is a subject locator.
            # Cannot export this referral without the Subject Locator.
            subject_locator = self.locator_model_cls.objects.get(
                subject_identifier=self.subject_visit.subject_identifier)
            # check if referral is complete
            if (self.referral_code and self.referral_appt_date
                    and self.referral_clinic_type):
                try:
                    # export the subject locator
                    self.locator_model_cls.export_history.export_transaction_model.objects.get(
                        object_name=self.locator_model_cls._meta.object_name,
                        tx_pk=subject_locator.pk,
                        export_change_type='I')
                    self.locator_model_cls.export_history.serialize_to_export_transaction(
                        subject_locator, 'U', 'default', force_export=True)
                except ObjectDoesNotExist:
                    self.locator_model_cls.export_history.serialize_to_export_transaction(
                        subject_locator, 'I', 'default', force_export=True)
                except MultipleObjectsReturned:
                    self.locator_model_cls.export_history.serialize_to_export_transaction(
                        subject_locator, 'U', 'default', force_export=True)
                finally:
                    export_subject_referral = True
            else:
                # there is no referral ready yet, need to send a Delete to the
                # export tx receipient.
                # is the last transaction not a D? if not, add one.
                try:
                    aggr = self.locator_model_cls.export_history.export_transaction_model.objects.filter(
                        pk=subject_locator.pk).aggregate(Max('timestamp'), )
                    self.locator_model_cls.export_history.export_transaction_model.objects.get(
                        timestamp=aggr.get('timestamp__max'),
                        export_change_type='D')
                except self.locator_model_cls.export_history.export_transaction_model.DoesNotExist:
                    self.locator_model_cls.export_history.serialize_to_export_transaction(
                        subject_locator, 'D', None)
        except ObjectDoesNotExist:
            pass
        return export_subject_referral
