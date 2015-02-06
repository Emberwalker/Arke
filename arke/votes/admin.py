from django.contrib import admin
from votes.models import Vote, Choice, CastVote

admin.site.register(Vote)
admin.site.register(Choice)
admin.site.register(CastVote)
