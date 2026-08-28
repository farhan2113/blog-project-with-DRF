import re

from .test_models import create_post, create_user, create_comment
from django.urls import reverse
from rest_framework.test import APITestCase

class TestPostViewSet(APITestCase):
    def test_get_posts(self):
        url = reverse('post-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


    def test_create_posts(self):
        user = create_user()
        data = {'title':'title', 'body':'body'}
        self.client.force_login(user)
        url = reverse('post-list')
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, 201)


    def test_retrieve_post(self):
        user = create_user()
        post = create_post(body='body', title='title', owner=user)
        url = reverse('post-detail', args=(post.pk, ))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_post(self):
        user = create_user()
        self.client.force_login(user)
        post = create_post(body='body', title='title', owner=user)
        url = reverse('post-detail', args=(post.pk, ))
        data = {'body':'updated body', 'title':'updated title'}        
        response = self.client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_delete_post(self):
        user = create_user()
        post = create_post(title='title', body='body', owner=user)

        self.client.force_login(user)
        url = reverse('post-detail', args=(post.pk, ))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 204)

class TestCommentViewSet(APITestCase):
    def test_get_comments(self):
        url = reverse('comment-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_comment(self):
        user = create_user()
        
        post = create_post(title='title', body='body', owner=user)
        url = reverse('comment-list')
        post_url = reverse('post-detail', args=(post.pk, ))
        data = {'body':'body', 'post':post_url}
        self.client.force_login(user)
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, 201)

    def test_retrieve_comment(self):
        user = create_user()
        post = create_post(title='title', body='body', owner=user)       
        comment = create_comment(body='body', owner=user, post=post)

        url = reverse('comment-detail', args=(comment.pk, ))

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)


    def test_update_comment(self):
        user = create_user()
        post = create_post(title= 'title', body='body', owner=user)
        comment = create_comment(body='body', post=post, owner=user)

        self.client.force_login(user)

        url = reverse('comment-detail', args=(comment.pk, ))
        post_url = reverse('post-detail', args=(post.pk, ))
        data = {'body':'updated body', 'post':post_url}
        response = self.client.put(url, data=data, format='json')

        self.assertEqual(response.status_code, 200)

    def test_delete_comment(self):
        user = create_user()
        post = create_post(title= 'title', body='body', owner=user)
        comment = create_comment(body='body', post=post, owner=user)
        
        self.client.force_login(user)
        url = reverse('comment-detail', args=(comment.pk, ))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 204)

    

class TestSignUpApiView(APITestCase):
    def test_sign_up(self):
        data = {'username':'username', 'email':'example@example.com','password':'password', 'password_2':'password'}
        url = reverse('sign-up')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)


class TestLogInApiView(APITestCase):
    def test_login(self):
        url = reverse('login')
        create_user()
        data = {'username':'username', 'email':'example@example.com', 'password':'password'}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, 200)


class TestRefreshAccessTokenApiView(APITestCase):
    def test_refresh_access_token(self):
        login_url = reverse('login')
        data = {'username':'username', 'password':'password'}
        self.client.post(login_url, data, format= 'json')

        url = reverse('refresh-access-token')
        response = self.client.post(url)

        self.assertEqual(response.status_code, 200)


class TestLogOutApiView(APITestCase):
    def test_logout(self):
        url = reverse('logout')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)