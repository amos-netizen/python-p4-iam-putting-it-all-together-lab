from app import app, db
from models import User, Recipe

with app.app_context():
    # Create some users
    user1 = User(username='user1', image_url='http://example.com/user1.jpg', bio='User 1 bio')
    user1.password = 'password1'
    user2 = User(username='user2', image_url='http://example.com/user2.jpg', bio='User 2 bio')
    user2.password = 'password2'

    db.session.add(user1)
    db.session.add(user2)

    # Create some recipes
    recipe1 = Recipe(title='Recipe 1', instructions='Instructions for recipe 1', minutes_to_complete=30, user=user1)
    recipe2 = Recipe(title='Recipe 2', instructions='Instructions for recipe 2', minutes_to_complete=45, user=user2)

    db.session.add(recipe1)
    db.session.add(recipe2)

    db.session.commit()
