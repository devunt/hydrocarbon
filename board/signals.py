from django.contrib.sessions.models import Session
from django.dispatch import receiver
from account.signals import email_confirmation_sent, user_signed_up


@receiver(email_confirmation_sent)
def email_confirmation_sent_callback(sender, confirmation, **kwargs):
    user = confirmation.email_address.user
    # Logout user
    [s.delete() for s in Session.objects.all() if s.get_decoded().get('_auth_user_id') == user.id]


@receiver(user_signed_up)
def user_signed_up_callback(sender, user, form, **kwargs):
    user.is_active = True
    user.save()
