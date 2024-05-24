### Setup

1. **Clone the repository**:

    ```bash
    git clone https://github.com/LOKESHLOKI07/data_pusher.git
    cd data_pusher
    cd data_pusher
    pip install -r requirements.txt 
    ```

2 **Apply migrations**:

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

3. **Create a superuser**:

    ```bash
    python manage.py createsuperuser
    ```

4. **Run the development server**:

    ```bash
    python manage.py runserver
    ```

5. **Access the admin interface**:

    Open a web browser and go to `http://127.0.0.1:8000/admin/`
