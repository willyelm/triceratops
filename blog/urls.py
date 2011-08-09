from django.conf.urls.defaults import *
#from django.views.generic.date_based import archive_index
#from django.views.generic import list_detail
#from blog.models import Entry

urlpatterns = patterns('blog.views',
   #(r'^$', list_detail.object_list, {'queryset': Entry.objects.filter(status=1)}),
   #(r'^$', 'blog.views.view_published_entries'),
   (r'^$', 'index'),
   (r'^archive[/]', 'archive'),
   (r'^(?P<year>\d{4})/(?P<month>\d{2})[/]', 'archive_month'),
   (r'^(?P<year>\d{4})[/]', 'archive_year'),
   (r'^(?P<slug>[a-zA-Z0-9\-]+)[/]', 'entry'),
)
