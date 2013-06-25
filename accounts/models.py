# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User



class UserProfile( models.Model ):
        user = models.ForeignKey( User, null = True )
        comment = models.CharField( max_length = 52, default = '' )


def user_post_save(sender, instance, **kwargs):
    ( profile, new ) = UserProfile.objects.get_or_create(user=instance)

models.signals.post_save.connect(user_post_save, sender=User)
