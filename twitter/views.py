from pyramid.view import view_config

from twitter.models import User


@view_config(route_name='home', renderer='templates/home.pt')
def my_view(request):
    return {'project': 'twitter'}


@view_config(route_name='account', renderer='templates/account.pt')
def account_view(request):
    admin = User.get_by_username(request, 'admin')
    if admin is None:
        admin = User(username='admin', email='admin@gmail.com', password='pass', is_admin=True)
        request.db.add(admin)
        request.db.commit()
    admin = User.get_by_username(request, 'admin')
    return {'username': admin.username, 'email': admin.email}


@view_config(route_name='post_view', renderer='templates/home.pt')
def post_view(request):
    return {'project': 'twitter'}
