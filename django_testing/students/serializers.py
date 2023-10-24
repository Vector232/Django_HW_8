from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.conf import settings

from students.models import Course, Student


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ("id", "name", "students")


    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""

        # TODO: добавьте требуемую валидацию
        if self.context["request"].method in ['POST', 'PATCH']:
            count_of_student = len(data.get('students', []))
        
            if count_of_student > settings.MAX_STUDENTS_PER_COURSE:
                raise ValidationError('Слишком много студентов на курсе!')

        return data

class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = ("id", "name", "birth_date")