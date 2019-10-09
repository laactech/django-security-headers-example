import os
import sys

from django.core.wsgi import get_wsgi_application

# This allows easy placement of apps within the interior directory
app_path = os.path.dirname(os.path.abspath(__file__)).replace("/config", "")
sys.path.append(os.path.join(app_path, "django_security_headers_example"))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.base")

application = get_wsgi_application()
