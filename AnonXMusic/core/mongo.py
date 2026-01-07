from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_DB_URI
from ..logging import LOGGER
import asyncio

logger = LOGGER(__name__)
logger.info("Connecting to your Mongo Database...")

# Ensure URI is set
if not MONGO_DB_URI:
    logger.error("MONGO_DB_URI is not set in your environment variables!")
    exit()

try:
    # Create client and get DB instance
    _mongo_async_ = AsyncIOMotorClient(MONGO_DB_URI)
    mongodb = _mongo_async_.Lassi

    # Test connection by pinging the DB
    async def test_connection():
        await _mongo_async_.admin.command("ping")

    asyncio.get_event_loop().run_until_complete(test_connection())
    logger.info("Connected to your Mongo Database.")
except Exception as e:
    logger.error(f"Failed to connect to your Mongo Database. Reason: {e}")
    exit()
