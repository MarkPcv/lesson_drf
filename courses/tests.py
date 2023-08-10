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
            owner=self.user_member
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
        # Create second lesson
        response = self.client.post(
            reverse("courses:lesson-create"),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        # Check total number of lessons
        self.assertEqual(
            Lesson.objects.count(),
            2
        )

    def test_get_list(self):
        """Testing retrieval of list of lessons """
        # Authenticate MODERATOR without token
        self.client.force_authenticate(self.user_moderator)
        # Get list of lessons
        response = self.client.get(
            reverse("courses:lesson-list"),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        # Check list data
        self.assertEqual(
            response.json(),
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {'id': 1, 'video_url': None, 'name': 'test lesson',
                     'preview': None, 'description': 'lesson description',
                     'course': 1, 'owner': 1}
                ]
            }
        )

    def test_get_lesson(self):
        """Testing retrieval of one lesson"""
        # Authenticate user without token
        self.client.force_authenticate(self.user_moderator)
        # Get lesson
        response = self.client.get(
            reverse("courses:lesson-detail", kwargs={'pk': self.lesson.id}),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        # Check lesson data
        self.assertEqual(
            response.json(),
            {'id': 1, 'video_url': None, 'name': 'test lesson',
             'preview': None, 'description': 'lesson description',
             'course': 1, 'owner': 1}

        )

    def test_update_lesson(self):
        """Testing lesson update"""
        # Authenticate user without token
        self.client.force_authenticate(self.user_moderator)
        # Update name of lesson
        data = {
            'name': 'test lesson updated',
        }

        response = self.client.patch(
            reverse("courses:lesson-update", kwargs={'pk': self.lesson.id}),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        # Check updated name
        self.assertEqual(
            Lesson.objects.get(pk=1).name,
            'test lesson updated'
        )

    def test_delete_lesson(self):
        """Testing lesson deletion"""
        # Authenticate MEMBER without token and owner of current lesson
        self.client.force_authenticate(self.user_member)
        # print(Lesson.objects.get(pk=1).owner.email) # TODO: remove
        # Delete lesson
        response = self.client.delete(
            reverse("courses:lesson-delete", kwargs={'pk': self.lesson.id})
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
        # Check that no lesson exists in Database
        self.assertFalse(
            Lesson.objects.exists()
        )


