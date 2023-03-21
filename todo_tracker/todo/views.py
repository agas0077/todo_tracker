import datetime as dt
import os
import requests

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from dotenv import load_dotenv


from todo.forms import TaskForm
from todo.models import Task

load_dotenv()
DATE_FROMAT = '%Y-%m-%d'
SUCCESS_API_CATEGORY = 'funny'
SUCCESS_API_KEY = os.getenv('NINJA_API_KEY')
DEFAULT_QUOTE = [
    {
        'quote': ('I turned down "Some Like It Hot." See how smart I am? '
                  'I felt I could not bring anything funny to it. '
                  'The outfit was funny. '
                  'I do not need to compete with the wardrobe.'),
        'author': 'Jerry Lewis',
        'category': 'funny'
    }
]


def get_success_quote():
    api_url = (f'https://api.api-ninjas.com/v1/'
               f'quotes?category={SUCCESS_API_CATEGORY}')
    response = requests.get(
        api_url, headers={'X-Api-Key': SUCCESS_API_KEY}, verify=False)
    if response.status_code == requests.codes.ok:
        return response.json()[0]
    else:
        return DEFAULT_QUOTE


@method_decorator(login_required, name='dispatch')
class IndexView(ListView):
    template_name = 'todo/index.html'
    model = Task
    paginate_by = 4
    SORTING_OPTIONS = (
        ('deadline_date', 'Дедлайн - по возрастанию'),
        ('-deadline_date', 'Дедлайн - по убыванию'),
        ('create_date', 'Дата создания - по возрастанию'),
        ('-create_date', 'Дата создания - по убыванию'),
        ('title', 'Заголовок'),
        ('text', 'Текст'),
    )
    GROUP_OPTIONS = Task.Group.choices
    COMPLETED_OPTIONS = (('', 'Не завершено'), ('True', 'Завершено'), )

    def get_queryset(self):
        user = self.request.user
        self.group = self.request.GET.get('group_options', 'work')
        self.completed = self.request.GET.get('completed_options')
        queryset_filter = {
            'created_by': user,
            'group': self.group,
            'completed': bool(self.completed),
        }
        queryset = self.model.objects.filter(**queryset_filter)
        self.ordering = self.get_ordering()
        if self.ordering:
            if isinstance(self.ordering, str):
                ordering = (self.ordering,)
            queryset = queryset.order_by(*ordering)
        return queryset

    def get_ordering(self):
        ordering = self.request.GET.get('sorting_options', '-deadline_date')

        return ordering

    def get_context_data(self, *args, **kwargs):
        context = super(IndexView, self).get_context_data(*args, **kwargs)
        context['options'] = {
            'sorting_options': {
                'name': 'sorting_options',
                'label_text': 'Сортировка:',
                'options': self.SORTING_OPTIONS,
                'current_state': self.ordering,
            },
            'group_options': {
                'name': 'group_options',
                'label_text': 'Группа:',
                'options': self.GROUP_OPTIONS,
                'current_state': self.group,
            },
            'completed_options': {
                'name': 'completed_options',
                'label_text': 'Статус:',
                'options': self.COMPLETED_OPTIONS,
                'current_state': self.completed,
            },
        }
        context['action_url'] = 'todo:index'
        if self.request.method == 'GET':
            GET_params = self.request.GET.copy()
            if 'page' in GET_params:
                del GET_params['page']
            context['GET_params'] = GET_params
        return context


@login_required
def create_task(req: HttpRequest) -> HttpResponse:
    form = TaskForm(req.POST or None, files=req.FILES or None)
    template = 'todo/create_task.html'
    context = {
        'form': form,
    }

    if not req.method == 'POST' or not form.is_valid():
        return render(req, template, context)

    task = form.save(commit=False)
    task.created_by = req.user
    task.save()
    return redirect('todo:index')


@login_required
def update_task(req: HttpRequest, task_id: int) -> HttpResponse:
    task = get_object_or_404(Task, pk=task_id)
    form = TaskForm(instance=task)
    template = 'todo/update_task.html'
    context = {
        'form': form,
        'is_edit': True,
        'task_id': task_id,
    }

    if not req.method == 'POST':
        return render(req, template, context)

    if req.method == 'POST':
        post = req.POST.copy()
        # HTML doesn't return dt, but str.
        # Without conversion django |data:"Y-m-d" doesn't work
        if isinstance(post['deadline_date'], str):
            post['deadline_date'] = dt.datetime.strptime(
                post['deadline_date'], DATE_FROMAT)
        form = TaskForm(post or None, files=req.FILES, instance=task)

        if form.is_valid():
            form = form.save(commit=False)
            form.created_by = req.user
            form.save()
            if form.completed:
                return redirect('todo:congrats')
            return redirect('todo:index')
        context['form'] = form
        return render(req, template, context)


@login_required
def delete_task(req: HttpRequest, task_id: int) -> HttpResponse:
    task = get_object_or_404(Task, pk=task_id)
    if req.user == task.created_by:
        task.delete()
    return redirect('todo:index')


@login_required
def congrats(req: HttpRequest) -> HttpResponse:
    context = {
        'quote': get_success_quote(),
    }
    template = 'todo/congrats.html'
    return render(req, template, context)
