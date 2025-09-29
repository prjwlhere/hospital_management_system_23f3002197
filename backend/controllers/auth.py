from flask import jsonify, request
from datetime import timedelta
from flask.views import MethodView
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)
from models.models import db, User, PatientProfile


class RegisterAPI(MethodView):
    def post(self):
        data = request.get_json() or {}
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        full_name = data.get("full_name")
        phone = data.get("phone")

        if not username or not password or not email:
            return jsonify({"error": "Missing required fields"}), 400

        # check if username or email already exists
        if User.query.filter((User.username == username) | (User.email == email)).first():
            return jsonify({"error": "User already exists"}), 400

        user = User(
            username=username,
            email=email,
            role="patient",
            full_name=full_name,
            phone=phone,
            is_active=True,
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        patient_profile = PatientProfile(user=user)
        db.session.add(patient_profile)
        db.session.commit()

        return jsonify({"message": "Patient registered successfully"}), 201


class LoginAPI(MethodView):
    def post(self):
        data = request.get_json() or {}
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"error": "Missing credentials"}), 400

        user = User.query.filter_by(username=username).first()
        if not user or not user.check_password(password):
            return jsonify({"error": "Invalid username or password"}), 401

        token = create_access_token(
            identity=str(user.id), 
            additional_claims={
                "username": user.username,
                "role": user.role,
                "full_name": user.full_name,
                "is_active": user.is_active,
            },
            expires_delta=timedelta(days=1),
        )

        return (
            jsonify(
                {
                    "access_token": token,
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "role": user.role,
                        "email": user.email,
                    },
                }
            ),
            200,
        )


class LogoutAPI(MethodView):
    # apply jwt requirement to all methods of this view
    decorators = [jwt_required()]

    def post(self):
        # For JWT stateless tokens, just instruct client to discard token.
        # If you use token revocation/blacklist, add logic here to blacklist the token.
        return jsonify({"message": "Logout successful. Discard token client-side"}), 200

class ProfileAPI(MethodView):
    # require JWT for all profile actions
    decorators = [jwt_required()]

    def get(self):
        user_id = get_jwt_identity()   # now just an int
        claims = get_jwt()             # extra fields stored in token

        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        return jsonify({
            "id": user.id,
            "username": claims.get("username", user.username),
            "email": user.email,
            "role": claims.get("role", user.role),
            "full_name": user.full_name,
            "phone": user.phone,
            "is_active": claims.get("is_active", user.is_active)
        }), 200

    def put(self):
        user_id = get_jwt_identity()   # now just an int
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        data = request.get_json() or {}

        # Only update allowable fields
        user.full_name = data.get("full_name", user.full_name)
        user.phone = data.get("phone", user.phone)
        user.email = data.get("email", user.email)

        db.session.commit()

        return jsonify({"message": "Profile updated successfully"}), 200
