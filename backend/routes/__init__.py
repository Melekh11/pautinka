"""
This module initializes and imports the API route modules for the application.

The following routers are imported and can be included in the main FastAPI application:
- auth_router: Handles authentication-related routes such as login and registration.
- user_router: Handles user-related routes such as fetching user details and updating user information.
- review_router: Handles work review-related routes such as creating and fetching work reviews.
"""
from .auth_routes import auth_router
from .user_routes import user_router
from .review_routes import review_router
