from django.conf import settings

if settings.APP_NAME == 'bcpp_referral':
    from .tests import models
