from shared_utils.conf import conf


def debugging_function(func):
    def wrapped(self, *args, **kwargs):
        if conf.debugging:
            return func(self, *args, **kwargs)
    return wrapped
