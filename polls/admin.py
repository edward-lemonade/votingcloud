from django.contrib import admin

# Register your models here.
from .models import Choice, Question, User, Vote

class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 2

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pDate'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInLine]
    list_display = ('question_text', 'pDate', 'was_published_recently')
    list_filter = ['pDate']
    search_fields = ['question_text']

admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(User)
admin.site.register(Vote)
