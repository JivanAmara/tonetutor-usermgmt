'''
Created on Sep 9, 2016

@author: jivan
'''
from datetime import timedelta
import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

class AdCampaign(models.Model):
    code = models.CharField(max_length=8)
    description = models.CharField(max_length=300)
    name = models.CharField(max_length=20)

    def __str__(self):
        s = '{}:{}'.format(self.name, self.code)
        return s

class RegistrationCode(models.Model):
    code = models.CharField(max_length=8)
    max_users = models.IntegerField(null=True, blank=True, default=None)
    notes = models.TextField()
    unlimited_use = models.BooleanField(default=False)

    def __str__(self):
        return '{} - UserLimit: {} - Unlimited: {}'\
                   .format(self.code, self.max_users, self.unlimited_use)

class UserProfile(models.Model):
    default_color_theme = 'greys'
    user = models.OneToOneField(User, related_name='profile')
    registration_code = models.ForeignKey(
        RegistrationCode, related_name='user_profiles', null=True, blank=True
    )
    ad_campaign = models.ForeignKey(AdCampaign, null=True, blank=True)
    color_theme = models.CharField(max_length=15, default=default_color_theme)

    def color_theme_display_text(self):
        d = {
            'greys': 'Greys',
            'inverted': 'Inverted',
            'purple': 'Purple',
        }
        if self.color_theme not in d:
            self.color_theme = UserProfile.default_color_theme
        dt = d[self.color_theme]
        return dt

    @staticmethod
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            if hasattr(instance, 'registration_code'):
                rc = instance.registration_code
                if rc.code == settings.TRIAL_REGISTRATION_CODE \
                    and SubscriptionHistory.objects.filter(user=instance).count() == 0:
                    today = datetime.datetime.today()
                    SubscriptionHistory.objects.create(
                        user=instance, stripe_confirm='free', begin_date=today, end_date=today,
                        payment_amount=0
                    )
            else:
                rc = None

            ac = instance.ad_campaign if hasattr(instance, 'ad_campaign') else None

            UserProfile.objects.create(user=instance, registration_code=rc, ad_campaign=ac)

    def __str__(self):
        rc = 'None' if self.registration_code is None else self.registration_code.code
        s = '{} - RegCode: {} AdCampaign: {}'.format(self.user.username, rc, self.ad_campaign)
        return s

post_save.connect(UserProfile.create_user_profile, sender=User)

class SubscriptionHistory(models.Model):
    user = models.ForeignKey(User)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_amount = models.DecimalField(max_digits=6, decimal_places=2)
    payment_id = models.CharField(max_length=100, null=True, blank=True, default=None)
    begin_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    @classmethod
    def expires(cls, user):
        user_subscriptions = SubscriptionHistory.objects.values('end_date').filter(user=user)\
            .exclude(stripe_confirm=None).order_by('-end_date')
        if len(user_subscriptions) == 0:
            expires = datetime.date(datetime.MAXYEAR, 1, 1)
        else:
            expires = user_subscriptions[0]['end_date']

        return expires

    @classmethod
    def is_active(cls, user):
        # Returns true if the user has a subscription with an end date after today or
        #    up to 1 day before today.
        user_history = SubscriptionHistory.objects.values('end_date')\
            .filter(user=user).exclude(stripe_confirm=None).order_by('-end_date')
        dttoday = datetime.datetime.today()
        today = datetime.date(year=dttoday.year, month=dttoday.month, day=dttoday.day)
        if len(user_history) == 0:
            active = False
        elif today <= user_history[0]['end_date'] + timedelta(days=1):
            active = True
        else:
            active = False

        return active

    def __str__(self):
        s = '{}: Active: {} Expires: {}'.format(
                self.user.username, self.is_active(self.user), self.expires(self.user)
        )
        return s
