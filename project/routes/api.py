from fastapi import APIRouter
from project.endpoints.user_auth import user_authentication
from project.endpoints.admin_auth import admin_authentication
from ..endpoints.master_data import master_data
from ..endpoints.user import user

router = APIRouter()

# --------------------Authenticatio Routing---------------------
router.include_router(user_authentication.router)


# --------------------User Routing---------------------
router.include_router(user.router)

# --------------------Admin Routing--------------------
router.include_router(admin_authentication.router)

# --------------------master data Routing--------------------
router.include_router(master_data.router)
