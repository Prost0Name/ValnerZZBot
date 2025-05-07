from .channel import channel_router
from .private import private_router

def register_routers(dp):
    dp.include_router(channel_router)
    dp.include_router(private_router) 