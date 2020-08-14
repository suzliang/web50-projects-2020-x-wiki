from django.db import models
from django import forms
from django.forms import ModelForm, Textarea
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Entry(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()

class New(ModelForm):
    class Meta:
        model = Entry
        fields = '__all__'
        widgets = {
            'content': Textarea(attrs={'rows':20, 'cols':100}),
        }
        labels = {
            'title': _('Title'),
            'content': _('Content'),
        }
        help_texts = {
            'content': _('Markdown'),
        }