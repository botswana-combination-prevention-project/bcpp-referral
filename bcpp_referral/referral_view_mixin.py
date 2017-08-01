from .referral import Referral
from .bcpp_referral_facilities import bcpp_referral_facilities


class ReferralViewMixin:

    referral_cls = Referral

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.referral = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.subject_visit:
            self.referral = self.referral_cls(
                subject_visit=self.subject_visit,
                referral_facilities=bcpp_referral_facilities)
        context.update(referral=self.referral)
        return context
