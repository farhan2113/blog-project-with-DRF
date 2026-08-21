from django.test import TestCase
from django.urls import reverse
from test_models import create_user, create_post, create_comment

class TestPostListUrl(TestCase):
    def test_post_list_url(self):
        url = reverse('post-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestPostDetailUrl(TestCase):
    def test_post_detail_url(self):
        user = create_user()
        post = create_post(title='title', body='body', owner=user)
        url = reverse('post-detail', args=(post.pk, ))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)



class TestCommentListUrl(TestCase):
    def test_comment_list_url(self):
        url = reverse('comment-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestCommentDetailUrl(TestCase):
    def test_comment_detail_url(self):
        user = create_user()
        post = create_post(title= 'title', body='body', owner=user)
        comment = create_comment(body='body', owner=user, post=post)
        url = reverse('comment-detail', args=(comment.pk))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

