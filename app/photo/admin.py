from django.contrib import admin
from photo.models import Category, GifArchive, Like

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(GifArchive)
class GifArchiveAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'modify_dt')

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('liker', 'gif')