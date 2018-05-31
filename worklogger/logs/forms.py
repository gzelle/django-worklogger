from django import forms

from .models import Log


class DateInput(forms.DateInput):
    input_type = 'date'


class LogForm(forms.ModelForm):
    class Meta:
        model = Log
        fields = ('duration', 'project', 'log_date')
        widgets = {
            'log_date': DateInput()
        }
