# Blood Bank Management System

![developer](https://img.shields.io/badge/Developed%20By%20%3A-Minhajul%20Abedin-red)
![version](https://img.shields.io/badge/Version-2.0-blue)
![django](https://img.shields.io/badge/Django-3.0.5-green)
![python](https://img.shields.io/badge/Python-3.7+-orange)

A comprehensive web-based Blood Bank Management System designed to streamline blood donation and request processes. This system facilitates efficient management of blood inventory, donor registrations, patient requests, and automated donation confirmations.

---

## 🚀 Features (Version 2.0)

### ✨ Auto-Confirmation System

- **Automatic donation confirmation** when donors donate blood
- **No manual confirmation required** - streamlined process
- **Real-time status updates** for all stakeholders

### 🎨 Enhanced User Interface

- **Modern responsive design** with gradient backgrounds
- **Dynamic admin notifications** with color-coded alerts
- **Improved blood group selection** with dropdown interface
- **Professional footer** with developer attribution

### 📊 Advanced Dashboard Features

- **Real-time statistics** for admins, donors, and patients
- **Dynamic notification system** showing pending items
- **Color-coded alerts** (red for urgent, blue for all clear)
- **Comprehensive donation history** with detailed tracking

### 🔧 Improved Functionality

- **Enhanced blood group field** with better user experience
- **Streamlined donor request system** with auto-forwarding
- **Better error handling** and user feedback
- **Professional footer** with developer information

---

## 🎯 Core Functions

### 👨‍💼 Admin Features

- **Dashboard Overview**: View blood stock, donor count, request statistics
- **Dynamic Notifications**: Color-coded alerts for pending items
- **Donor Management**: View, update, delete donor profiles
- **Patient Management**: View, update, delete patient profiles
- **Blood Request Management**: Approve/reject blood requests
- **Donation Approval**: Review and approve blood donations
- **Stock Management**: Update blood group units manually
- **Request History**: View complete history of all requests

### 🩸 Donor Features

- **Account Registration**: Easy signup with profile management
- **Blood Donation**: Donate blood with auto-confirmation
- **Request Management**: Accept/reject blood requests from admin
- **Donation History**: View complete donation history with status
- **Blood Requests**: Request blood when needed
- **Dashboard Statistics**: View personal donation metrics
- **Auto-Confirmation**: Automatic donation confirmation for pending requests

### 🏥 Patient Features

- **Quick Registration**: No admin approval required
- **Blood Requests**: Request specific blood groups and units
- **Request Tracking**: Monitor request status (Pending/Approved/Rejected)
- **Dashboard Overview**: View personal request statistics
- **Profile Management**: Update personal information

---

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- Git (optional, for cloning)

### Step-by-Step Installation

1. **Clone or Download the Project**

   ```bash
   git clone <repository-url>
   # OR download and extract the ZIP file
   ```

2. **Navigate to Project Directory**

   ```bash
   cd bloodbankmanagement-master
   ```

3. **Create Virtual Environment (Recommended)**

   ```bash
   python -m venv env
   # On Windows
   env\Scripts\activate
   # On macOS/Linux
   source env/bin/activate
   ```

4. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

5. **Run Database Migrations**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create Superuser (Admin Account)**

   ```bash
   python manage.py createsuperuser
   ```

7. **Start Development Server**

   ```bash
   python manage.py runserver
   ```

8. **Access the Application**
   ```
   http://127.0.0.1:8000/
   ```

---

## 🎨 Key Features

### 🔄 Auto-Confirmation System

- When donors donate blood, pending requests are automatically confirmed
- Eliminates manual confirmation steps
- Streamlines the donation process

### 📊 Dynamic Admin Dashboard

- Real-time statistics and notifications
- Color-coded alerts (red for urgent items, blue for all clear)
- Comprehensive overview of system status

### 🎯 Enhanced User Experience

- Modern responsive design
- Improved form interfaces
- Better error handling and feedback
- Professional styling throughout

### 🔐 Role-Based Access

- **Admin**: Full system management capabilities
- **Donor**: Blood donation and request management
- **Patient**: Blood request and profile management

---

## 🏗️ Technology Stack

- **Backend**: Django 3.0.5
- **Database**: SQLite3
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 4
- **Icons**: Font Awesome 5
- **Styling**: Custom CSS with gradient designs

---

## 📁 Project Structure

```
bloodbankmanagement-master/
├── blood/                    # Blood management app
│   ├── models.py            # Blood request and stock models
│   ├── views.py             # Admin dashboard and blood management views
│   ├── urls.py              # Blood app URL patterns
│   └── admin.py             # Admin interface configuration
├── donor/                    # Donor management app
│   ├── models.py            # Donor and donation models
│   ├── views.py             # Donor dashboard and donation views
│   ├── forms.py             # Donation and donor forms
│   ├── urls.py              # Donor app URL patterns
│   └── admin.py             # Admin interface configuration
├── patient/                  # Patient management app
│   ├── models.py            # Patient model
│   ├── views.py             # Patient dashboard and request views
│   ├── forms.py             # Patient forms
│   ├── urls.py              # Patient app URL patterns
│   └── admin.py             # Admin interface configuration
├── bloodbankmanagement/      # Main project settings
│   ├── settings.py          # Django settings configuration
│   ├── urls.py              # Main URL patterns
│   └── wsgi.py              # WSGI configuration
├── templates/                # HTML templates
│   ├── blood/               # Blood management templates
│   ├── donor/               # Donor templates
│   ├── patient/             # Patient templates
│   └── admin/               # Admin templates
├── static/                   # Static files
│   ├── css/                 # Stylesheets
│   ├── js/                  # JavaScript files
│   ├── image/               # Images and icons
│   ├── profile_pic/         # User profile pictures
│   └── vendor/              # Third-party libraries
├── env/                      # Virtual environment
├── db.sqlite3               # Database file
├── manage.py                # Django management script
├── requirements.txt          # Python dependencies
├── README.md                # Project documentation
├── LICENSE                  # License file
└── .gitignore              # Git ignore rules
```

---

## 🚀 Quick Start Guide

### For Developers

1. **Setup Environment**

   ```bash
   python -m venv env
   env\Scripts\activate  # Windows
   source env/bin/activate  # macOS/Linux
   pip install -r requirements.txt
   ```

2. **Database Setup**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```

3. **Run Development Server**

   ```bash
   python manage.py runserver
   ```

4. **Access Application**
   - Open browser and go to: `http://127.0.0.1:8000/`
   - Admin panel: `http://127.0.0.1:8000/admin/`

### For Users

1. **Admin Access**

   - Login with superuser credentials
   - Manage donors, patients, and blood requests
   - Monitor system statistics

2. **Donor Registration**

   - Visit the homepage
   - Click "Donor Signup"
   - Complete registration form
   - Start donating blood

3. **Patient Registration**
   - Visit the homepage
   - Click "Patient Signup"
   - Complete registration form
   - Request blood when needed

---

## 🔧 Configuration

### Email Settings (Optional)

To enable email notifications, update the email settings in `bloodbankmanagement/settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

### Static Files

The project uses Django's static file handling. For production, consider using a CDN or web server for static files.

---

## 🐛 Troubleshooting

### Common Issues

1. **Database Migration Errors**

   ```bash
   python manage.py makemigrations --empty blood donor patient
   python manage.py migrate
   ```

2. **Static Files Not Loading**

   ```bash
   python manage.py collectstatic
   ```

3. **Port Already in Use**

   ```bash
   python manage.py runserver 8001
   ```

4. **Virtual Environment Issues**
   ```bash
   deactivate  # Exit current environment
   python -m venv env --clear  # Recreate environment
   ```

---

## 🤝 Contributing

This project is developed and maintained by **Minhajul Abedin**. For contributions, suggestions, or bug reports, please contact the developer.

### Development Guidelines

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Developer

**Minhajul Abedin**

- **Project**: Blood Bank Management System
- **Version**: 2.0
- **Technology**: Django, Python, HTML/CSS/JavaScript
- **Focus**: Healthcare Technology & Innovation

---

## 🙏 Acknowledgments

- Django Framework for robust web development
- Bootstrap for responsive design components
- Font Awesome for beautiful icons
- All contributors and testers

---

## 📞 Support

For support, questions, or feature requests, please contact the developer or create an issue in the repository.

**Made with ❤️ by Minhajul Abedin**
