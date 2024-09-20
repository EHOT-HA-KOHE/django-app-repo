from django.db import models

from users.models import User
from pairs.models import Pools


class UserCollections(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название подборки')
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True, related_name='pool_lists', verbose_name='Пользователь')  # Один пользователь может иметь много подборок
    pools = models.ManyToManyField(to=Pools, related_name='pool_lists', verbose_name='Пулы')  # Подборка может содержать много пулов

    # Чтобы добавлять токен в подборку если пользователь не авторизован
    session_key = models.CharField(max_length=32, null=True, blank=True)

    class Meta:
        db_table = 'pool_list'
        verbose_name = 'Подборка пулов'
        verbose_name_plural = 'Подборки пулов'
        constraints = [
            models.UniqueConstraint(fields=['user', 'name'], name='unique_user_list_name')
        ]
        
    def __str__(self):
        return self.name
