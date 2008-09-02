from django import template

def person(user):
    return {'user': user}

register = template.Library()
register.inclusion_tag('profile/person.html')(person)
