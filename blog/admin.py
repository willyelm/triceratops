from django.contrib import admin
from blog.models import Category, Entry

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ['title']
    prepopulated_fields = {"slug":('title',)}

class EntryAdmin(admin.ModelAdmin):
    list_display = ('title','pub_date','status')
    search_fields = ['title']
    list_filter = ('pub_date','status')
    prepopulated_fields = {"slug":('title',)}
    fieldsets = (
        (None, {'fields':(('title', 'status'),'pub_date','intro_html','body_html','categories','tags','slug')}),
    )

admin.site.register(Category,CategoryAdmin)
admin.site.register(Entry,EntryAdmin)
