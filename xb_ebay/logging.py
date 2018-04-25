from .environ import *

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'error_log': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
        },
        'null': {
            'class': 'logging.NullHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
        },
        'django.request': {
            'handlers': ['mail_admins', 'error_log'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['mail_admins', 'error_log'],
            'level': 'ERROR',
            'propagate': False,
        },
        'py.warnings': {
            'handlers': ['console'],
        },
    }
}

# Send error logs to Slack, if not local.
if not LOCAL:
    LOGGING['handlers']['slack-error'] = {
            'level': 'ERROR',
            'api_key': SLACK_SECRET_KEY,
            'class': 'slacker_log_handler.SlackerLogHandler',
            'channel': '#xpressbuyer',
            'username': ENVIRON + ' system',
            # 'icon_url': '',
            # 'icon_emoji': '',
        }
    LOGGING['loggers']['django.request']['handlers'].append('slack-error')
    LOGGING['loggers']['django.security']['handlers'].append('slack-error')
