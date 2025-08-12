# Quick Red Tech – Tech Services Website

A modern, responsive Flask web application for Quick Red Tech, offering tech services such as website/app development, database management, bug fixing, and graphic design.

## Features
- User authentication (Flask-Login)
- SQLite database (easy to switch to MySQL/PostgreSQL)
- Project submission and tracking
- Admin dashboard for managing submissions
- Responsive UI with Bootstrap 5
- Service icons (Font Awesome/Bootstrap Icons)
- Sticky navbar, footer, and mobile-friendly design

## Folder Structure
```
/quickredtech
   /static
   /templates
   app.py
   models.py
   forms.py
   requirements.txt
   config.py
```

## How to Run Locally
1. Install dependencies:
   ```
   pip install -r quickredtech/requirements.txt
   ```
2. Set environment variables (optional):
   - `SECRET_KEY` (for Flask sessions)
   - `DATABASE_URL` (if not using SQLite)
3. Run the app:
   ```
   flask --app quickredtech/app.py run
   ```
4. Visit [http://127.0.0.1:5000](http://127.0.0.1:5000)

---
All projects are completed in 62 days or less — guaranteed.
# QUICK-RED-TECH
