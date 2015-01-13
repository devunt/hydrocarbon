from django.contrib.sessions.models import Session
from django.dispatch import receiver
from django.utils.translation import ugettext as _
from account.signals import email_confirmation_sent, user_signed_up

from board.models import Board, Notification
from board.utils import treedict


@receiver(email_confirmation_sent)
def email_confirmation_sent_callback(sender, confirmation, **kwargs):
    user = confirmation.email_address.user
    # Logout user
    [s.delete() for s in Session.objects.all() if s.get_decoded().get('_auth_user_id') == user.id]


@receiver(user_signed_up)
def user_signed_up_callback(sender, user, form, **kwargs):
    user.is_active = True
    user.save()
    ndata = treedict()
    ndata['type'] = 'SITE_ANNOUNCEMENT'
    ndata['message']  = _('New site announcement')
    ndata['text'] = _('Welcome to herocomics! We strongly recommend you read the announcements.')
    ndata['url'] = Board.objects.get(slug='notice').get_absolute_url()
    Notification.create(None, user, data)
