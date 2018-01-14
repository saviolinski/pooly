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

#
# class DocumentForm(forms.ModelForm):
#     class Meta:
#         model = Document
#
#     def __init__(self, *args, **kwargs):
#         user = kwargs.pop('user','')
#         super(DocumentForm, self).__init__(*args, **kwargs)
#         self.fields['user_defined_code']=forms.ModelChoiceField(queryset=UserDefinedCode.objects.filter(owner=user))
