"""
AppConfig for the users app.

- Sets a clear verbose name for the Django admin.
- Uses BigAutoField for primary keys by default.
- Provides a ready() hook where you can import signal handlers
  (e.g., to auto-create default groups/permissions or profile rows).
"""
from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"
    verbose_name = "Users & Authentication"