from django.contrib import admin
from votes.models import Category, Vote, Choice, CastVote

admin.site.register(Category)
admin.site.register(Vote)
admin.site.register(Choice)
admin.site.register(CastVote)
