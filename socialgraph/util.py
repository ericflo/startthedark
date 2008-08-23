from django.contrib.auth.models import User
from socialgraph.models import UserLink

def get_people_user_follows(user):
    ul = UserLink.objects.filter(from_user=user).values('to_user')
    return User.objects.filter(id__in=[i['to_user'] for i in ul])

def get_people_following_user(user):
    ul = UserLink.objects.filter(to_user=user).values('from_user')
    return User.objects.filter(id__in=[i['from_user'] for i in ul])

def get_mutual_followers(user):
    follows = UserLink.objects.filter(from_user=user).values('to_user')
    following = UserLink.objects.filter(to_user=user).values('from_user')
    follows_set = set([i['to_user'] for i in follows])
    following_set = set([i['from_user'] for i in following])
    return User.objects.filter(id__in=follows_set.intersection(following_set))