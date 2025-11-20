from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return f'{self.name}'


class Post(models.Model):
    header = models.CharField(max_length=50)
    text = models.TextField()
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_updated = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    image = models.ImageField(blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        format_datetime_created = self.datetime_created.strftime('%d.%m.%Y %H:%M')
        format_datetime_updated = self.datetime_updated.strftime('%d.%m.%Y %H:%M')
        return f'Заголовок: {self.header} Текст: {self.text[0:20]}... Автор: {self.author} Создано: {format_datetime_created} Изменено: {format_datetime_updated}'