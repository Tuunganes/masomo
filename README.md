# Masomo School Management System

Masomo is an open‑source game‑changing school management system designed to digitalize schools in African contexts, with a pilot blueprint in Bukavu & Goma, Democratic Republic of Congo. Our mission is to equip students and teachers with digital materials, Internet access, and ICT training, bridging the educational technology gap in underserved regions.


## Features (Implemented so far)

* **Student CRUD**: Create, Read (List & Detail), Update student records via web forms.
* **Shared Layout**: Centralised `base.html` for consistent header, navigation, footer, and styling.
* **Responsive Design**: Flex-based layout with media queries for mobile-friendly navigation and sticky footer.
* **Static Asset Management**: CSS, JavaScript, and images served via Django's staticfiles.
* **SQLite Database**: Lightweight local database, migrations configured.

## Tech Stack

* **Backend**: Django 5.1.5
* **Frontend**: HTML5, Tailwind-inspired CSS (custom `styles.css`), vanilla JavaScript
* **Database**: SQLite (development)

## Getting Started

### Prerequisites

* Python 3.10+ (tested on 3.12)
* pip
* (Optional) Virtual environment tool: `venv` or `virtualenv`

### Installation

1. **Clone the repository**:

   ```bash
   git clone <your-repo-url>
   cd Masomo/masomo/backend
   ```

2. **Create & activate a virtual environment**:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install --upgrade pip
   pip install -r ../requirements.txt
   ```

4. **Configure environment variables**

   Copy `.env.example` (if provided) to `.env` and fill in secrets. We recommend keeping sensitive keys out of source control. Our `.gitignore` excludes common secrets files.

5. **Run migrations**:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Collect static files** (for production):

   ```bash
   python manage.py collectstatic --noinput
   ```

7. **Run the development server**:

   ```bash
   python manage.py runserver
   ```

8. **Access the app**: Open `http://127.0.0.1:8000/` in your browser.

## Project Structure

```
Masomo/masomo
├── backend
│   ├── manage.py
│   ├── db.sqlite3
│   ├── masomo_config
│   │   ├── settings.py
│   │   └── urls.py
│   └── students
│       ├── migrations/
│       ├── templates
│       │   ├── base.html
│       │   ├── student_list.html
│       │   ├── add_student.html
│       │   ├── student_detail.html
│       │   └── student_edit.html
│       ├── forms.py
│       ├── models.py
│       ├── urls.py
│       └── views.py
├── frontend
│   ├── css/styles.css
│   ├── js/scripts.js
│   └── templates
│       ├── index.html
│       └── Gestionduneecole.html
├── .gitignore
├── package.json
└── requirements.txt
```

## Usage

* **Home**: Landing page (`/`)
* **Étudiants**: List all students (`/student_list/`)
* **Add Student**: Add a new student (`/add_student/`)
* **Detail / Edit**: Click a name in the list to view details and edit.

## Next Steps

* **Delete** functionality with confirmation dialog
* **Authentication & Permissions** (Admin vs Staff)
* **Search, Filtering & Pagination** for student lists
* **Reports & Exports** (CSV/PDF)
* **Multi-language Support (i18n)**
* **Docker & Production Deployment**

## Contributing

Contributions welcome! Please fork the repo, create a feature branch, and open a pull request.

## License

Released under the MIT License. See `LICENSE` for details.

---

*Masomo is a project dedicated to empowering African educators and students through technology.*
