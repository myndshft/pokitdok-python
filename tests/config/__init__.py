import importlib
import sys
import os
from ast import literal_eval


def pre_check_config(conf):
    new_globals = dict()
    for key in conf.keys():
        if key in os.environ and os.environ.get(key) is not None and os.environ.get(key) != "":
            try:
                new_globals[key] = literal_eval(os.environ.get(key))
            except:
                new_globals[key] = os.environ.get(key)
        else:
            new_globals[key] = conf.get(key)
    globals().update(new_globals)

# store your client id and client secret in config/local.py
# for production apps, change to DEFAULT
default_mod = 'tests.config.local'
cfg = importlib.import_module(default_mod)
pre_check_config(cfg.__dict__)


def from_module(mod=None):
    """
    load configuration properties from a module, overriding defaults
    :param mod:
    :return:
    """
    if not mod:
        return
    sys.stdout.write('Loading environment variables from the ' + mod + ' configuration\n')
    mod = 'tests.config.' + mod
    cfg = importlib.import_module(mod)
    pre_check_config(cfg.__dict__)


# for production apps, change to DEFAULT
env = os.environ.get('APP_ENV', 'LOCAL')
try:
    if env != 'LOCAL':
        from_module(env.lower())
    else:
        try:
            from_module(env.lower())
        except:
            # If there is not local config file, just...
            pass
    sys.stdout.write('Running with ' + env.lower() + ' configuration\n')
except:
    #TODO: What alerting should be done here in deployed environments?
    import traceback
    traceback.print_exc()

