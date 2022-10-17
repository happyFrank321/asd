from http import client
from socket import fromfd
from urllib import response


from django.test import Client
from django.test import TestCase
from .models import Post, User
from django.urls import reverse


class ProfileTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.auth_client = Client()

        self.username = 'test_user'
        self.email = 'user@test.com'
        self.password = '123'

        self.user = User.objects.create(
            username=self.username, email=self.email)
        self.user.set_password(self.password)
        self.user.save()
        self.auth_client.login(username=self.username, password=self.password)

    # После регистрации пользователя создается его персональная страница (profile)
    def test_user_profile(self):
        # формируем GET-запрос к странице сайта
        response = self.auth_client.get(
            reverse("profile", kwargs={"username": self.username})
        )
        # Проверяем, что страница найдена
        self.assertEqual(response.status_code, 200)
        # проверяем, что объект пользователя, переданный в шаблон,
        # соответствует пользователю, которого мы создали
        self.assertIsInstance(response.context["current_user"], User)
        self.assertEqual(
            response.context["current_user"].username,
            self.username
        )

    # Неавторизованный посетитель не может опубликовать пост (его редиректит на страницу входа) DONE
    def test_not_auth_user_create_post(self):
        response = self.client.get(reverse('new_post'))
        # Код 302 показывает, что происходит редирект
        self.assertEqual(response.status_code, 302)
        # Находим адрес старници после редиректа (Также про универсальная проверка на незарегистрированного пользователя)
        self.assertTrue(response.url.startswith('/auth/login/'))

    # Авторизованный пользователь может опубликовать пост (new)
    def test_auth_user_create_post(self):
        test_text = 'test test test'
        self.auth_client.post(reverse('new_post'), data={'text': test_text})
        response = self.auth_client.get(
            reverse("profile", kwargs={"username": self.username}))
        # page состоит только из 1 записи
        self.assertEqual(len(response.context['page']), 1)
        # на странице отображается тестовый пост
        self.assertContains(response, test_text)

    # После публикации поста новая запись появляется на главной странице сайта (index), на персональной странице пользователя (profile), и на отдельной странице поста (post)
    def test_auth_user_view_post(self):
        test_text = 'test test test'
        self.auth_client.post(reverse('new_post'), data={'text': test_text})
        post_id = Post.objects.get(author=self.user).pk
        urls = (
            reverse('index'),
            reverse('profile', kwargs={'username': self.username}),
            reverse('post', kwargs={
                    'username': self.username, 'post_id': post_id})
        )
        for element in urls:
            response = self.auth_client.get(element)
            # на странице отображается тестовый пост
            self.assertContains(response, test_text)

    # Авторизованный пользователь может отредактировать свой пост и его содержимое изменится на всех связанных страницах
    def test_auth_user_change_post(self):
        test_text = 'test test test'
        test_text2 = 'change change change'
        self.auth_client.post(reverse('new_post'), data={'text': test_text})
        post_id = Post.objects.get(author=self.user).pk
        self.auth_client.post(reverse('post_edit', kwargs={'username':self.username,'post_id': post_id }), data={'text': test_text2})
        urls = (
            reverse('index'),
            reverse('profile', kwargs={'username': self.username}),
            reverse('post', kwargs={
                    'username': self.username, 'post_id': post_id})
        )
        for element in urls:
            response = self.auth_client.get(element)
            # на странице отображается тестовый пост
            self.assertContains(response, test_text2)
