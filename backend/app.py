import os
import sys
from datetime import date, timedelta

from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

# Import models
from models.models import (
    db,
    User,
    DoctorProfile,
    PatientProfile,
    Specialization,
    DoctorAvailability,
)

# Import central blueprint (routes are defined in controllers/urls.py)
from controllers.urls import main_routes


def create_app():
    """Application factory."""
    app = Flask(__name__)

    # --- Config ---
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", "sqlite:///hmsdb.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "super-secret-key")
    app.secret_key = os.getenv("FLASK_SECRET_KEY", "secret_key_dev")

    # --- Init extensions ---
    db.init_app(app)
    Migrate(app, db)
    JWTManager(app)

    # --- Register blueprints ---
    app.register_blueprint(main_routes)

    return app


def seed_database(app, force_recreate: bool = False):
    """
    Initialize and seed the database with default admin, doctor, patient, and specializations.
    """
    with app.app_context():
        if force_recreate:
            print("⚠️  Dropping all tables...")
            db.drop_all()

        print("Creating database tables (if missing)...")
        db.create_all()

        # --- Seed admin ---
        admin_username = os.getenv("HMS_ADMIN_USERNAME", "admin")
        admin_email = os.getenv("HMS_ADMIN_EMAIL", "admin@example.com")
        admin_password = os.getenv("HMS_ADMIN_PASSWORD", "admin123")

        admin_user = User.query.filter_by(username=admin_username).first()
        if not admin_user:
            admin = User(
                username=admin_username,
                email=admin_email,
                role="admin",
                full_name="System Admin",
                is_active=True,
            )
            admin.set_password(admin_password)
            db.session.add(admin)
            db.session.commit()
            print(f"✅ Created admin user: {admin_username} / {admin_email}")
        else:
            print(f"Admin already exists: {admin_username}")

        # --- Seed specializations ---
        specs = [
            ("Cardiology", "Heart specialist"),
            ("Neurology", "Brain & nerves"),
            ("Orthopedics", "Bones & joints"),
            ("Pediatrics", "Child healthcare"),
            ("Dermatology", "Skin specialist"),
        ]
        created = 0
        for name, desc in specs:
            if not Specialization.query.filter_by(name=name).first():
                db.session.add(Specialization(name=name, description=desc))
                created += 1
        if created:
            db.session.commit()
            print(f"✅ Seeded {created} specializations")

        # --- Seed doctor ---
        if not User.query.filter_by(username="drsmith").first():
            doc_user = User(
                username="drsmith",
                email="drsmith@example.com",
                role="doctor",
                full_name="Dr. John Smith",
                phone="1234567890",
                is_active=True,
            )
            doc_user.set_password("doctor123")

            doc_profile = DoctorProfile(
                user=doc_user,
                bio="Experienced cardiologist with 10+ years in practice.",
                qualification="MBBS, MD (Cardiology)",
                consultation_fee=500,
            )

            db.session.add(doc_profile)
            db.session.commit()
            print("✅ Created sample doctor: drsmith")

            today = date.today()
            for i in range(3):
                slot = DoctorAvailability(
                    doctor=doc_profile,
                    date=today + timedelta(days=i),
                    time_slot="09:00-10:00",
                )
                db.session.add(slot)
            db.session.commit()
            print("✅ Added 3 availability slots for drsmith")
        else:
            print("Doctor drsmith already exists")

        # --- Seed patient ---
        if not User.query.filter_by(username="johndoe").first():
            patient_user = User(
                username="johndoe",
                email="johndoe@example.com",
                role="patient",
                full_name="John Doe",
                phone="9876543210",
                is_active=True,
            )
            patient_user.set_password("patient123")

            patient_profile = PatientProfile(
                user=patient_user,
                dob=date(1990, 5, 15),
                gender="Male",
                address="123 Main St, City",
                emergency_contact="Jane Doe - 9876543211",
            )
            db.session.add(patient_profile)
            db.session.commit()
            print("✅ Created sample patient: johndoe")
        else:
            print("Patient johndoe already exists")

        print("🎉 Database seeding complete.")


if __name__ == "__main__":
    # CLI interface: init-db, init-db --force
    force = False
    do_init = False

    if len(sys.argv) > 1:
        if sys.argv[1] in ("init-db", "init_db", "init"):
            do_init = True
            if len(sys.argv) > 2 and sys.argv[2] in ("--force", "-f"):
                force = True
        else:
            print("Unknown command:", sys.argv[1])
            print("Usage: python app.py [init-db|init-db --force]")
            sys.exit(1)

    app = create_app()

    if do_init:
        seed_database(app, force_recreate=force)
        sys.exit(0)

    # Run server
    port = int(os.environ.get("PORT", 5000))
    debug = True
    app.run(host="0.0.0.0", port=port, debug=debug)
