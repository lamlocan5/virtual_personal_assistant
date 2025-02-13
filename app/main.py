from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging.config
import yaml
from pathlib import Path

# Initialize logging
logging.config.fileConfig('config/logging.conf')
logger = logging.getLogger('app')

# Load configuration
config_path = Path('config/config.yaml')
with config_path.open() as f:
    config = yaml.safe_load(f)

app = FastAPI(
    title="Virtual Personal Assistant",
    description="Multi-Agent System for Personal Assistance",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import routers
from app.routers import qa, image, speech, management

# Include routers
app.include_router(qa.router, prefix="/qa", tags=["Question Answering"])
app.include_router(image.router, prefix="/image", tags=["Image Processing"])
app.include_router(speech.router, prefix="/speech", tags=["Speech Processing"])
app.include_router(management.router, prefix="/manage", tags=["Personal Management"])

@app.get("/")
async def root():
    return {"message": "Virtual Personal Assistant API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=config['api']['host'], port=config['api']['port'])