# Standard Library
import datetime as dt

# Third Party Library
from django import forms
from error_messages.DefaultFromErrors import DEFAULT_ERRORS
from error_messages.ValidationErrors import DEADLINE_ERROR
from todo.models import Task


class TaskForm(forms.ModelForm):
    completed = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        required=False,
        label="Завершено",
        label_suffix="",
    )

    class Meta:
        model = Task
        fields = (
            "title",
            "text",
            "deadline_date",
            "completed",
            "image",
            "priority",
            "group",
        )
        error_messages = dict.fromkeys(fields, DEFAULT_ERRORS)

    def clean_deadline_date(self):
        data = self.cleaned_data["deadline_date"].date()
        if data < dt.datetime.now().date():
            raise forms.ValidationError(DEADLINE_ERROR)
        if isinstance(data, str):
            data = dt.datetime.strptime(data, "%Y-%m-%d")
        return data
