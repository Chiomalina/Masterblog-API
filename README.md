# Masterblog API

A simple Flask-based blog API with file-based persistence using JSON. This project demonstrates CRUD operations, search, sorting, and serves a static front-end from the same application.

## Features

* **Persistent Storage**: Stores posts in `posts.json` to survive server restarts.
* **CRUD Endpoints**:

  * **Create**: `POST /api/posts` to add a new post.
  * **Read**: `GET /api/posts` to list posts with optional sorting.
  * **Update**: `PUT /api/posts/<id>` to modify an existing post.
  * **Delete**: `DELETE /api/posts/<id>` to remove a post.
* **Search**: `GET /api/posts/search` with query parameters (`title`, `content`, `author`, `date`).
* **Sorting**: `GET /api/posts?sort=<field>&direction=<asc|desc>`.
* **Static Front-End**: Serves `index.html`, `main.js`, and `style.css` under `templates/` and `static/`.
* **CORS Enabled**: Allows cross-origin requests if needed.

## Project Structure

```
├── app.py             # Main Flask application
├── posts.json         # Data store (auto-created)
├── templates/
│   └── index.html     # Front-end HTML
└── static/
    ├── main.js        # Front-end JavaScript
    └── style.css      # Front-end CSS
```

## Getting Started

### Prerequisites

* Python 3.8 or higher
* `pip` package manager

### Installation

1. **Clone the repository**:

   ```bash
   git clone <repository_url>
   cd <repository_folder>
   ```

2. **Create and activate a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate      # macOS/Linux
   venv\Scripts\activate       # Windows
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize data file** (optional):

   ```bash
   echo "[]" > posts.json
   ```

### Running the Application

```bash
python app.py
```

By default, the server runs on `http://0.0.0.0:5002/`. Navigate to this URL to view the front-end.

## API Documentation

### List Posts

```
GET /api/posts
```

* **Query Parameters (optional)**:

  * `sort`: `title` or `content`
  * `direction`: `asc` (default) or `desc`

* **Response**: `200 OK`

```json
[
  {
    "id": 1,
    "title": "First post",
    "content": "This is the first post.",
    "author": "Alice",
    "date": "2025-05-12"
  }
]
```

### Create Post

```
POST /api/posts
```

* **Body (JSON)**:

  * `title` (string, required)
  * `content` (string, required)
  * `author` (string, required)
  * `date` (string, required)

* **Response**: `201 Created`

```json
{
  "id": 3,
  "title": "New Post",
  "content": "Content here",
  "author": "Bob",
  "date": "2025-05-13"
}
```

### Update Post

```
PUT /api/posts/<id>
```

* **Body (JSON)**: Any of `title`, `content`, `author`, `date` (optional)

* **Response**: `200 OK` or `404 Not Found`

```json
{
  "id": 3,
  "title": "Updated Title",
  "content": "Updated content.",
  "author": "Bob",
  "date": "2025-05-13"
}
```

### Delete Post

```
DELETE /api/posts/<id>
```

* **Response**: `200 OK` or `404 Not Found`

```json
{ "message": "Post with id 3 has been deleted successfully." }
```

### Search Posts

```
GET /api/posts/search?title=<term>&content=<term>&author=<term>&date=<term>
```

* **All parameters optional**; returns posts matching any filter.
* **Response**: `200 OK`

```json
[ { "id": 2, "title": "Flask Tips"} ]
```

## License

This project is released under the MIT License.
