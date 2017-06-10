
class Category:

    def __init__(self, name=None, routine=None, urgent=None):
        self.routine = routine or []
        self.urgent = urgent or []
        self.all = self.routine
        self.all.extend(self.urgent)


class ReferralCategory:

    def __init__(self, name=None):
        self.urgent = []
        self.routine = []
        self.category_names = []

    def add(self, name=None, urgent_referral_codes=None, routine_referral_codes=None):
        urgent_referral_codes = urgent_referral_codes or []
        routine_referral_codes = routine_referral_codes or []
        try:
            category = getattr(self, name)
        except AttributeError:
            category = Category(
                name=name,
                routine=routine_referral_codes,
                urgent=urgent_referral_codes)
            setattr(self, name, category)
            self.urgent.extend(urgent_referral_codes)
            self.routine.extend(routine_referral_codes)
            self.category_names.append(name)
