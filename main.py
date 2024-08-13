import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from app.routes.employee import router as employee_routes
# from app.utils.config import get_settings

app = FastAPI(
    title="minimal fastapi keycloak template",
    version="0.0.0",
    openapi_url="/openapi.json",
    docs_url="/docs",
)

app.include_router(employee_routes, prefix='/v1')

# Sets all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Guards against HTTP Host Header attacks
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1"],
)

if __name__ == "__main__":
    uvicorn.run(host="0.0.0.0", port=8000, app=app)