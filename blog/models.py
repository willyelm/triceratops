from django.db import models
from django.utils import text
from tagging.fields import TagField
from tagging.models import Tag
from datetime import datetime

class Category(models.Model):
    """
    This model defines a category that entries fall under.
    """

    title = models.CharField(max_length=150,help_text='Maximum 150 characters.')
    slug = models.SlugField(help_text='Automatically built from the title.')

    class Meta:
		ordering = ['title']
		verbose_name_plural = "categories"
		
    def __unicode__(self):
        return self.title
 
	def get_absolute_url(self):
		return "/categories/%s/" % self.slug
		
class Entry(models.Model):
    """
    This model defines a blog entry.
    """
    
    title = models.CharField(max_length=150,help_text='Maximum 150 characters.')
    slug = models.SlugField(unique_for_date='pub_date',help_text='Automatically built from the title.')
    body_html = models.TextField(blank=True)
    pub_date = models.DateTimeField('Date published.',default=datetime.now())
    categories = models.ManyToManyField(Category)
    tags = TagField();
    PUB_STATUS = (
        (0, 'Draft'),
        (1, 'Published')
    )
    status = models.IntegerField(choices=PUB_STATUS, default=0)

    class Meta:
        ordering = ('-pub_date',)
        get_latest_by = 'pub_date'
        verbose_name_plural = 'entries'
    
    def __unicode__(self):
        return u'%s' % (text.truncate_words(self.title, 30))

    def get_absolute_url(self):
        # return a permalink
        return "/%s/%s/" % (self.pub_date.strftime("%Y/%b/%d").lower(), self.slug)

    def get_previous_published(self):
        # only get Entry objects which are marked as published
        return self.get_previous_by_pub_date(status__exact=1)

    def get_next_published(self):
        return self.get_next_by_pub_date(status__exact=1)

    def get_tags(self):
        return Tag.objects.get_for_object(self)
