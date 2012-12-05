from __future__ import absolute_import

import os
import sys

from .local import *

BUGZILLA_API_URL = BUGZILLA_BASE_URL + '/xmlrpc.cgi'
BUGZILLA_SHOW_URL = BUGZILLA_BASE_URL + '/show_bug.cgi?'
BUGZILLA_FILE_URL = BUGZILLA_BASE_URL + '/enter_bug.cgi?'
BUGZILLA_SEARCH_URL = BUGZILLA_BASE_URL + '/buglist.cgi?'

DEFAULT_LOG_LEVEL = 'DEBUG' if DEBUG else 'INFO'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'formatters': {
        'verbose': {
            'format': ('%(levelname)s %(asctime)s %(name)s %(process)d '
                       '%(thread)d %(message)s'),
        },
        'simple': {
            'format': '%(levelname)s %(asctime)s %(name)s %(message)s',
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false'],
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'stream': sys.stdout,
        },
    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'propagate': False,
            'level': 'DEBUG',
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'nose': {
            'handlers': ['null'],
            'level': 'DEBUG',
            'propagate': False,
        },
        '': {
            'handlers': ['console'],
            'level': os.environ.get('SCRUM_LOG_LEVEL', DEFAULT_LOG_LEVEL),
            'propagate': True,
        },
    }
}

if 'SENTRY_DSN' in locals():
    LOGGING['handlers']['sentry'] = {
        'level': 'ERROR',
        'class': 'raven.handlers.logging.SentryHandler',
        'dsn': SENTRY_DSN,
    }
    LOGGING['loggers']['']['handlers'].append('sentry')
