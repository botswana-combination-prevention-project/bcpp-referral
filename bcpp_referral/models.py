from django.conf import settings

if settings.APP_NAME == 'bcpp_referral':
    from .tests.models import SubjectVisit, SubjectReferral, Circumcision
    from .tests.models import PimaCd4, HivCareAdherence, ReproductiveHealth
