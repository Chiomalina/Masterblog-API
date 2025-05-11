from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
CORS(app)

# Swagger UI configuration\ nSWAGGER_URL = "/api/docs"  # URL for exposing Swagger UI
SWAGGER_URL="/api/docs"
API_URL     = "/static/masterblog.json"  # Path to Swagger JSON
swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={ 'app_name': 'Masterblog API' }
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

# In-memory data store
POSTS = [
    {
        "id": 1,
        "title": "First post",
        "content": "This is the first post.",
        "author": "Chimamanda Adichie",
        "data": "2023-06-07"
    },

    { "id": 2,
      "title": "Second post",
      "content": "This is the second post.",
      "author": "Chinua Achebe",
      "data": "1999-05-25"
      }
]

# 1) List (with optional sorting)
@app.route('/api/posts', methods=['GET'])
def get_posts():
    sort_field = request.args.get('sort')
    direction  = request.args.get('direction', 'asc')

    allowed_fields     = ['title', 'content']
    allowed_directions = ['asc', 'desc']

    if sort_field and sort_field not in allowed_fields:
        return jsonify({
            'error': f"Invalid sort field '{sort_field}'. Must be 'title' or 'content'."
        }), 400

    if direction not in allowed_directions:
        return jsonify({
            'error': f"Invalid direction '{direction}'. Must be 'asc' or 'desc'."
        }), 400

    if sort_field:
        is_descending = (direction == 'desc')
        posts_list    = sorted(
            POSTS,
            key=lambda post: post[sort_field].lower(),
            reverse=is_descending
        )
    else:
        posts_list = POSTS

    return jsonify(posts_list), 200

# 2) Search
@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    title_term   = request.args.get('title', '').strip().lower()
    content_term = request.args.get('content', '').strip().lower()
    author_term = request.args.get('author', '').strip().lower()
    date_term = request.args.get('date', '').strip().lower()

    if not title_term and not content_term and not author_term and not date_term:
        return jsonify(POSTS), 200

    matching = []
    for post in POSTS:
        post_title = post['title'].lower()
        post_comment = post['content'].lower()
        post_author = post['author'].lower()
        post_date = post['date'].lower()
        if (
                (title_term and title_term in post_title)
                or (content_term and content_term in post_comment)
                or (author_term and author_term in post_author)
                or (date_term and date_term in post_date)
        ):
            matching.append(post)
    return jsonify(matching), 200

# 3) Create
@app.route('/api/posts', methods=['POST'])
def create_post():
    try:
        data = request.get_json(force=True)
    except Exception:
        return jsonify({ 'error': 'Invalid JSON body.' }), 400

    title   = data.get('title', '').strip()
    content = data.get('content', '').strip()
    author = data.get('author', '').strip()
    date = data.get('date', '').strip()
    if not title:
        return jsonify({ 'error': 'Title is required.' }), 400
    if not content:
        return jsonify({ 'error': 'Content is required.' }), 400
    if not author:
        return jsonify({ 'error': 'Author is required.' }), 400
    if not date:
        return jsonify({ 'error': 'Date is required.' }), 400

    new_id  = max((p['id'] for p in POSTS), default=0) + 1
    new_post = {
        'id': new_id,
        'title': title,
        'content': content,
        'author': author,
        'date': date,
    }
    POSTS.append(new_post)
    return jsonify(new_post), 201

# 4) Update
@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    data = request.get_json() or {}
    for post in POSTS:
        if post['id'] == post_id:
            if 'title' in data:
                post['title'] = data['title']
            if 'content' in data:
                post['content'] = data['content']
            if 'author' in data:
                post['author'] = data['author']
            if 'date' in data:
                post['date'] = data['date']
            return jsonify(post), 200
    return jsonify({ 'message': f"Post with id {post_id} not found." }), 404

# 5) Delete
@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    for post in POSTS:
        if post['id'] == post_id:
            POSTS.remove(post)
            return jsonify({ 'message': f"Post with id {post_id} has been deleted successfully." }), 200
    return jsonify({ 'message': f"Post with id {post_id} was not found." }), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
