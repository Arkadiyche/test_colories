from django.db import models

# Create your models here.

class Person(models.Model):
    id = models.AutoField(primary_key=True)
    surname = models.CharField(verbose_name='Фамилия', max_length=150)
    first_name = models.CharField(verbose_name='Имя', max_length=150)
    patronymic = models.CharField(verbose_name='Отчество', max_length=150, default='')
    height = models.IntegerField(verbose_name='Рост')
    weight = models.IntegerField(verbose_name='Вес')
    age = models.IntegerField(verbose_name='Возраст')

    def __str__(self):
        return f'[{self.id}] {self.surname} {self.first_name} {self.patronymic}'

class Activity(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name='Название активности', max_length=150)
    calorie_content = models.IntegerField(verbose_name='Удельная калорийность')
    unit = models.CharField(verbose_name='Единица измерения', max_length=150)

    def __str__(self):
        return f'[{self.id}] {self.name} {self.calorie_content}Ккал за {self.unit}'


class Dish(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name='Название блюда', max_length=150)
    calorie_content = models.IntegerField(verbose_name='Удельная калорийность')
    serving_weight = models.IntegerField(verbose_name='Масса по умольчанию в граммах')

    def __str__(self):
        return f'[{self.id}] {self.name} {self.calorie_content}Ккал в {self.serving_weight}'

class PersonActivity(models.Model):
    id = models.AutoField(primary_key=True)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    activity = models.ForeignKey('Activity', on_delete=models.CASCADE)
    date = models.DateTimeField(verbose_name='Время активности')
    duration = models.IntegerField(verbose_name='Продолжительность активности')

class PersonDish(models.Model):
    id = models.AutoField(primary_key=True)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    dish = models.ForeignKey('Dish', on_delete=models.CASCADE)
    date = models.DateTimeField(verbose_name='Время еды')
    amount = models.IntegerField(verbose_name='Кол-во порций')

