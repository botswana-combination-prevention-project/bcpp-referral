from django.core.exceptions import ObjectDoesNotExist

from edc_constants.constants import YES

from .data_helper import DataHelper


class FemaleDataHelper(DataHelper):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        try:
            reproductive_health = self.subject_visit.reproductivehealth
        except ObjectDoesNotExist:
            self.pregnant = None
        else:
            self.pregnant = (
                True if reproductive_health.currently_pregnant == YES else False)
        if not self.pregnant:
            self.pregnant = kwargs.get('pregnant')
