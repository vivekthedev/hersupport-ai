### Prerequisites
- Python 3.8+
- pip (Python package installer)

### Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/vivekthedev/hersupport-ai
    cd hersupport-ai
    ```

2. **Create a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the Django application:**

    - **Migrate the database:**
      ```bash
      python manage.py migrate
      ```

    - **Create a superuser (admin account):**
      ```bash
      python manage.py createsuperuser
      ```

5. **Run the application:**
    ```bash
    python manage.py runserver
    ```

6. Visit `http://127.0.0.1:8000` in your browser to view the application.
