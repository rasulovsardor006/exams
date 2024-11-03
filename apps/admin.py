from django.contrib import admin
from .models import User, Subject, Examine, Question


class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'role', 'is_verified', 'is_active')
    search_fields = ('name', 'email')
    list_filter = ('role', 'is_verified', 'is_active')

class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    search_fields = ('name',)
    list_filter = ('user',)

class ExamAdmin(admin.ModelAdmin):
    list_display = ('subject', 'user', 'start_time', 'end_time', 'duration')
    search_fields = ('subject__name', 'user__name')
    list_filter = ('subject', 'user')

@admin.register(Question)
class QuestionsAdmin(admin.ModelAdmin):
    pass

admin.site.register(User, UserAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Examine, ExamAdmin)
