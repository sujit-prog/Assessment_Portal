"""
WSGI config for quiz_app project.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz_app.settings')

application = get_wsgi_application()

# Vercel requires this
app = application