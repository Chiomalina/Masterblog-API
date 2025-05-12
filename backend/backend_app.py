import json
import os

from flask import Flask, abort, jsonify, render_template, request
from flask_cors import CORS


# Configuration constants
DATA_FILE = os.path.join(os.path.dirname(__file__), 'posts.json')

# Initialize Flask app with absolute template/static paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')

app = Flask(
    __name__,
    template_folder=TEMPLATE_DIR,
    static_folder=STATIC_DIR,
)
CORS(app)


# Persistence helpers

def load_posts():
    """
    Load and return the list of posts from the JSON data file.
    If the file is missing or invalid, return an empty list.
    """
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as fileobject:
            return json.load(fileobject)
    except (IOError, json.JSONDecodeError):
        return []


def save_posts(posts):
    """
    Save the list of posts to the JSON data file.
    Abort with 500 on failure.
    """
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as fileobject:
            json.dump(posts, fileobject, indent=2)
    except IOError:
        abort(500, description='Failed to write data file.')


# Frontend route


@app.route('/', methods=['GET'])
def home():
    """Serve the main HTML page."""
    return render_template('index.html')


# API endpoints


@app.route('/api/posts', methods=['GET'])
def get_posts():
    """
    List posts, optionally sorted by title or content in asc/desc order.
    Query params:
      - sort: 'title' or 'content'
      - direction: 'asc' (default) or 'desc'
    """
    posts = load_posts()
    sort_field = request.args.get('sort')
    direction = request.args.get('direction', 'asc').lower()

    valid_fields = {'title', 'content'}
    valid_directions = {'asc', 'desc'}

    if sort_field and sort_field not in valid_fields:
        return (
            jsonify(
                {'error': f"Invalid sort field '{sort_field}'."
                          " Must be 'title' or 'content'."}
            ),
            400,
        )

    if direction not in valid_directions:
        return (
            jsonify(
                {'error': f"Invalid direction '{direction}'."
                          " Must be 'asc' or 'desc'."}
            ),
            400,
        )

    if sort_field:
        reverse = direction == 'desc'
        posts = sorted(
            posts,
            key=lambda post: post[sort_field].lower(),
            reverse=reverse,
        )

    return jsonify(posts), 200


@app.route('/api/posts', methods=['POST'])
def create_post():
    """
    Create a new post. Required JSON fields: title, content, author, date.
    Returns the created post with status 201.
    """
    data = request.get_json(force=True) or {}

    title = data.get('title', '').strip()
    content = data.get('content', '').strip()
    author = data.get('author', '').strip()
    date_ = data.get('date', '').strip()

    if not title:
        abort(400, description='Title is required.')
    if not content:
        abort(400, description='Content is required.')
    if not author:
        abort(400, description='Author is required.')
    if not date_:
        abort(400, description='Date is required.')

    posts = load_posts()
    new_id = max((post['id'] for post in posts), default=0) + 1

    new_post = {
        'id': new_id,
        'title': title,
        'content': content,
        'author': author,
        'date': date_,
    }
    posts.append(new_post)
    save_posts(posts)

    return jsonify(new_post), 201


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """Delete a post by its ID. Returns 200 on success or 404 if not found."""
    posts = load_posts()
    for post in posts:
        if post['id'] == post_id:
            posts.remove(post)
            save_posts(posts)
            return (
                jsonify(
                    {'message':
                     f"Post with id {post_id} has been deleted successfully."}
                ),
                200,
            )

    return (
        jsonify({'error': f'Post with id {post_id} was not found.'}),
        404,
    )


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    """
    Update an existing post by ID. Fields title, content, author, date are optional.
    Returns the updated post or 404 if not found.
    """
    data = request.get_json(force=True) or {}
    posts = load_posts()

    for post in posts:
        if post['id'] == post_id:
            if 'title' in data:
                post['title'] = data['title'].strip()
            if 'content' in data:
                post['content'] = data['content'].strip()
            if 'author' in data:
                post['author'] = data['author'].strip()
            if 'date' in data:
                post['date'] = data['date'].strip()
            save_posts(posts)
            return jsonify(post), 200

    return (
        jsonify({'error': f'Post with id {post_id} not found.'}),
        404,
    )


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    """
    Search posts by title, content, author, or date. All query params are optional.
    Returns posts that match any provided filter.
    """
    title_term = request.args.get('title', '').strip().lower()
    content_term = request.args.get('content', '').strip().lower()
    author_term = request.args.get('author', '').strip().lower()
    date_term = request.args.get('date', '').strip().lower()

    posts = load_posts()
    if not any((title_term, content_term, author_term, date_term)):
        return jsonify(posts), 200

    matching = []
    for post in posts:
        if (
            (title_term and title_term in post['title'].lower())
            or (content_term and content_term in post['content'].lower())
            or (author_term and author_term in post['author'].lower())
            or (date_term and date_term in post['date'].lower())
        ):
            matching.append(post)

    return jsonify(matching), 200


if __name__ == '__main__':
    # Ensure the data file exists
    if not os.path.isfile(DATA_FILE):
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)
    app.run(host='0.0.0.0', port=5002, debug=True)
