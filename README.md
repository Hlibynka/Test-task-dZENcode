# SPA Comments System

A Single Page Application (SPA) for a cascading comments system, built with Django (Backend) and Vue.js (Frontend). This project fully satisfies the requirements including real-time updates, background processing, caching, and JWT authentication.

## Features

* **Cascading Comments:** Endless replies to comments with a clean, indented UI.
* **Sorting & Pagination:** Sort by Date (LIFO/FIFO), User Name, and Email. Paginated at 25 comments per page.
* **Media Attachments:** Upload images (auto-resized if > 320x240, formats: JPG, PNG, GIF) and TXT files (up to 100KB).
* **Visual Effects:** Built-in Lightbox effect for viewing attached images.
* **Security:**
  * XSS & SQL Injection protection.
  * Allowed XHTML tags only (`<a>`, `<code>`, `<i>`, `<strong>`).
  * CAPTCHA validation on the backend.
* **Real-time Updates (WebSockets):** New comments appear instantly for all connected users without page reloads (powered by Django Channels & Redis).
* **Background Processing (Queue):** Heavy tasks (mocked) are handled asynchronously by Celery workers.
* **Caching:** Read-heavy API endpoints are cached via Redis to reduce database load.
* **JWT Authentication:** Admin panel implementation. Only authenticated users with a valid JWT token can post comments, while guests have read-only access.

##  Tech Stack

* **Backend:** Python, Django, Django REST Framework, Django Channels (WebSockets)
* **Frontend:** Vue.js 3, Axios
* **Database:** PostgreSQL
* **Infrastructure:** Docker, Docker Compose, Redis, Celery, Daphne (ASGI)

##  Quick Start

To run this project locally, you need Docker and Docker Compose installed.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Hlibynka/Test-task-dZENcode

```cd <repository-folder>```
   
2. **Build and start the containers:**
    ```bash
   docker-compose up -d --build
   
3. **DB migration**
    ```bash
   docker-compose exec web python manage.py migrate

4. **make user**
    ```bash
   docker-compose exec web python manage.py createsuperuser

Set up your username and passwrd

## Access to app

* **Front:** ```http://localhost:5173```
* **Back:** ```http://localhost:8000/api/comments/```
* **Admin panel:** ```http://localhost:8000/admin/```

## Additional

* JWT is hidden by default. Use your superuser data for the top login panel to log in and get your token
* New message make window go to the place of it appearing with highlight animation on every window(even other user)]
* Background task is there only for imitation some kind of hard process (checking, analizys whatever) Check the docker logs to see background tasks executing after a comment is posted.
```bash
docker-compose logs -f celery