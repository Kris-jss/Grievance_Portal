# 🎓 Grievance Management & Redressal System

A web-based complaint management portal built with Django, designed for colleges to handle student grievances efficiently and confidentially.

## 📋 Overview

This system provides a safe platform for students to report issues like ragging, harassment, faculty misconduct, infrastructure problems, and other concerns. Admins can manage, respond to, and track all complaints through a centralized dashboard.

## ✨ Features

### 👨‍🎓 Student Portal
- **User Registration & Authentication** - Secure login system with role-based access
- **Submit Complaints** - Choose from 6 categories (Ragging, Harassment, Faculty Issues, Student Misconduct, Infrastructure, Other)
- **Upload Evidence** - Attach images or PDF documents to support complaints
- **Track Status** - Real-time status updates (Pending, In Progress, Resolved, Escalated, Dismissed)
- **View Responses** - Read admin responses and follow-up messages
- **Complaint History** - Access all submitted complaints with detailed timeline
- **Animated Dashboard** - Visual statistics with smooth counting animations
- **Delete Complaints** - Remove complaints if submitted by mistake

### 👨‍💼 Admin Portal
- **Comprehensive Dashboard** - Overview of all complaints with statistics
- **Advanced Filtering** - Filter by status (All, Pending, In Progress, Resolved, Escalated, Archived)
- **Respond to Complaints** - Add responses visible to students
- **Update Status** - Change complaint status to track progress
- **Archive System** - Move resolved complaints to archive (student history preserved)
- **Delete from View** - Remove complaints from admin view (student still sees it)
- **Student Information** - Access reporter details for communication
- **Response History** - View all previous admin responses

### 🎨 Design Features
- **Responsive Layout** - Works seamlessly on desktop, tablet, and mobile
- **Modern UI** - Professional gradient themes and animations
- **Custom Typography** - Google Fonts (Poppins & Inter) for readability
- **Bootstrap 5** - Clean, accessible interface
- **Bootstrap Icons** - Visual indicators throughout
- **Animated Statistics** - Counting animations on dashboard cards
- **Modal Popups** - Smooth interactions for forms and confirmations

### 🔒 Security & Privacy
- **Confidential Complaints** - Only admins can view complaint details
- **Auto-generated IDs** - Unique tracking IDs (e.g., GRV-2025-001)
- **CSRF Protection** - Django's built-in security
- **Login Required** - Protected routes with authentication decorators
- **IST Timezone** - Indian Standard Time for all timestamps

## 🛠️ Tech Stack

- **Backend:** Django 5.x (Python)
- **Frontend:** HTML5, CSS3, Bootstrap 5
- **Database:** SQLite3
- **Icons:** Bootstrap Icons
- **Fonts:** Google Fonts (Poppins, Inter)
- **File Handling:** Pillow for image uploads

## 📥 Installation

### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone the repository**
```bash
git clone https://github.com/Kris-jss/Grievance_Portal.git
cd Grievance_Portal
```

2. **Create virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install django pillow
```

4. **Run migrations**
```bash
python manage.py migrate
```

5. **Create superuser (admin account)**
```bash
python manage.py createsuperuser
```

6. **Set user role to admin**
```bash
python manage.py shell
```

**Python**
```
from accounts.models import User
admin = User.objects.get(username='your_username')
admin.role = 'admin'
admin.save()
exit()
```

7. **Run development server**
```bash
python manage.py runserver
```

8. **Access the application**
- Homepage: http://127.0.0.1:8000/
- Admin Panel: http://127.0.0.1:8000/admin/


# 👨‍💻 Author:
- Built as an intermediate-level Django project for learning purposes.

# 📄 License:
- MIT License


