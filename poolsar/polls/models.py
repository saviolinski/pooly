import datetime
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify


class Question(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    slug = models.SlugField(unique=True)
    question_text = models.CharField(max_length=200)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)


    def __unicode__(self):
        return self.question_text

    def was_published_recently(self):
        return self.timestamp >= timezone.now() - datetime.timedelta(days=1)
    was_published_recently.admin_order_field = 'timestamp'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    def get_absolute_url(self):
        return reverse("polls:detail", kwargs={"slug": self.slug})

    def strid(self):
        return str(self.id)

class Choice(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __unicode__(self):
        return self.choice_text

class Voted(models.Model):
    vote_count = models.IntegerField(default=0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.vote_count


def create_slug(instance, new_slug=None):
    slug = slugify(instance.question_text)
    if new_slug is not None:
        slug = new_slug
    qs = Question.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug ="{}-{}".format(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_question_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_question_receiver, sender=Question)