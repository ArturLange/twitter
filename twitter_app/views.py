from django.utils import timezone
from django.views import generic

from twitter_app.models import Post


class IndexView(generic.ListView):
    template_name = 'twitter_app/index.html'
    context_object_name = 'latest_posts_list'

    def get_queryset(self):
        return Post.objects.filter(date_created__lte=timezone.now()).order_by('-date_created')[:5]
