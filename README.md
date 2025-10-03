# 📌 JobTracker – Job Application & Reminder Management System

A **Django-based full-stack application** to manage job applications, track statuses, and set reminders for follow-ups.  
This project also includes **email notifications using Celery & Redis** to remind users about pending actions.  

---

## ✨ Features

- 🔎 **Job Application Tracking**
  - Save job details (role, company, job URL, platform).
  - Track application status (applied, interviewing, rejected, etc.).
  - Add notes and follow-up dates.

- ⏰ **Reminder Scheduling**
  - Set follow-up reminders.
  - Reminders are scheduled with **Celery & Redis**.
  - Auto-send emails to notify users at the scheduled time.

- 📧 **Email Notifications**
  - Email reminders via Gmail SMTP.
  - Configurable email backend.

- 💾 **Database**
  - Uses **MySQL** for persistence.
  - Supports migrations via Django ORM.

- 🖥️ **Frontend**
  - Simple **Bootstrap-based UI**.
  - Inline edit & delete for job applications.

---

## 🛠️ Tech Stack

- **Backend**: Django (DRF for APIs)
- **Database**: MySQL
- **Task Queue**: Celery
- **Broker**: Redis
- **Frontend**: Bootstrap + jQuery
- **Authentication**: JWT (via cookies)
- **Email**: Gmail SMTP

---

## ⚡ Getting Started

<!-- ### 1️⃣ Clone the repository
```bash
git clone https://github.com/../jobtracker.git
cd jobtracker

# Start Redis
redis-server

# start CELERY
celery -A jobtracker worker --loglevel=info -->

