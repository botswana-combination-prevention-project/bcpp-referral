from .referral import Referral


class ReferralViewMixin:

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.referral = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.subject_visit:
            self.referral = Referral(self.subject_visit)
        context.update(referral=self.referral)
        return context
