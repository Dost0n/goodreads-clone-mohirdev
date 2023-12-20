from django.test import TestCase
from users.models import CustomUser
from django.urls import reverse
from django.contrib.auth import get_user



class RegistrationTestCase(TestCase):
    
    def test_user_account_is_created(self):
        self.client.post(reverse('users:register_page'),
        data = {
            "username": "Doston",
            "last_name": "Imomaliyev",
            "first_name": "Doston",
            "email": "ctron1108@gmail.com",
            "password": "doston123",
        })

        user = CustomUser.objects.get(username = "Doston")

        self.assertEqual(user.first_name, "Doston")
        self.assertEqual(user.last_name, "Imomaliyev")
        self.assertEqual(user.email, "ctron1108@gmail.com")
        self.assertNotEqual(user.password, "doston123")
        self.assertTrue(user.check_password('doston123'))


    def test_required_fields(self):
        response = self.client.post(reverse('users:register_page'),
                        data = {
                            "first_name": "Doston",
                            "email": "ctron1108@gmail.com",
                        }
        )
        user_count = CustomUser.objects.count()

        self.assertEqual(user_count, 0)
        self.assertFormError(response, "form", 'username', 'This field is required.')
        self.assertFormError(response, "form", 'password', 'This field is required.')
    

    def test_invalid_email(self):
        response = self.client.post(reverse('users:register_page'),
                                    data = {
                                        "username": "Doston",
                                        "last_name": "Imomaliyev",
                                        "first_name": "Doston",
                                        "email": "invalid-email",
                                        "password": "doston123",
                                    })
        user_count = CustomUser.objects.count()
        self.assertEqual(user_count, 0)
        self.assertFormError(response, "form", 'email', 'Enter a valid email address.')


    def test_unique_username(self):
        user =  CustomUser.objects.create(
            username = "Doston",
            last_name = "Imomaliyev",
            first_name = "Doston"
        )
        user.set_password('doston123')
        user.save()

        response = self.client.post(reverse('users:register_page'),
                                    data = {
                                        "username": "Doston",
                                        "last_name": "Imomaliyev",
                                        "first_name": "Doston",
                                        "email": "invalid-email",
                                        "password": "doston123",
                                    })
        user_count = CustomUser.objects.count()
        self.assertEqual(user_count, 1)
        self.assertFormError(response, "form", 'username', 'A user with that username already exists.')



class LoginTestCase(TestCase):

    def setUp(self):
        self.db_user =  CustomUser.objects.create(username = "Doston",first_name = "Doston")
        self.db_user.set_password('doston123')
        self.db_user.save()

    # create user and login and get user and assert to authentication
    def test_successful_login(self):
        self.client.post(reverse('users:login_page'),
                                    data = {
                                        "username": "Doston",
                                        "password": "doston123",
                                    })
        user = get_user(self.client)

        self.assertTrue(user.is_authenticated)

    def test_wrong_crdentials(self):
        self.client.post(reverse('users:login_page'),
                                    data = {
                                        "username": "Doston123",
                                        "password": "doston123",
                                    })
        user = get_user(self.client)

        self.assertFalse(user.is_authenticated)
        self.client.post(reverse('users:login_page'),
                                    data = {
                                        "username": "Doston",
                                        "password": "doston",
                                    })
        user = get_user(self.client)

        self.assertFalse(user.is_authenticated)
    
    def test_logout(self):
        self.client.login(username='doston', password='doston123')

        response = self.client.get(reverse("users:logout_page"))
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)


class ProfileTestCase(TestCase):

    def test_login_required(self):
        response = self.client.get(reverse("users:profile_page"))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('users:login_page') + '?next=/users/profile/')

    def test_profile_details(self):
        user =  CustomUser.objects.create(
                                    username = "doston",
                                    last_name = "Imomaliyev",
                                    first_name = "Doston",
                                    email = "ctron1108@gmail.com"
                                )
        user.set_password('doston123')
        user.save()

        self.client.login(username='doston', password='doston123')

        response = self.client.get(reverse("users:profile_page"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, user.username)
        self.assertContains(response, user.last_name)
        self.assertContains(response, user.first_name)
        self.assertContains(response, user.email)
    
    def test_profile_update(self):
        user =  CustomUser.objects.create(
                                    username = "doston",
                                    last_name = "Imomaliyev",
                                    first_name = "Doston",
                                    email = "ctron1108@gmail.com"
                                )
        user.set_password('doston123')
        user.save()

        self.client.login(username='doston', password='doston123')

        response = self.client.post(reverse("users:profile_edit_page"), 
                                   data = {
                                        "username" : "doston",
                                        "last_name" : "Imomaliyev",
                                        "first_name" : "W1zard",
                                        "email" : "ctron11@gmail.com"
                                        }
                                   )
        user = CustomUser.objects.get(pk=user.pk)
        # user.refresh_from_db


        self.assertEqual(user.first_name, "W1zard")
        self.assertEqual(user.email, "ctron11@gmail.com")
        self.assertEqual(response.url, reverse("users:profile_page"))