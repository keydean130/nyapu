from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from diary.models import Diary

class DiaryViewSetTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('diary-list')  # Assuming you've named the URL pattern as 'diary-list'
        self.valid_payload = {'title': 'value1', 'contents': 'value2'}
        self.invalid_payload = {'title': '', 'contents': 'value2'}

    def test_create_diary(self):
        response = self.client.post(self.url, data=self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(diary.objects.count(), 1)
        self.assertEqual(diary.objects.get().title, 'value1')

    def test_create_diary_invalid_payload(self):
        response = self.client.post(self.url, data=self.invalid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(diary.objects.count(), 0)

    def test_retrieve_diary(self):
        diary = Diary.objects.create(title='value1', contents='value2')
        retrieve_url = reverse('diary-detail', kwargs={'pk': diary.pk})
        response = self.client.get(retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'value1')

    def test_update_diary(self):
        diary = Diary.objects.create(title='value1', contents='value2')
        update_url = reverse('diary-detail', kwargs={'pk': diary.pk})
        response = self.client.put(update_url, data={'title': 'new_value'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(diary.objects.get().title, 'new_value')

    def test_delete_diary(self):
        diary = Diary.objects.create(title='value1', contents='value2')
        delete_url = reverse('diary-detail', kwargs={'pk': diary.pk})
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(diary.objects.count(), 0)
