from pyramid.response import Response
from pyramid.security import remember, forget
from pyramid import httpexceptions
from pyramid.view import view_config
from twitter.models import User, Post, Hashtag
from sqlalchemy.exc import IntegrityError


@view_config(route_name='home', renderer='templates/home.jinja2')
def my_view(request):
    return {'title': 'twitter'}


@view_config(route_name='account', renderer='templates/account.jinja2')
def account_view(request):
    user = User.get_by_username(request, request.authenticated_userid)
    return {'user': user}


@view_config(route_name='post_view', renderer='templates/post.jinja2')
def post_view(request):
    user = User.get_by_username(request, request.authenticated_userid)
    if request.method == "GET":
        post = request.db.query(Post).filter(Post.creator_id == user.id).first()
        return {'post': post}
    if request.method == "POST":
        post = Post(content=request.params['post_content'], creator_id=user.id)
        request.db.add(post)
        request.db.commit()
        return {'post': None}


@view_config(route_name='posts_view', renderer='templates/posts.jinja2')
def posts_view(request):
    posts = request.db.query(Post).all()
    postsusers = [(post, request.db.query(User).filter(post.creator_id == User.id).first()) for post in posts]
    return {'posts': postsusers}


@view_config(route_name='hashtag_view', renderer='templates/posts.jinja2')
def hashtag_view(request):
    hashtag = request.db.query(Hashtag).filter(Hashtag.name == 'elo').first()
    posts = Post.get_by_hashtag(request, hashtag)
    return {'posts': posts}


@view_config(route_name='login_view', renderer='templates/login.jinja2')
def login_view(request):
    if request.method == "POST":
        username = request.params['username']
        password = request.params['password']
        user = User.get_by_username(request, username)
        if user is not None and password == user.password:
            token = remember(request, username)
            return Response(headerlist=token)
        raise httpexceptions.HTTPUnauthorized()
    return {'auser': request.authenticated_userid}


@view_config(route_name='logout_view', renderer='templates/logout.jinja2')
def logout_view(request):
    if request.method == "POST":
        if request.authenticated_userid is not None:
            token = forget(request)
        return Response(headerlist=token)
    return {'auser': request.authenticated_userid}


@view_config(route_name='register_view', renderer='templates/register.jinja2')
def register_view(request):
    if request.method == "POST":
        data = request.params
        try:
            user = User(**data)
        except TypeError:
            raise httpexceptions.HTTPBadRequest()
        try:
            request.db.add(user)
            request.db.commit()
        except IntegrityError:
            raise httpexceptions.HTTPBadRequest('An account already exists for this email address.')
        return {'status': 'ok'}
    return {}
