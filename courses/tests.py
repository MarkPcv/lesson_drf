from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from courses.models import Course, Lesson
from users.models import User


class LessonTest(APITestCase):

    def create_member(self):
        """Creates a new MEMBER user"""
        # Create test user with MEMBER role
        self.user_member = User.objects.create(
            email='test@gmail.com',
            is_active=True,
        )
        self.user_member.set_password('test')
        self.user_member.save()

        # Obtain token
        # data = {
        #     'email': 'test@gmail.com',
        #     'password': 'test'
        # }
        # response = self.client.post(
        #     reverse("users:token_obtain_pair"),
        #     data=data
        # )
        # self.token_member = response.json()['access']

    def create_moderator(self):
        """Creates a new MODERATOR user"""
        # Create test user with MEMBER role
        self.user_moderator = User.objects.create(
            email='test2@gmail.com',
            is_active=True,
            role='moderator'
        )
        self.user_moderator.set_password('test')
        self.user_moderator.save()

        # Obtain token
        # data = {
        #     'email': 'test@gmail.com',
        #     'password': 'test'
        # }
        # response = self.client.post(
        #     reverse("users:token_obtain_pair"),
        #     data=data
        # )
        # self.token_moderator = response.json()['access']

    def setUp(self) -> None:
        """Set up initial objects for each test"""
        # Create MEMBER user
        self.create_member()
        # Create MODERATOR user
        self.create_moderator()

        # Create Course object
        self.course = Course.objects.create(
            name='test course',
            description='course description'
        )
        # Create Lesson object
        self.lesson = Lesson.objects.create(
            name='test lesson',
            description='lesson description',
            course=self.course,
        )

    def test_create_lesson(self):
        """Testing lesson creation"""
        # Authenticate user without token
        self.client.force_authenticate(self.user_member)

        data = {
            'name': 'test lesson2',
            'description': 'lesson2 description',
            'course': self.course.id,
        }

        response = self.client.post(
            reverse("courses:lesson-create"),
            # data=data,
            # headers={
            #     'Authorization': f'Bearer {self.token_member}'
            # },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            Lesson.objects.count(),
            2
        )

    def test_get_list(self):
        """Testing retrieval of list of lessons """
        # Authenticate user without token
        self.client.force_authenticate(self.user_moderator)

        response = self.client.get(
            reverse("courses:lesson-list"),
            # headers={
            #     'Authorization': f'Bearer {self.token_moderator}'
            # },
            # user=self.user_moderator,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {'id': 1, 'video_url': None, 'name': 'test lesson',
                     'preview': None, 'description': 'lesson description',
                     'course': 1, 'owner': None}
                ]
            }
        )
