# backend/controllers/permissions.py
from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, get_jwt
from models.models import User

def _get_role_and_id_from_token():
    """
    Returns tuple (user_id_or_None, role_or_None)
    """
    identity = get_jwt_identity()
    claims = get_jwt()
    user_id = None
    role = None

    # identity is expected to be the 'sub' (string or int)
    try:
        if identity is not None:
            user_id = int(identity)
    except Exception:
        user_id = None

    # role should be in claims (additional_claims)
    role = claims.get("role")
    return user_id, role

def role_required(role):
    """Restrict access to a single role."""
    def wrapper(fn):
        @wraps(fn)
        def decorated(*args, **kwargs):
            verify_jwt_in_request()
            user_id, role_in_token = _get_role_and_id_from_token()
            if role_in_token != role:
                return jsonify({"error": f"Unauthorized - {role} only"}), 403
            return fn(*args, **kwargs)
        return decorated
    return wrapper

def roles_required(roles):
    """Restrict access to multiple roles."""
    def wrapper(fn):
        @wraps(fn)
        def decorated(*args, **kwargs):
            verify_jwt_in_request()
            user_id, role_in_token = _get_role_and_id_from_token()
            if role_in_token not in roles:
                return jsonify({"error": f"Unauthorized - requires one of {roles}"}), 403
            return fn(*args, **kwargs)
        return decorated
    return wrapper

def current_user_required(fn):
    """Inject current_user model into view from JWT identity."""
    @wraps(fn)
    def decorated(*args, **kwargs):
        verify_jwt_in_request()
        user_id, role_in_token = _get_role_and_id_from_token()
        if user_id is None:
            return jsonify({"error": "Invalid token"}), 401

        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        return fn(current_user=user, *args, **kwargs)
    return decorated

# Shortcuts
def admin_required(fn):
    return role_required("admin")(fn)

def doctor_required(fn):
    return role_required("doctor")(fn)

def patient_required(fn):
    return role_required("patient")(fn)
