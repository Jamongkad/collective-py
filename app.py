import web

from movie import Raters, Movie, RatersPreference, Rating, UserRole, Role, db_session
from mongo_movie import collection

import form
import formencode
from formencode import htmlfill

from view import render

import algos

from validation import validate

urls = (
    '/login', 'login',
    '/logout', 'logout',
    '/dashboard', 'dashboard',
    '/', 'index', 
    '/add_movie', 'add_movie',
    '/raters', 'raters',
    '/movies/([0-9]+)', 'movies',
    '/compare/([A-Za-z0-9]+)/([A-za-z0-9]+)', 'compare',
    '/test', 'test'
)

app = web.application(urls, globals(), autoreload=True)
session = web.session.Session(app, web.session.DiskStore('sessions'),
                              initializer={'loggedIn':False})

def session_hook():
    web.ctx.session = session

app.add_processor(web.loadhook(session_hook))

def protect(role=[]):
    def check_meth(meth):
        def check_login(self, *args, **kwa):
            check = web.ctx.session.get('loggedIn')
            role_check = web.ctx.session.get('role')
            if check is False:
                raise web.seeother('/login')
            elif not role:
                return meth(self, *args, **kwa)
            elif role_check not in role:
                referer = web.ctx.env.get("HTTP_REFERER")
                raise web.seeother(referer)
            else:
                return meth(self, *args, **kwa)
        return check_login
    return check_meth

class login:
    def GET(self):
        return render('auth.html')

    @validate(schema=form.LoginForm(), html='auth.html')
    def POST(self):
        i = web.input()        
        check = db_session.query(Raters, Role, UserRole)\
                          .filter(Raters.name==i.username)\
                          .filter(UserRole.rater_id==Raters.id)\
                          .filter(UserRole.role_id==Role.id)\
                          .first()
        if check != None:
            web.ctx.session.username = i.username
            web.ctx.session.role = check.Role.role_name
            web.ctx.session.loggedIn = True
            return web.seeother('/dashboard')

        return 'something went awry!'

class logout():
    def GET(self):
        web.ctx.session.kill()
        return web.redirect('/login')

class dashboard:
 
    @protect()
    def GET(self):
        return render('dashboard.html')
    
    @validate(schema=form.DashboardForm(), html="dashboard.html")
    def POST(self): 
        return web.input()

class index:
    @protect()
    def GET(self):
        movies = db_session.query(Movie).order_by(Movie.id.desc()).all()
        return render('index.html', movies=movies) 

class raters:
    @protect()
    def GET(self):
        user_raters = db_session.query(Raters).all()
        return render('raters.html', raters=user_raters)

def movie_prefs(person_id):
    return db_session.query(Rating, Movie)\
                     .filter(Rating.rater_id==person_id)\
                     .filter(Rating.movie_id==Movie.id).all() 

def mongo_movie_prefs(name):
    return collection.scores.find_one({'name' : name.capitalize()})['prefs']

class movies:
    @protect()
    def GET(self, id):
        user = db_session.query(Raters).filter(Raters.id==id).first().name
        user_movies = movie_prefs(id) 
        return render('movies.html', user_movies=user_movies, user=user)

class compare:
    def GET(self, person1, person2):
        values = algos.sim_pearson(mongo_movie_prefs, person1, person2)
        return render('compare.html', values=values)
               
class add_movie:
    def POST(self):
        i = web.input()
        db_session.add(Movie(i.movie_name))
        db_session.commit()
        return web.seeother('/')

class test:
    @protect()
    def GET(self):
        return web.ctx.env.get("HTTP_REFERER")

if __name__ == '__main__':
    app.run()
