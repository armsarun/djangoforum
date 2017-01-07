from django.contrib import admin
from .models import Profile,Post, Thread, Comment, Correctanswer
# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_of_birth', 'photo')

class PostAdmin(admin.ModelAdmin):
   readonly_fields = ('slug','create','closed_reason')
   list_display =  ('title','create')

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Post,PostAdmin)
admin.site.register(Thread)
admin.site.register(Comment)
admin.site.register(Correctanswer)
