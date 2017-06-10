from .data_helper import DataHelper


class MaleDataHelper(DataHelper):
    def __init__(self, circumcised=None, **kwargs):
        super().__init__(**kwargs)
        self.circumcised = circumcised
