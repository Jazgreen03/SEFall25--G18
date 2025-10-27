"""
AppConfig for the Inventory app.

- Sets a clear verbose name for the Django admin.
- Uses BigAutoField for primary keys by default.
- Provides a ready() hook where you can import signal handlers
  (e.g., to auto-create default groups/permissions or profile rows).
"""

from django.apps import AppConfig


class ItemsConfig(AppConfig):
    default_auto_field = "django_mongodb_backend.fields.ObjectIdAutoField"
    name = "Item"
    verbose_name = "Item Management"

class InventoriesConfig(AppConfig):
    default_auto_field = "django_mongodb_backend.fields.ObjectIdAutoField"
    name = "Inventory"
    verbose_name = "Inventory Management"