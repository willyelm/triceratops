from datetime import datetime, date
#from tagging.models import Tag,TaggedItem
from blog.models import Entry, Category
from syncr.twitter.models import Tweet
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.utils import simplejson
from django.core.paginator import Paginator
import re

def ajax_return(request):
    return HttpResponse(
        simplejson.dumps(request, indent=2, ensure_ascii=False),
        content_type = 'application/javascript; charset=utf8'
    )

def get_items(start_date=datetime(1900,1,1,0,0,0), end_date=datetime.now()):
    results = list()
    
    entries = Entry.objects.filter(pub_date__range=(start_date, end_date)).filter(status=1)
    for entry in entries: 
        results.append({'type':'entry', 'entry':entry, 'datetime':entry.pub_date})

    tweets = Tweet.objects.filter(pub_time__range=(start_date, end_date))
    hash_regex = re.compile(r'#[0-9a-zA-Z+_]*',re.IGNORECASE) 
    user_regex = re.compile(r'@[0-9a-zA-Z+_]*',re.IGNORECASE)
    for tweet in tweets:
        body = tweet.text
        # change URLs to proper html formatted links
        body = re.sub('http://[^ ,]*', lambda t: "<a href=\"%s\">%s</a>" % (t.group(0), t.group(0)), body)
        # change @user references to links
        for usr in user_regex.finditer(body):
            url_user = usr.group(0).replace('@','')
            body = body.replace(usr.group(0), '<a href="http://twitter.com/'+url_user+'" title="'+usr.group(0)+'">'+usr.group(0)+'</a>')
        # change #hashtags to links
        for hashtag in hash_regex.finditer(body):
            url_hash = hashtag.group(0).replace("#",'%23')
            if len(hashtag.group(0)) > 2: body = body.replace(hashtag.group(0),'<a href="http://search.twitter.com/search?q='+url_hash+'" title="'+hashtag.group(0)+'">'+hashtag.group(0)+'</a>')
        results.append({'type':'tweet', 'tweet':body, 'user':tweet.user.screen_name, 'datetime':tweet.pub_time})

    results = sorted(results, key=lambda x: x['datetime'], reverse=True)
    return results
    
def index(request):
    return render_to_response('blog/index.html', {'object_list':get_items()})

def view_published_entries(request):
    return render_to_response('blog/entry_list.html', {'object_list':Entry.objects.filter(status=1)[:5]})

def entry(request, slug):
    return render_to_response('blog/entry.html', {'object':get_object_or_404(Entry, slug=slug)})  

def archive(request):
    arch = Entry.objects.dates('pub_date', 'month', order='DESC')
    archives = {}
    for i in arch:
        year = i.year
        month = i.month
        try:
            archives[year][month-1][1] = True
        except KeyError:
            archives[year]=[[date(year,month,1),False] for month in xrange(1,13)]
            archives[year][month-1][1] = True
    return render_to_response('blog/archive.html', {'archives':sorted(archives.items(),reverse=True)})  

def archive_month(request, year, month):
    return render_to_response('blog/index.html', {'object_list':get_items(datetime(int(year),int(month),1,0,0,0),datetime(int(year),int(month),31,0,0,0))})

def archive_year(request, year):
    return render_to_response('blog/index.html', {'object_list':get_items(datetime(int(year),1,1,0,0,0),datetime(int(year)+1,1,1,0,0,0))})
