from django.core.management.utils import get_random_secret_key
from django.utils.encoding import force_str

key = get_random_secret_key()

print(force_str(key))