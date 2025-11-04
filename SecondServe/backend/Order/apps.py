"""
AppConfig for the Order app.

- Uses BigAutoField for primary keys by default.
"""

from django.apps import AppConfig


class OrderConfig(AppConfig):
    default_auto_field = "django_mongodb_backend.fields.ObjectIdAutoField"
    name = "Order"
    verbose_name = "Order"
