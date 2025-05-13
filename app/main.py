import uvicorn
from fastapi import FastAPI
from app.api.v1 import review_endpoint
from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="API for managing product reviews and feedback",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add router with version prefix and resource
app.include_router(
    review_endpoint.router,
    prefix="/api/v1/reviews",
    tags=["reviews"]
)

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=settings.DEBUG)
