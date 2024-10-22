from flask import Flask, request, jsonify, session
from flask_restful import Api, Resource
from models import db, User, Recipe
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

class Signup(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        image_url = data.get('image_url', None)
        bio = data.get('bio', None)

        user = User(username=username)
        user.password = password
        
        try:
            db.session.add(user)
            db.session.commit()
            session['user_id'] = user.id
            return jsonify({
                'id': user.id,
                'username': user.username,
                'image_url': user.image_url,
                'bio': user.bio
            }), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 422

class CheckSession(Resource):
    def get(self):
        user_id = session.get('user_id')
        if user_id:
            user = User.query.get(user_id)
            return jsonify({
                'id': user.id,
                'username': user.username,
                'image_url': user.image_url,
                'bio': user.bio
            }), 200
        return jsonify({"error": "Unauthorized"}), 401

class Login(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user._password_hash, password):
            session['user_id'] = user.id
            return jsonify({
                'id': user.id,
                'username': user.username,
                'image_url': user.image_url,
                'bio': user.bio
            }), 200
        return jsonify({"error": "Unauthorized"}), 401

class Logout(Resource):
    def delete(self):
        if 'user_id' in session:
            session.pop('user_id')
            return '', 204
        return jsonify({"error": "Unauthorized"}), 401

class RecipeIndex(Resource):
    def get(self):
        if 'user_id' in session:
            recipes = Recipe.query.all()
            return jsonify([{
                'id': recipe.id,
                'title': recipe.title,
                'instructions': recipe.instructions,
                'minutes_to_complete': recipe.minutes_to_complete,
                'user': {'id': recipe.user.id, 'username': recipe.user.username}
            } for recipe in recipes]), 200
        return jsonify({"error": "Unauthorized"}), 401

    def post(self):
        if 'user_id' in session:
            data = request.get_json()
            title = data.get('title')
            instructions = data.get('instructions')
            minutes_to_complete = data.get('minutes_to_complete')

            recipe = Recipe(title=title, instructions=instructions, minutes_to_complete=minutes_to_complete, user_id=session['user_id'])
            try:
                db.session.add(recipe)
                db.session.commit()
                return jsonify({
                    'id': recipe.id,
                    'title': recipe.title,
                    'instructions': recipe.instructions,
                    'minutes_to_complete': recipe.minutes_to_complete,
                    'user': {'id': recipe.user.id, 'username': recipe.user.username}
                }), 201
            except Exception as e:
                return jsonify({"error": str(e)}), 422
        return jsonify({"error": "Unauthorized"}), 401

# Add resources to the API
api.add_resource(Signup, '/signup')
api.add_resource(CheckSession, '/check_session')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(RecipeIndex, '/recipes')

if __name__ == '__main__':
    app.run(debug=True)
