from django import forms
from events.models import Event

class EventForm(forms.ModelForm):
    """
    A simple form for creating a new event, which is a simple description
    field and that is it.
    """
    description = forms.CharField(max_length=340, widget=forms.Textarea)

    class Meta:
        model = Event
        fields = ('description',)