class Codes:

    def __init__(self, **options):
        self.hivind = options.get('hivind')
        self.hivneg_pregnant = options.get('hivneg_pregnant')
        self.hivneg_uncircumcised = options.get('hivneg_uncircumcised')
        self.hivunknown_pregnant = options.get('hivunknown_pregnant')
        self.hivunknown_uncircumcised = options.get('hivunknown_uncircumcised')
        self.hivuntested = options.get('hivuntested')
        self.known_hivpos_defaulter = options.get('known_hivpos_defaulter')
        self.known_hivpos_naive = options.get('known_hivpos_naive')
        self.known_hivpos_naive_high_cd4 = options.get(
            'known_hivpos_naive_high_cd4')
        self.known_hivpos_naive_low_cd4 = options.get(
            'known_hivpos_naive_low_cd4')
        self.known_hivpos_naive_pregnant = options.get(
            'known_hivpos_naive_pregnant')
        self.known_hivpos_onart = options.get('known_hivpos_onart')
        self.known_hivpos_onart_pregnant = options.get(
            'known_hivpos_onart_pregnant')
        self.new_hivpos_naive = options.get('new_hivpos_naive')
        self.new_hivpos_naive_high_cd4 = options.get(
            'new_hivpos_naive_high_cd4')
        self.new_hivpos_naive_low_cd4 = options.get('new_hivpos_naive_low_cd4')
        self.new_hivpos_pregnant = options.get('new_hivpos_pregnant')


REFERRAL_CODES = (
    ('pending', '<data collection in progress>'),
    # ('TST-CD4', 'POS any, need CD4 testing'),    # not needed
    ('TST-HIV', 'HIV test'),
    ('TST-IND', 'Indeterminate result'),

    ('MASA-CC', 'Known POS, MASA continued care'),  # viral load
    ('MASA-DF', 'Known POS, MASA defaulter (was on ART)'),
    ('SMC-NEG', 'SMC (uncircumcised, hiv neg)'),    # not needed
    # ('SMC?NEG', 'SMC (Unknown circumcision status, hiv neg'),    # not needed
    ('SMC-UNK', 'SMC (uncircumcised, hiv result not known)'),    # not needed
    ('UNK?-PR', 'HIV UNKNOWN, Pregnant'),
    ('NEG!-PR', 'NEG today, Pregnant'),    # not needed
    ('POS!-PR', 'POS today, Pregnant'),
    ('POS#-AN', 'Known POS, Pregnant, on ART (ANC)'),
    ('POS#-PR', 'Known POS, Pregnant, not on ART'),

    ('POS!-HI', 'POS today, not on ART, high CD4)'),  # not needed
    ('POS!-LO', 'POS today, not on ART, low CD4)'),  # not needed

    ('POS#-HI', 'Known POS, not on ART, high CD4)'),  # not needed

    ('POS#-LO', 'Known POS, not on ART, low CD4)'),  # not needed
    ('POS!NVE', 'POS today, not on ART/NAIVE'),
    ('POS#NVE', 'Known POS, not on ART/NAIVE'),
)
