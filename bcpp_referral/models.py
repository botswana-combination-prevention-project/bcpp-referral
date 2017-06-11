import sys

if 'tests' in sys.argv:
    from .tests.models import SubjectVisit, SubjectReferral, Circumcision, ReproductiveHealth
    from .tests.models import PimaCd4, HivCareAdherence
