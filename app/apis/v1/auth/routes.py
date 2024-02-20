from fastapi import APIRouter

import app.apis.v1.auth.login.end_point as login
import app.apis.v1.auth.logout.end_point as logout
import app.apis.v1.auth.registration.end_point as registration

auth_api_router = APIRouter()
auth_api_router.include_router(registration.router, tags=["Authentication"])
auth_api_router.include_router(login.router, tags=["Authentication"])
auth_api_router.include_router(logout.router, tags=["Authentication"])
