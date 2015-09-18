from pyramid.response import Response
from pyramid.security import remember, forget
from pyramid import httpexceptions
from pyramid.view import view_config
from twitter.models import User, Post, Hashtag
from sqlalchemy.exc import IntegrityError


def follow(request, followed):
    follower = User.get_by_username(request, request.authenticated_userid)
    followed.followers.append(follower)


def logged_in(request):
    if request.authenticated_userid is None:
        return False
    else:
        return User.get_by_username(request, request.authenticated_userid)


def retweet(request, original_post_id):
    user = User.get_by_username(request, request.authenticated_userid)
    original_post = request.db.query(Post).filter(Post.id == original_post_id).first()
    return Post(original_creator_id=original_post.original_creator_id, content=original_post.content,
                creator_id=user.id)


@view_config(route_name='home', renderer='templates/home.jinja2')
def home_view(request):
    user = User.get_by_username(request, request.authenticated_userid)
    if user is None:
        return {'logged_in': logged_in(request)}
    posts = []
    for creator in user.followed:
        posts.extend(Post.get_by_creator(request, creator))
    return {'posts': posts, 'logged_in': logged_in(request)}


@view_config(route_name='account', renderer='templates/account.jinja2')
def account_view(request):
    user = request.db.query(User).filter(User.id == request.matchdict['user_id']).first()
    if request.method == "POST" and 'follow' in request.params:
        follow(request, user)
    if request.method == "POST" and 'post_id' in request.params:
        request.db.add(retweet(request, request.params['post_id']))
        request.db.commit()
    return {'user': user, 'logged_in': logged_in(request)}


@view_config(route_name='post_view', renderer='templates/post.jinja2')
def post_view(request):
    user = User.get_by_username(request, request.authenticated_userid)
    if user is None:
        raise httpexceptions.HTTPUnauthorized()
    if request.method == "POST":
        post = Post(content=request.params['post_content'], original_creator_id=user.id)
        request.db.add(post)
        request.db.commit()
    return {'logged_in': logged_in(request)}


@view_config(route_name='posts_view', renderer='templates/posts.jinja2')
def posts_view(request):
    if request.method == "POST":
        request.db.add(retweet(request, request.params['post_id']))
    posts = request.db.query(Post).all()
    postsusers = [(post, request.db.query(User).filter(post.original_creator_id == User.id).first()) for post in posts]
    return {'posts': postsusers, 'logged_in': logged_in(request)}


@view_config(route_name='hashtag_view', renderer='templates/posts.jinja2')
def hashtag_view(request):
    if request.method == "POST":
        request.db.add(retweet(request, request.params['post_id']))
    hashtag = request.db.query(Hashtag).filter(Hashtag.name == request.matchdict['hashtag']).first()
    if hashtag is None:
        return {'logged_in': logged_in(request)}
    posts = Post.get_by_hashtag(request, hashtag)
    postsusers = [(post, request.db.query(User).filter(post.original_creator_id == User.id).first()) for post in posts]
    return {'posts': postsusers, 'logged_in': logged_in(request)}


@view_config(route_name='hashtag_list_view', renderer='templates/hashtags.jinja2')
def hashtag_list_view(request):
    hashtags = request.db.query(Hashtag).all()
    return {'hashtags': hashtags, 'logged_in': logged_in(request)}


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
    return {'auser': request.authenticated_userid, 'logged_in': logged_in(request)}


@view_config(route_name='logout_view', renderer='templates/logout.jinja2')
def logout_view(request):
    if request.method == "POST":
        if request.authenticated_userid is not None:
            token = forget(request)
        else:
            raise httpexceptions.HTTPBadRequest()
        return Response(headerlist=token)
    return {'auser': request.authenticated_userid, 'logged_in': logged_in(request)}


@view_config(route_name='register_view', renderer='templates/register.jinja2')
def register_view(request):
    if request.method == "POST":
        data = request.params
        if "" in [data['username'], data['password'], data['email']]:
            raise httpexceptions.HTTPBadRequest('Username, password or email is missing')
        try:
            user = User(**data)
        except TypeError:
            raise httpexceptions.HTTPBadRequest()
        try:
            request.db.add(user)
            request.db.commit()
        except IntegrityError:
            raise httpexceptions.HTTPBadRequest()
        return {'status': 'ok', 'logged_in': logged_in(request)}
    return {'logged_in': logged_in(request)}
