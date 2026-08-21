from django.test import TestCase
from models import Post, Comment
from django.contrib.auth import get_user_model

User = get_user_model()

def create_user():
    user = User(first_name= 'first_name', last_name= 'last_name')
    user.save()
    return user

def create_post(title, body, owner):
    post = Post(title= title, body= body, owner= owner)
    post.save()
    return post

def create_comment(post, owner, body):
    comment = Comment(post=post, owner= owner, body= body)
    comment.save()
    return comment

class TestPost(TestCase):
    def test_if_post_has_title(self):
        user = create_user()
        post = create_post(title= 'title', body= 'body', owner=user)
        self.assertEqual(post.title, 'title')


    def test_if_post_has_body(self):
        user = create_user()
        post = create_post(title= 'title', body= 'body', owner=user)
        self.assertEqual(post.body, 'body')

    def test_if_post_has_user(self):
        user = create_user()
        post = create_post(title= 'title', body= 'body', owner=user)
        self.assertEqual(post.owner_id, 1)


class TestComment(TestCase):
    def test_if_comment_has_body(self):
        user = create_user()
        post = create_post(title='title', body= 'body', owner=user)
        comment = create_comment(body='body', post=post, owner= user)
        self.assertEqual(comment.body, 'body')

    def test_if_comment_related_to_post(self):
        user = create_user()
        post = create_post(title='title', body= 'body', owner=user)
        comment = create_comment(body='body', post=post, owner= user)
        self.assertEqual(comment.post_id, 1)

    def test_if_comment_related_to_user(self):
        user = create_user()
        post = create_post(title='title', body= 'body', owner=user)
        comment = create_comment(body='body', post=post, owner= user)
        self.assertEqual(comment.owner_id, 1)        