from django.contrib.auth.hashers import make_password

from board.models import OneTimeUser


def account_delete_mark(deletion):
    pass


def account_delete_expunge(deletion):
    user = deletion.user
    ot_user = OneTimeUser()
    ot_user.nick = user.nickname
    # Make unusable password
    ot_user.password = make_password(None)
    ot_user.save()
    user.posts.all().update(onetime_user=ot_user)
    user.comments.all().update(onetime_user=ot_user)
    user.delete()
