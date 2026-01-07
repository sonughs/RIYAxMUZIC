from pyrogram import Client

import config

from ..logging import LOGGER

# These lists are populated by Call.start() when PyTgCalls starts the assistants
assistants = []
assistantids = []


class Userbot:
    """
    Userbot class for managing assistant metadata.
    
    NOTE: In PyTgCalls 2.x, Pyrogram clients are started automatically
    by PyTgCalls.start(). This class now only provides access to
    assistant metadata after they're started by the Call class.
    """
    
    def __init__(self):
        # Clients are created and managed by Call class in call.py
        # This class is kept for backward compatibility
        pass
    
    async def start(self):
        """
        Assistants are now started by PyTgCalls in Call.start().
        This method is kept for backward compatibility.
        """
        LOGGER(__name__).info("Userbot manager initialized (clients started by PyTgCalls)")
    
    async def stop(self):
        """
        Assistants are stopped when PyTgCalls stops.
        This method is kept for backward compatibility.
        """
        LOGGER(__name__).info("Userbot manager stopped")
