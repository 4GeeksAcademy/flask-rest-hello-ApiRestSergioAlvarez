import os
from flask_admin import Admin
from models import db, User, Characters, Starships, Planets, FavCharacters, FavPlanets, FavStarships
from flask_admin.contrib.sqla import ModelView


class UserModelView(ModelView):
    column_auto_select_related = True 
    column_list  = ['id','email', 'is_active', 'favorites_characters_list','favorites_starships_list', 'favorites_planets_list']

class PlanetsModelView(ModelView):
    column_auto_select_related = True
    column_list = ['id', 'name', 'population', 'galaxy', 'favorites']


class CharactersModelView(ModelView):
    column_auto_select_related = True
    column_list = ['id', 'name', 'height', 'weight', 'favorites']


class StarshipsModelView(ModelView):
    column_auto_select_related = True
    column_list = ['id', 'name', 'weight', 'passengers', 'favorites']

class FavCharactersModelView(ModelView):
    column_auto_select_related = True
    column_list = ['id', 'character_id', 'user_id', 'user', 'people']
    
class FavPlanetsModelView(ModelView):
    column_auto_select_related = True
    column_list = ['id', 'planet_id', 'user_id', 'planet', 'user']
    
class FavStarshipsModelView(ModelView):
    column_auto_select_related = True
    column_list = ['id', 'starships_id', 'user_id', 'user', 'starships_list']


def setup_admin(app):

    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(UserModelView(User, db.session))
    admin.add_view(PlanetsModelView(Planets, db.session))
    admin.add_view(CharactersModelView(Characters, db.session))
    admin.add_view(StarshipsModelView(Starships, db.session))
    admin.add_view(FavCharactersModelView(FavCharacters, db.session))
    admin.add_view(FavPlanetsModelView(FavPlanets, db.session))
    admin.add_view(FavStarshipsModelView(FavStarships, db.session))
    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))
