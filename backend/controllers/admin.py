# admin.py
from flask import jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from models.models import User
from .permissions import admin_required

class Dashboard(MethodView):
    decorators = [jwt_required()]

    @admin_required
    def get(self):
        data = {
            "total_users": User.query.count(),
            "active_users": User.query.filter_by(is_active=True).count(),
            "inactive_users": User.query.filter_by(is_active=False).count(),
        }
        return jsonify(data), 200
