from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user','slug')
    search_fields = ('created_time ', 'slug', 'title')
    list_filter = ('created_time',)
    prepopulated_fields = {'slug': ('content',)}
    raw_id_fields = ('user',)


# admin.site.register(Post, PostAdmin)
