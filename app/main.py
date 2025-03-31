# from fastapi import FastAPI
# from app.api.routes import router

# app = FastAPI(title="Panchang API", description="Compute Hindu Panchang details")

# app.include_router(router, prefix="/api")



from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="Panchang API", description="Compute detailed Hindu Panchang")

app.include_router(router, prefix="/api")
