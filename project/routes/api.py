from fastapi import APIRouter
from project.endpoints.user_auth import user_authentication
from project.endpoints.admin_auth import admin_authentication
from ..endpoints.master_data import master_data
<<<<<<< HEAD
from ..endpoints.tickets_request import tickets_request
from ..endpoints.user import user
from ..endpoints.notifications import notifications
=======
from ..endpoints.user import user
>>>>>>> 4ff072eea4bf3d9e21bdfa50534e18dd866d673d

router = APIRouter()

# --------------------Authenticatio Routing---------------------
router.include_router(user_authentication.router)


# --------------------User Routing---------------------
router.include_router(user.router)

<<<<<<< HEAD
#--------------------User Routing---------------------
router.include_router(tickets_request.router)



# --------------------Admin Routing--------------------
router.include_router(admin_authentication.router)

#---------------------notifications---------------------
router.include_router(notifications.router)

=======
# --------------------Admin Routing--------------------
router.include_router(admin_authentication.router)

>>>>>>> 4ff072eea4bf3d9e21bdfa50534e18dd866d673d
# --------------------master data Routing--------------------
router.include_router(master_data.router)
