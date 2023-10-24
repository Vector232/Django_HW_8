from django.db import models


class Student(models.Model):

    name = models.TextField()
    # auto_now_add добавил для упрощения тестов, пишу на случай если забыл убрать
    birth_date = models.DateField(
        null=True, auto_now_add=True
    )


class Course(models.Model):

    name = models.TextField()

    students = models.ManyToManyField(
        Student,
        blank=True,
    )
