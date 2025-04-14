from fastapi import FastAPI
from app.routes import candidate, admin, panelist
from app.database import Base, engine
import uvicorn
import logging
import sys

# Simple direct logging configuration
logging.basicConfig(
    level=logging.DEBUG,  # Set to DEBUG to see all messages
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stdout  # Force output to stdout
)

# Get logger
logger = logging.getLogger(__name__)

# Log startup information
logger.info("Starting application...")

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Log router inclusion
logger.info("Including routers...")
app.include_router(candidate.router)
app.include_router(admin.router)
app.include_router(panelist.router)
logger.info("All routers included successfully")



if __name__ == "__main__":
    logger.info("Starting uvicorn server...")
    uvicorn.run(app, host="127.0.0.1", port=8005)
