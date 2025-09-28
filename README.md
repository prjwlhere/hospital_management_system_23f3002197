# Hospital Management System - V2

The Hospital Management System (HMS) is a web application that enables hospitals to manage patients, doctors, appointments, and treatments efficiently. It provides role-based access for Admin, Doctors, and Patients to interact with the system based on their responsibilities. 

This project utilizes Flask for API development, VueJS for frontend UI, SQLite as the database, and Redis and Celery for batch jobs and caching.

## Project Structure

/hospital_management_system_23f3002197
/backend - Backend server (Flask API)
/frontend - Frontend application (VueJS)

markdown
Copy code

## Requirements

- **Backend**:
    - Flask (Python)
    - Redis
    - Celery
    - SQLite

- **Frontend**:
    - VueJS
    - Bootstrap (CSS Framework)

- **External Services**:
    - Google Chat Webhooks or SMS/Email for notifications
    - SMTP for email sending

---

## Features

### Admin (Hospital Staff)
- **Login/Logout** functionality (Admin, Doctor, Patient).
- **Dashboard**: Display total number of doctors, patients, and appointments.
- **Manage Doctors**: Add, update, and delete doctor profiles.
- **Manage Appointments**: View and manage all appointments.
- **Search functionality**: Search for patients or doctors by name/specialization.
- **Blacklist Functionality**: Remove doctors/patients from the system.

### Doctor
- **Dashboard**: Display upcoming appointments and list of assigned patients.
- **Appointment Status**: Mark appointments as completed or canceled.
- **Patient History**: View and update patient treatment history.
- **Availability**: Set availability for the next 7 days.
  
### Patient
- **Registration/Login**: Register as a new patient or login to an existing account.
- **Profile Management**: Edit personal profile.
- **Search for Doctors**: Search for doctors by specialization and availability.
- **Appointments**: Book, reschedule, or cancel appointments.
- **History**: View past appointment history, diagnoses, prescriptions, and treatment details.
  
### Backend Jobs
- **Scheduled Job**: Daily reminders to users for upcoming appointments.
- **Monthly Activity Report**: Generate a report for the doctor that includes diagnosis, treatments, and patient history.
- **CSV Export**: Export treatment details for a patient in CSV format.

### Performance & Caching
- Caching using Redis to optimize performance for frequently accessed data.
- Expiry set on cache to avoid stale data.

---

## Technologies Used

### Backend
- **Flask**: For building the REST API.
- **Redis**: Used for caching frequently requested data and session storage.
- **SQLite**: A lightweight SQL database for data storage.
- **Celery**: For scheduling background jobs (e.g., sending reminders, generating monthly reports).
  
### Frontend
- **VueJS**: For building the user interface.
- **Bootstrap**: For styling and layout.
- **Jinja2**: For embedding dynamic content into HTML templates when necessary.
  
---

## Installation

### Prerequisites
Make sure you have Python, Node.js, and SQLite installed. The following guide assumes you have a basic understanding of setting up Python and Node.js applications.

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/hospital_management_system_23f3002197.git
cd hospital_management_system_23f3002197
2. Backend Setup (Flask)
Install Dependencies
bash
Copy code
cd backend
pip install -r requirements.txt
Configure Database
The database will be created programmatically by Flask after the application runs for the first time. No manual creation is needed.

Running the Backend
bash
Copy code
python app.py
The Flask API will start on http://localhost:5000.

3. Frontend Setup (VueJS)
Install Dependencies
bash
Copy code
cd frontend
npm install
Running the Frontend
bash
Copy code
npm run serve
The VueJS frontend will be served at http://localhost:8080.

Features
Admin Features:
Admin Dashboard: Shows total doctors, patients, and appointments.

Doctor Management: Add, edit, and remove doctors.

Appointment Management: View and manage appointments.

Search: Search for doctors or patients.

Doctor Features:
Doctor Dashboard: Shows upcoming appointments and patient assignments.

Mark Appointment: Change status of appointments (Completed/Cancelled).

Patient History: Update diagnosis, treatment, and prescriptions.

Set Availability: Define availability for the upcoming week.

Patient Features:
Patient Dashboard: View doctor availability and book appointments.

Manage Appointments: View, reschedule, or cancel appointments.

Treatment History: View past treatments, diagnoses, and prescriptions.

Backend Jobs
1. Scheduled Job - Daily Reminders
Remind patients about their appointments for the day using Google Chat Webhooks, Email, or SMS.

2. Scheduled Job - Monthly Activity Report
On the first day of each month, generate a report containing the details of all appointments made during the previous month and send it to the respective doctor via email.

3. User Triggered Async Job - Export as CSV
A patient can request to download their treatment details in CSV format. This export will include details like the consulting doctor, diagnosis, treatment, and more.

Caching and Performance
Redis caching is implemented to store frequently accessed data and to avoid database overload.

Cache expiry is configured to ensure data freshness.

Additional Features (Optional)

PDF Reports: You can opt to generate PDF reports for monthly activities.

Charts: Integration of ChartJS for displaying doctor’s statistics, appointment trends, etc.

Responsive UI: The application is responsive and works seamlessly across desktop and mobile devices.

Payment Portal: A dummy payment portal view to simulate taking payment details.

Troubleshooting
1. Issues with Database Creation

Ensure that the backend/app.py file contains the correct logic to programmatically create tables. If needed, run flask db upgrade to ensure database tables are created.

2. Caching Issues

Verify that Redis is running and properly connected. You may need to check your Redis configuration and ensure the service is active.

Contributing

This is purely a personal and acedamic project