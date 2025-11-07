"""
WSGI config for roadhealth project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'roadhealth.settings')

application = get_wsgi_application()
