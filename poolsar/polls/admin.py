from django.contrib.admin import TabularInline, ModelAdmin
from django.contrib import admin

from .models import Question, Choice


class ChoiceInline(TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        # ('Slug', {'fields': ['slug'], 'classes': ['collapse']}),
        (None, {'fields': ['user']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'timestamp', 'was_published_recently')
    list_filter = ['timestamp']
    search_fields = ['question_text']

    class Meta:
        model = Question

class ChoiceAdmin(ModelAdmin):
    list_display = ('choice_text', 'question', 'votes')
    search_fields = ['choice_text', 'question']

    class Meta:
        model = Choice


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)

