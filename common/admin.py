from django.contrib import admin

from common import models
from common.models import Subjects, Examine, Question, Assignment

admin.site.register(Subjects)
# @admin.site.register(Subjects)
admin.site.register(Examine)
admin.site.register(Question)
admin.site.register(Assignment)