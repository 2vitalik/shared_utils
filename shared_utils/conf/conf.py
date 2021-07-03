
# tokens:
coda_token = None
dynalist_token = None
telegram_token = None

# slack:
slack_disabled = False
slack_hooks = {}
slack_path = None
slack_multiline = False

# paths:
logs_path = None

# other:
debugging = False

timing_skip_desc = False
timing_prefix = '@'
timing_suffix = ''
timing_skip_milliseconds = False


try:
    from .local_conf import *
except ImportError:
    pass
