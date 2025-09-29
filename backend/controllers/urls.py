from flask import Blueprint
from controllers import auth , admin

main_routes = Blueprint("main_routes", __name__)

# ==== AUTH ====
# Register
main_routes.add_url_rule(
    "/api/auth/register",
    view_func=auth.RegisterAPI.as_view("auth_register"),
    methods=["POST"],
)

# Login
main_routes.add_url_rule(
    "/api/auth/login",
    view_func=auth.LoginAPI.as_view("auth_login"),
    methods=["POST"],
)

# Logout (requires JWT)
main_routes.add_url_rule(
    "/api/auth/logout",
    view_func=auth.LogoutAPI.as_view("auth_logout"),
    methods=["POST"],
)

# Profile (same URL serves GET and PUT)
main_routes.add_url_rule(
    "/api/auth/profile",
    view_func=auth.ProfileAPI.as_view("auth_profile"),
    methods=["GET", "PUT"],
)

# ==== ADMIN ====
main_routes.add_url_rule(
    "/api/admin/dashboard",
    view_func=admin.Dashboard.as_view("admin_dashboard"),
    methods=["GET"])

# ==== DOCTOR ====
# main_routes.add_url_rule("/api/doctor/dashboard", view_func=doctor.dashboard, methods=["GET"])

# ==== PATIENT ====
# main_routes.add_url_rule("/api/patient/dashboard", view_func=patient.dashboard, methods=["GET"])
