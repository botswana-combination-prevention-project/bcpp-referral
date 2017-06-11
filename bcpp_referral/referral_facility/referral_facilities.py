
class ReferralFacilityDuplicateCode(Exception):
    pass


class ReferralFacilityAlreadyRegistered(Exception):
    pass


class ReferralFacilityNotFound(Exception):
    pass


class ReferralFacilities:

    """A named collection of referral facility instances.
    """

    def __init__(self, name=None):
        self._register = {}
        self.name = name  # e.g. community / map_area

    def __repr__(self):
        return f'{self.__class__.__name__}(name={self.name})'

    def __str__(self):
        return self.name

    @property
    def facilities(self):
        return self._register

    def get_facility(self, referral_code=None):
        """Returns the facility for this referral code.
        """
        for facility in self._register.values():
            if referral_code in facility.all_codes:
                return facility
        raise ReferralFacilityNotFound(
            f'Referral facility not found. Got referral '
            f'code \'{referral_code}\'. See {repr(self)}')

    def add_facility(self, facility=None):
        """Adds a new facility.
        """
        if facility.name in self._register:
            raise ReferralFacilityAlreadyRegistered(f'Got {facility}')
        dups = [code for code in facility.all_codes if code in self.all_codes]
        if dups:
            raise ReferralFacilityDuplicateCode(f'Code(s) already in use. Got {dups}')
        self._register.update({facility.name: facility})

    @property
    def urgent_codes(self):
        """Returns a list of urgent referral codes.
        """
        codes = []
        [codes.extend(facility.urgent_codes)
         for facility in self._register.values()]
        return codes

    @property
    def routine_codes(self):
        """Returns a list of routine referral codes.
        """
        codes = []
        [codes.extend(facility.routine_codes)
         for facility in self._register.values()]
        return codes

    @property
    def all_codes(self):
        """Returns a list of all referral codes.
        """
        codes = []
        [codes.extend(facility.all_codes)
         for facility in self._register.values()]
        return codes
