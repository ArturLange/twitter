from django.shortcuts import render
from django.utils import timezone
from django.views import generic

from twitter_app.models import Post, User


class IndexView(generic.ListView):
    template_name = 'twitter_app/index.html'
    context_object_name = 'latest_posts_list'

    def get_queryset(self):
        return Post.objects.filter(date_created__lte=timezone.now()).order_by('-date_created')[:20]


class UserProfileView(generic.DetailView):
    template_name = 'twitter_app/profile.html'

    def get(self, request, pk):
        user = User.objects.get(id=pk)
        posts = Post.objects.get_by_user_id(user.id)
        context = {'user_profile': user, 'posts': posts}
        return render(request, self.template_name, context)
