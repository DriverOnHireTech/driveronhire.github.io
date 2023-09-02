"""
ASGI config for base_site project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import booking.routing


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "base_site.settings")

# application = get_asgi_application()
application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            booking.routing.websocket_urlpatterns
        )
    ),

})
