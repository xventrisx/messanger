from channels.routing import ProtocolTypeRouter, URLRouter

from chats.middlewares import TokenAuthMiddlewareStack
from chats.routing import web_socket

application = ProtocolTypeRouter({"websocket": TokenAuthMiddlewareStack(web_socket)})
