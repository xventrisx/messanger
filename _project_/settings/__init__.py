from .global_settings import *
from .email_settings import *

try:
    from .local_settings import *
except ImportError:
    pass
