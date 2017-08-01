class MockCurrent:

    def __init__(self, declined=None, **kwargs):
        self.declined = declined

    def __repr__(self):
        return f'{self.__class__.__name__}({self.__dict__})'


class MockStatusHelper:

    def __init__(self, final_hiv_status=None, final_arv_status=None,
                 indeterminate=None, declined=None,
                 newly_diagnosed=None, **kwargs):
        self.current = MockCurrent(declined=declined)
        self.final_hiv_status = final_hiv_status
        self.final_arv_status = final_arv_status
        self.indeterminate = indeterminate
        self.newly_diagnosed = newly_diagnosed

    def __repr__(self):
        return f'{self.__class__.__name__}({self.__dict__})'
