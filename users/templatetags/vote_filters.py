from django import template
from meetings.models.vote import VoteChoice
from meetings.models.vote import Vote

register = template.Library()

@register.filter
def yes_count(votes):
    if votes is None:
        return 0
    return votes.filter(choice=VoteChoice.YES).count()

@register.filter
def no_count(votes):
    if votes is None:
        return 0
    return votes.filter(choice=VoteChoice.NO).count()

@register.filter
def abstain_count(votes):
    if votes is None:
        return 0
    return votes.filter(choice=VoteChoice.ABSTAIN).count()
