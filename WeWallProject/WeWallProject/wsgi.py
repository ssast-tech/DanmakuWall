"""
WSGI config for WeWallProject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os

#18.3.27
#import sys
#path = '/home/WewallProject'

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WeWallProject.settings")

application = get_wsgi_application()
