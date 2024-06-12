from django.contrib import admin

from .models import *

admin.site.register(User)
admin.site.register(UserCreateRequest)
admin.site.register(Type)
admin.site.register(Document)
admin.site.register(Partner)
admin.site.register(Suggestion)


class PostImageAdmin(admin.StackedInline):
    model = UniversityImage


@admin.register(University)
class PostAdmin(admin.ModelAdmin):
    inlines = [PostImageAdmin]

    class Meta:
        model = University

