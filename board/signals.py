from django.dispatch import receiver
from registration.signals import user_registered

from board.models import UserProfile


@receiver(user_registered)
def user_registered_callback(sender, user, request, **kwargs):
    profile = UserProfile(user=user)
    profile.nick = request.POST.get('nick')
    profile.save()
