import sys

# make sure meta is in sys.modules
import meta  # NOQA

# link this module to meta
sys.modules[__name__] = sys.modules["meta"]
