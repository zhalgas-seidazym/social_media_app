import json
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from post.models import Post, Comment

User = get_user_model()

class SocialMediaMurynAPITestCase(APITestCase):

    def setUp(self):
        # Create a user and authenticate
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='TestPassword123')
        self.token_url = reverse('token_obtain_pair')

        # Get JWT Token
        response = self.client.post(self.token_url, {'username': 'testuser', 'password': 'TestPassword123'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.token = response.data['access']

        # Set Authorization header
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        # Create a test post using the correct field name (creator)
        self.post = Post.objects.create(content="Test Post", creator=self.user)  # Correct field name

        # Direct URLs
        self.signup_url = '/api/accounts/signup/'
        self.followers_url = f'/api/accounts/{self.user.id}/followers/'
        self.following_url = f'/api/accounts/{self.user.id}/following/'
        self.info_url = f'/api/accounts/{self.user.id}/info/'
        self.follow_unfollow_url = f'/api/accounts/follow_unfollow/{self.user.id}/'

    def test_signup(self):
        url = self.signup_url
        data = {"username": "newuser","email": "newuser@example.com","password": "NewPassword123"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_create(self):
        url = '/api/post/create/'
        data = {"content": "Test Post"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_retrieve(self):
        url = f'/api/post/{self.post.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_update(self):
        url = f'/api/post/update/{self.post.id}/'
        data = {"content": "Updated Post"}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_delete(self):
        url = f'/api/post/delete/{self.post.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_post_like(self):
        url = f'/api/post/{self.post.id}/like/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_comment_create(self):
        url = f'/api/post/{self.post.id}/comments/create/'
        data = {"content": "Test Comment"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_comment_list(self):
        Comment.objects.create(content="Test Comment", post=self.post, creator=self.user)
        url = f'/api/post/{self.post.id}/comments/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_comment_update(self):
        comment = Comment.objects.create(content="Test Comment", post=self.post, creator=self.user)
        url = f'/api/post/comments/update/{comment.id}/'
        data = {"content": "Updated Comment"}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_comment_delete(self):
        comment = Comment.objects.create(content="Test Comment", post=self.post, creator=self.user)
        url = f'/api/post/comments/delete/{comment.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
