from django.db import models
from django.utils.translation import gettext_lazy as _

class Courses(models.Model):
    STATUS = [
        (1, 'Курс находится в разработке'),
        (2, 'Курс проходит проверку'),
        (3, 'Курс полностью готов'),
        (4, 'В курс вносятся правки')
    ]


    title = models.CharField(_('Название курса'),max_length=150, unique=True, blank=False)
    tagline = models.CharField(_('Слоган курса'),max_length=150, blank=False)
    amount_tasks = models.IntegerField(_('Интерактивных заданий'), blank=False)
    video_time = models.IntegerField(_('Время видеоуроков'), blank=False)
    portfolio =  models.IntegerField(_('Работ в портфолио'), blank=False)
    author = models.CharField(_('Работ в портфолио'), max_length=150, blank=False)
    course_program = models.TextField(_('О курсе'), blank=False)
    about_course_program = models.TextField(_('О курсе'), blank=False)
    is_course_develop = models.PositiveSmallIntegerField(_('Пол'), choices=STATUS, blank=False, default=1)

class Lessons(models.Model):
     video_link = models.URLField(_('Ссылка на урок'), max_length=1000, blank=False)
     about_lesson_program = models.TextField(_('Информация об уроке'), blank=False)