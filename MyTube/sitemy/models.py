from django.db import models
from django.contrib.auth import models as user_models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

def user_directory_path(instance, filename):
    # путь, куда будет осуществлена загрузка MEDIA_ROOT/user_<id>/<filename>
    return 'photo-user_{0}/{1}'.format(instance.id, filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # photo = models.CharField(max_length=500, verbose_name='Фото', blank=True)
    photo = models.ImageField(upload_to=user_directory_path, verbose_name="Фото", default='default.jpg')
    isManager = models.BooleanField(verbose_name="Менеджер или Пользователь", default=False)
    def __str__(self):
        return f'Клиент {self.id}'


    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()




class Videos(models.Model):
    name_video = models.CharField(max_length=200, verbose_name='Название видео', blank=False, null=False)
    title = models.CharField(max_length=1000, verbose_name='Описание к видео', blank=True, null=True)
    videofile = models.FileField(upload_to='videos/', blank=True, null=True, verbose_name="")
    userProfile = models.ForeignKey(Profile, on_delete=models.PROTECT, verbose_name='Клиент')
    isPublished = models.BooleanField(default=False, verbose_name="Опубликовано ли")


    class Meta:
        verbose_name = 'Видео'
        verbose_name_plural = 'Видео'

    def __str__(self):
        return self.name_video


class Like_DisLikes(models.Model):
    likes = models.IntegerField(verbose_name='Лайки', default=0)
    dislikes = models.IntegerField(verbose_name='Дизлайки', default=0)
    video = models.ForeignKey('Videos', on_delete=models.CASCADE)
    userProfile = models.ForeignKey(Profile, on_delete=models.PROTECT, verbose_name='Клиент')

    class Meta:
        verbose_name = 'Лайки и Дизлайки'
        verbose_name_plural = 'Лайки и Дизлайки'

    def __str__(self):
        return f' Лайки : {self.likes}\t Дизлайки : {self.dislikes}'

