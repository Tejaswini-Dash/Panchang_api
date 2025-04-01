<<<<<<< HEAD
from fastapi import FastAPI
from .api.routes import router

app = FastAPI()

# Include the router for Panchang API
app.include_router(router)
=======
# from fastapi import FastAPI
# from app.api.routes import router

# app = FastAPI(title="Panchang API", description="Compute Hindu Panchang details")

# app.include_router(router, prefix="/api")



from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="Panchang API", description="Compute detailed Hindu Panchang")

app.include_router(router, prefix="/api")
>>>>>>> b8a42b75d440e17b91f20f3edc6ef857bd7e3483
