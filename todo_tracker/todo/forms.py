import datetime as dt

from django import forms

from todo.models import Task

my_default_errors = {
    'required': 'Это обязательное поле!',
    'invalid': 'Ввдеите правильное значение!'
}


class TaskForm(forms.ModelForm):
    completed = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input'}),
        required=False,
        label='Завершено',
        label_suffix='')

    class Meta:
        model = Task
        fields = ('title', 'text', 'deadline_date', 'completed', 'image', )
        error_messages = dict.fromkeys(fields, my_default_errors)

    def clean_deadline_date(self):
        data = self.cleaned_data['deadline_date']
        if data.date() < dt.datetime.now().date():
            raise forms.ValidationError('Дата дедлайна не может быть в прошлом.')
        return data