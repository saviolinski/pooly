from django.forms import ModelForm, Form
from django import forms
from .models import Question, Choice

class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = [
            "question_text",
        ]

    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.fields['choice'] = forms.CharField(max_length=80)


class ChoiceForm(ModelForm):
    class Meta:
        model = Choice
        fields = [
            "choice_text",
        ]
