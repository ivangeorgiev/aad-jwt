from enum import Enum
from django.conf import settings

class MissingUserAction(Enum):
    IGNORE = 'Ignore'
    CREATE = 'Create'

AZJWT = getattr(settings, 'AZJWT', {})

MISSING_USER_ACTION = getattr(AZJWT, 'MISSING_USER_ACTION', MissingUserAction.IGNORE)
