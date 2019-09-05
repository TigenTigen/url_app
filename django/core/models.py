from django.db import models
from django.utils import timezone
from django_q.tasks import async_task, schedule
import requests
import datetime

def get_tag_content(text, tag):
    # text = pre_tag_content + open_tag + options + close_simbol + tag_content + close_tag + post_tag_content
    try:
        pre_tag_content, open_tag, text = text.partition(f'<{tag}')
        options, close_simbol, text = text.partition('>')
        if text.endswith(f'</{tag}>'):
            tag_content = text[0:len(text)-len(f'</{tag}>'):]
        else:
            tag_content, close_tag, post_tag_content = text.partition(f'</{tag}>')
        if tag_content.count('<') == 0:
            return tag_content
        else:
            pre_tag_content, open_simbol, text = tag_content.partition('<')
            tag, space, text = text.partition(' ')
            return get_tag_content(tag_content, tag)
    except:
        return None

def make_request(url_id):
    url = URL.objects.get(id = url_id)
    url.requested = timezone.now()
    r = requests.get(url.path)
    if r.status_code == 200:
        url.result = 'success'
        url.encoding = r.encoding
        url.title = get_tag_content(r.text, 'title')
        url.h1_content = get_tag_content(r.text, 'h1')
    else:
        url.result = 'status_code: {}, errors: {}'.format(r.status_code, r.reason)
    url.save()

class URL(models.Model):
    path = models.URLField('Электронный адрес страницы')
    timeshift_in_minutes = models.PositiveSmallIntegerField('Сдвиг во времени (мин)', default=0, choices=[(x, x) for x in range(60)])
    timeshift_in_seconds = models.PositiveSmallIntegerField('Сдвиг во времени (сек)', default=0, choices=[(x, x) for x in range(60)])
    added = models.DateTimeField('Дата и время добавления', auto_now_add=True)
    requested = models.DateTimeField('Дата и время запроса', null=True, blank=True)
    result = models.TextField('Статус запроса', null=True, blank=True)
    title = models.CharField('Заголовок страницы', max_length=200, null=True, blank=True)
    encoding = models.CharField('Кодировка страницы', max_length=20, null=True, blank=True)
    h1_content = models.CharField('Содержимое тега H1', max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.path)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        is_new = self._state.adding or force_insert
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)
        if is_new:
            self.delay_and_make_request()

    def total_timeshift(self):
        total_seconds = self.timeshift_in_minutes * 60 + self.timeshift_in_seconds
        if total_seconds > 0:
            return datetime.timedelta(0, total_seconds, 0)

    def delay_and_make_request(self, now = False):
        if self.total_timeshift() and not now:
            schedule('core.models.make_request', self.id, name = self.path, next_run = self.added + self.total_timeshift())
        else:
            async_task('core.models.make_request', self.id, task_name = self.path)
