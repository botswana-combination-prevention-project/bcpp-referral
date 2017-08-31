from .constants import PENDING, NOT_REFERRED

REFERRAL_CODES = (
    (PENDING, '<data collection in progress>'),
    (NOT_REFERRED, 'Not referred'),
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

REFERRAL_CLINIC_TYPES = (
    ('ANC', 'ANC'),
    ('IDCC', 'IDCC'),
    ('SMC', 'SMC'),
    ('VCT', 'VCT'),
)
