from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class TimestampMixin:
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True)



class User(db.Model, TimestampMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'admin' | 'doctor' | 'patient'
    full_name = db.Column(db.String(120))
    phone = db.Column(db.String(30))
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    blacklisted = db.Column(db.Boolean, default=False, nullable=False)

    doctor_profile = db.relationship("DoctorProfile", back_populates="user", uselist=False, cascade="all,delete")
    patient_profile = db.relationship("PatientProfile", back_populates="user", uselist=False, cascade="all,delete")
    export_jobs = db.relationship("ExportJob", back_populates="user")

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username} role={self.role}>"


class DoctorProfile(db.Model, TimestampMixin):
    __tablename__ = "doctor_profiles"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    bio = db.Column(db.Text)
    qualification = db.Column(db.Text)
    consultation_fee = db.Column(db.Integer, nullable=True)

    user = db.relationship("User", back_populates="doctor_profile")
    specializations = db.relationship("DoctorSpecialization", back_populates="doctor", cascade="all,delete")
    availability = db.relationship("DoctorAvailability", back_populates="doctor", cascade="all,delete")
    appointments = db.relationship("Appointment", back_populates="doctor", cascade="all,delete")
    monthly_reports = db.relationship("MonthlyReport", back_populates="doctor", cascade="all,delete")
    treatments = db.relationship("Treatment", back_populates="doctor", cascade="all,delete")

    def __repr__(self):
        return f"<DoctorProfile user_id={self.user_id}>"


class PatientProfile(db.Model, TimestampMixin):
    __tablename__ = "patient_profiles"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    dob = db.Column(db.Date, nullable=True)
    gender = db.Column(db.String(20), nullable=True)
    address = db.Column(db.Text, nullable=True)
    emergency_contact = db.Column(db.String(120), nullable=True)

    user = db.relationship("User", back_populates="patient_profile")
    appointments = db.relationship("Appointment", back_populates="patient", cascade="all,delete")

    def __repr__(self):
        return f"<PatientProfile user_id={self.user_id}>"


class Specialization(db.Model, TimestampMixin):
    __tablename__ = "specializations"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)

    doctors = db.relationship("DoctorSpecialization", back_populates="specialization", cascade="all,delete")

    def __repr__(self):
        return f"<Specialization {self.name}>"


class DoctorSpecialization(db.Model):
    __tablename__ = "doctor_specializations"
    __table_args__ = (db.UniqueConstraint("doctor_id", "specialization_id", name="uq_doctor_specialization"),)

    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctor_profiles.id", ondelete="CASCADE"), nullable=False)
    specialization_id = db.Column(db.Integer, db.ForeignKey("specializations.id", ondelete="CASCADE"), nullable=False)

    doctor = db.relationship("DoctorProfile", back_populates="specializations")
    specialization = db.relationship("Specialization", back_populates="doctors")

    def __repr__(self):
        return f"<DoctorSpecialization doctor_id={self.doctor_id} spec_id={self.specialization_id}>"


class DoctorAvailability(db.Model, TimestampMixin):
    __tablename__ = "doctor_availability"
    __table_args__ = (db.UniqueConstraint("doctor_id", "date", "time_slot", name="uq_doc_date_slot"),)

    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctor_profiles.id", ondelete="CASCADE"), nullable=False, index=True)
    date = db.Column(db.Date, nullable=False, index=True)
    time_slot = db.Column(db.String(50), nullable=False)  # e.g. '09:00-09:30'
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    doctor = db.relationship("DoctorProfile", back_populates="availability")
    appointment = db.relationship("Appointment", back_populates="availability", uselist=False)

    def __repr__(self):
        return f"<DoctorAvailability doc={self.doctor_id} date={self.date} slot={self.time_slot}>"


class Appointment(db.Model, TimestampMixin):
    __tablename__ = "appointments"
    __table_args__ = (db.UniqueConstraint("doctor_id", "date", "time_slot", name="uq_appointment_doc_date_slot"),)

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patient_profiles.id", ondelete="CASCADE"), nullable=False, index=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctor_profiles.id", ondelete="CASCADE"), nullable=False, index=True)
    availability_id = db.Column(db.Integer, db.ForeignKey("doctor_availability.id", ondelete="SET NULL"), nullable=True)
    date = db.Column(db.Date, nullable=False)
    time_slot = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(30), nullable=False, default="booked")
    reason = db.Column(db.Text, nullable=True) 

    patient = db.relationship("PatientProfile", back_populates="appointments")
    doctor = db.relationship("DoctorProfile", back_populates="appointments")
    availability = db.relationship("DoctorAvailability", back_populates="appointment")
    treatments = db.relationship("Treatment", back_populates="appointment", cascade="all,delete")
    status_history = db.relationship("AppointmentStatusHistory", back_populates="appointment", cascade="all,delete")

    def __repr__(self):
        return f"<Appointment id={self.id} doctor={self.doctor_id} patient={self.patient_id} date={self.date} slot={self.time_slot}>"


class AppointmentStatusHistory(db.Model):
    __tablename__ = "appointment_status_history"

    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey("appointments.id", ondelete="CASCADE"), nullable=False, index=True)
    old_status = db.Column(db.String(30))
    new_status = db.Column(db.String(30))
    changed_by_user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    note = db.Column(db.Text, nullable=True)
    changed_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    appointment = db.relationship("Appointment", back_populates="status_history")
    changed_by = db.relationship("User", foreign_keys=[changed_by_user_id])

    def __repr__(self):
        return f"<AppointmentStatusHistory appt={self.appointment_id} {self.old_status}->{self.new_status}>"


class Treatment(db.Model, TimestampMixin):
    __tablename__ = "treatments"

    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey("appointments.id", ondelete="CASCADE"), nullable=False, index=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctor_profiles.id"), nullable=False, index=True)
    diagnosis = db.Column(db.Text, nullable=True)
    prescription = db.Column(db.Text, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    followup_date = db.Column(db.Date, nullable=True)

    appointment = db.relationship("Appointment", back_populates="treatments")
    doctor = db.relationship("DoctorProfile", back_populates="treatments")

    def __repr__(self):
        return f"<Treatment id={self.id} appt={self.appointment_id} doctor={self.doctor_id}>"


class ExportJob(db.Model, TimestampMixin):
    __tablename__ = "export_jobs"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    job_type = db.Column(db.String(50), nullable=False)  # 'treatment_export', 'appointments_export', etc.
    status = db.Column(db.String(30), nullable=False, default="pending")
    file_path = db.Column(db.Text, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)

    user = db.relationship("User", back_populates="export_jobs")

    def __repr__(self):
        return f"<ExportJob id={self.id} user={self.user_id} status={self.status}>"


class MonthlyReport(db.Model, TimestampMixin):
    __tablename__ = "monthly_reports"
    __table_args__ = (db.UniqueConstraint("doctor_id", "month", "year", name="uq_report_doctor_month_year"),)

    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctor_profiles.id", ondelete="CASCADE"), nullable=False, index=True)
    month = db.Column(db.Integer, nullable=False)  # 1..12
    year = db.Column(db.Integer, nullable=False)
    report_path = db.Column(db.Text, nullable=True)

    doctor = db.relationship("DoctorProfile", back_populates="monthly_reports")

    def __repr__(self):
        return f"<MonthlyReport doctor={self.doctor_id} {self.month}/{self.year}>"


class Notification(db.Model, TimestampMixin):
    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True, index=True)
    type = db.Column(db.String(50), nullable=False)  # 'reminder','export_ready','report_sent', etc.
    payload = db.Column(db.Text, nullable=True)  # JSON text message or payload
    is_read = db.Column(db.Boolean, default=False, nullable=False)

    user = db.relationship("User")

    def __repr__(self):
        return f"<Notification id={self.id} user={self.user_id} type={self.type}>"
