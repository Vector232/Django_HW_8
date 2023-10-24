import pytest
from rest_framework.test import APIClient
from model_bakery import baker
from django.contrib.auth.models import User


from students.models import Course, Student


def test_example():
    assert True, "Just test example"


@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def user():
    return User.objects.create_user('tester')

@pytest.fixture
def courses_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory
    
@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory

@pytest.fixture
def castom_settings(settings):
    settings.MAX_STUDENTS_PER_COURSE = 3
    return settings.MAX_STUDENTS_PER_COURSE
    
    
@pytest.mark.django_db
def test_get_first_course(client, user, courses_factory):
    id = 1
    courses = courses_factory(_quantity=id+5)
    response = client.get(f'http://localhost:8000/api/v1/courses/{id}/')

    assert response.status_code // 10 == 20, f'Неожиданный ответ: {response.status_code}'
    data = response.json()
    assert courses[0].id == data['id'], 'Не совпал ID!'
    assert courses[0].name == data['name'], 'Не совпало имя!'

@pytest.mark.django_db
def test_get_list_of_courses(client, user, courses_factory):
    courses = courses_factory(_quantity=20)

    response = client.get('http://localhost:8000/api/v1/courses/')

    assert response.status_code // 10 == 20, f'Неожиданный ответ: {response.status_code}'
    data = response.json()
    assert len(data) == len(courses), f'Неверная длина ответа: {len(data)}, ожидалось {len(courses)}!'
    for index, cours in enumerate(data):
        assert courses[index].id == cours['id'], f'Не совпал ID у {index}!'
        assert courses[index].name == cours['name'], f'Не совпало имя у {index}!'

@pytest.mark.django_db
def test_course_id_filtering(client, user, courses_factory):
    id = 7
    courses = courses_factory(_quantity=id + 10)
    filter_id = courses[id].id
    response = client.get(f'http://localhost:8000/api/v1/courses/?id={filter_id}')
    
    assert response.status_code // 10 == 20, f'Неожиданный ответ: {response.status_code}!'
    data = response.json()
    assert data[0]['id'] == filter_id, f'Не совпал ID! {data}'
    assert courses[id].name == data[0]['name'], 'Не совпало имя!'

@pytest.mark.django_db
def test_course_name_filtering(client, user, courses_factory):
    id = 7
    courses = courses_factory(_quantity=id + 10)
    filter_name = courses[id].name
    response = client.get(f'http://localhost:8000/api/v1/courses/?name={filter_name}')
    
    assert response.status_code // 10 == 20, f'Неожиданный ответ: {response.status_code}!'
    data = response.json()
    for cours in data:
        assert cours['name'] == filter_name, f'Не совпало имя у {cours["id"]}!'

@pytest.mark.django_db
def test_create_course(client, user):
    path = 'http://localhost:8000/api/v1/courses/'

    response = client.post(path=path, data={'name': 'test_course'})

    assert response.status_code // 10 == 20, f'Неожиданный ответ: {response.status_code}!'

@pytest.mark.django_db
def test_create_course(client, user, courses_factory):
    courses = courses_factory(_quantity=1)
    id = courses[0].id
    path = f'http://localhost:8000/api/v1/courses/{id}/'

    response = client.patch(path=path, data={'name': 'test_course_patched'})

    assert response.status_code // 10 == 20, f'Неожиданный ответ: {response.status_code}!'

@pytest.mark.django_db
def test_delete_course(client, user, courses_factory):
    courses = courses_factory(_quantity=1)
    id = courses[0].id
    path = f'http://localhost:8000/api/v1/courses/{id}/'

    response = client.delete(path=path, data={'name': 'test_course_patched'})

    assert response.status_code // 10 == 20, f'Неожиданный ответ: {response.status_code}!'

@pytest.mark.django_db
def test_limit_of_students(client, user, castom_settings, student_factory):
    students = student_factory(_quantity=4)
    path = f'http://localhost:8000/api/v1/courses/'

    response_OK = client.post(path=path, data={'name': 'test_course',
                                                'students': [1,2,3]})
    response_not_OK = client.post(path=path, data={'name': 'test_course',
                                                    'students': [1,2,3,4]})
    
    assert response_OK.status_code // 10 == 20, f'Неожиданный ответ: {response_OK.status_code}!' 
    assert response_not_OK.status_code // 10 != 20, f'Неожиданный ответ: {response_not_OK.status_code}!' 
