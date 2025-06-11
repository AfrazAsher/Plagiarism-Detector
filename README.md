# Plagiarism-Detector

# 🏫 Academic Management System

A Django-powered Academic Management System designed to streamline the teaching-learning process for schools, colleges, or universities. It allows **teachers** to manage courses and assignments, **students** to submit work, and integrates a **plagiarism detection** system for academic integrity.

---

## ✨ Features

### 🔐 Authentication & Authorization

- User registration and login (students and teachers)
- Role-based redirection to dashboards
- Secure session management with Django’s built-in auth

### 👨‍🏫 Teacher Functionality

- Create, update, delete courses
- Create, edit, delete assignments with attachments
- Add students to courses
- View assignment submissions from students
- Detect plagiarism in student submissions
- Generate assignment plagiarism reports

### 👨‍🎓 Student Functionality

- Dashboard showing enrolled courses and assignments
- Upload assignment submissions
- View uploaded files
- View course-wise assignment listings

### 📑 Plagiarism Detection

- Jaccard similarity-based plagiarism checking
- Compare assignment submissions against each other
- View plagiarism percentages and marks deductions

---

## 🧩 Tech Stack

- **Backend:** Django (Python)
- **Database:** SQLite (default), can be changed to PostgreSQL/MySQL
- **Frontend:** HTML, CSS, Bootstrap (via Django templates)
- **Storage:** Django default storage system for file handling

---

## 🧪 How Plagiarism Detection Works

When a teacher runs plagiarism checks:

- All student submissions for an assignment are read.
- Pairwise comparison is performed using a similarity algorithm (e.g., Jaccard).
- A percentage score is calculated indicating overlap.
- Marks are deducted based on detected plagiarism.

> ⚠️ Files are read directly using Django’s storage path, and the results are shown via a rendered report.

---

## 📸 System Design Overview

### Use Case Diagram

![Use Case Diagram](/diagrams/use_case_diagram.png)

### Site Map

![Site Map](/diagrams/site_map.png)

### Component Workflow

![Workflow](/diagrams/combined_sequence_diagram.png)

---

## 🚀 Getting Started

Install python 3.9.18
Install vs Code or any other text editor of your choose

#### Setting up a virtual environment

First, create a virtual environment to isolate your project dependencies:

```bash
python -m venv pd
```

#### Activating the virtual environment

Activate the virtual environment using the command below:

- On Windows:

  ```bash
  pd\Scripts\activate
  ```

- On MacOS/Linux:

  ```bash
  source pd/bin/activate
  ```

#### Installing dependencies

Install all the required libraries using the following command:

```bash
pip install -r requirements.txt
```

#### Go To plagiarism_detector

```
cd plagiarism_detector
```

#### Migrations

```
python manage.py makemigrations
```

```
python manage.py migrate
```

### Running the Application

Now you can run the application using:

```
python manage.py runserver
```
