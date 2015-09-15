from pyramid.view import view_config


@view_config(route_name='home', renderer='templates/home.pt')
def my_view(request):
    return {'project': 'twitter'}


@view_config(route_name='account', renderer='templates/account.pt')
def account_view(request):
    return {'project': 'elo'}
