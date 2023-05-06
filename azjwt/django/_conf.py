from django.conf import settings

AZJWT = getattr(settings, 'AZJWT', {})
REST_FRAMEWORK = getattr(AZJWT, 'REST_FRAMEWORK', {})

REST_FRAMEWORK.setdefault('REALM', 'None')
