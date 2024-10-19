# # expenses/tests.py
# from django.test import TestCase
# from django.contrib.auth.models import User
# from rest_framework.test import APIClient
# from rest_framework import status
# from .models import Expense, ExpenseSplit
# from decimal import Decimal
# from rest_framework_simplejwt.tokens import RefreshToken

# class ExpenseAPITestCase(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.user1 = User.objects.create_user(username='user1', password='password1')
#         self.user2 = User.objects.create_user(username='user2', password='password2')
        
#         # JWT Authentication
#         self.client.force_authenticate(user=self.user1)
#         refresh = RefreshToken.for_user(self.user1)
#         self.jwt_token = str(refresh.access_token)
        
#     def authenticate(self):
#         self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.jwt_token)

#     def test_create_expense_equal_split(self):
#         self.authenticate()
#         data = {
#             'title': 'Test Expense',
#             'amount': '100.00',
#             'split_type': 'EQUAL',
#             'splits': [
#                 {'user': self.user1.id},
#                 {'user': self.user2.id}
#             ]
#         }
#         response = self.client.post('/api/expenses/', data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Expense.objects.count(), 1)
#         self.assertEqual(ExpenseSplit.objects.count(), 2)
#         self.assertEqual(ExpenseSplit.objects.filter(amount=Decimal('50.00')).count(), 2)

#     def test_create_expense_exact_split(self):
#         self.authenticate()
#         data = {
#             'title': 'Test Expense',
#             'amount': '100.00',
#             'split_type': 'EXACT',
#             'splits': [
#                 {'user': self.user1.id, 'amount': '60.00'},
#                 {'user': self.user2.id, 'amount': '40.00'}
#             ]
#         }
#         response = self.client.post('/api/expenses/', data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Expense.objects.count(), 1)
#         self.assertEqual(ExpenseSplit.objects.count(), 2)
#         self.assertEqual(ExpenseSplit.objects.get(user=self.user1).amount, Decimal('60.00'))
#         self.assertEqual(ExpenseSplit.objects.get(user=self.user2).amount, Decimal('40.00'))

#     def test_create_expense_percentage_split(self):
#         self.authenticate()
#         data = {
#             'title': 'Test Expense',
#             'amount': '100.00',
#             'split_type': 'PERCENTAGE',
#             'splits': [
#                 {'user': self.user1.id, 'percentage': '70.00'},
#                 {'user': self.user2.id, 'percentage': '30.00'}
#             ]
#         }
#         response = self.client.post('/api/expenses/', data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Expense.objects.count(), 1)
#         self.assertEqual(ExpenseSplit.objects.count(), 2)
#         self.assertEqual(ExpenseSplit.objects.get(user=self.user1).amount, Decimal('70.00'))
#         self.assertEqual(ExpenseSplit.objects.get(user=self.user2).amount, Decimal('30.00'))

#     def test_invalid_percentage_split(self):
#         self.authenticate()
#         data = {
#             'title': 'Test Expense',
#             'amount': '100.00',
#             'split_type': 'PERCENTAGE',
#             'splits': [
#                 {'user': self.user1.id, 'percentage': '60.00'},
#                 {'user': self.user2.id, 'percentage': '30.00'}
#             ]
#         }
#         response = self.client.post('/api/expenses/', data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#     def test_get_user_expenses(self):
#         self.authenticate()
#         Expense.objects.create(title='User1 Expense', amount=100, split_type='EQUAL', created_by=self.user1)
#         Expense.objects.create(title='User2 Expense', amount=200, split_type='EQUAL', created_by=self.user2)

#         response = self.client.get('/api/expenses/user_expenses/')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)
#         self.assertEqual(response.data[0]['title'], 'User1 Expense')

#     def test_get_overall_expenses(self):
#         # Creating an admin user with necessary permissions
#         admin_user = User.objects.create_superuser(username='admin', password='adminpass')
#         self.client.force_authenticate(user=admin_user)

#         # Creating sample expenses
#         Expense.objects.create(title='User1 Expense', amount=100, split_type='EQUAL', created_by=self.user1)
#         Expense.objects.create(title='User2 Expense', amount=200, split_type='EQUAL', created_by=self.user2)

#         # Accessing the overall expenses endpoint
#         response = self.client.get('/api/expenses/overall_expenses/')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 2)

#     def test_list_all_expenses_admin_only(self):
#         admin_user = User.objects.create_superuser(username='admin', password='adminpass')
#         self.client.force_authenticate(user=admin_user)

#         Expense.objects.create(title='User1 Expense', amount=100, split_type='EQUAL', created_by=self.user1)
#         Expense.objects.create(title='User2 Expense', amount=200, split_type='EQUAL', created_by=self.user2)

#         response = self.client.get('/api/expenses/overall_expenses/')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 2)

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from decimal import Decimal
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Expense, ExpenseSplit

# expenses/test_tests.py

class ExpenseAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(username='user1', password='password1')
        self.user2 = User.objects.create_user(username='user2', password='password2')
        
        # JWT Authentication
        self.client.force_authenticate(user=self.user1)
        refresh = RefreshToken.for_user(self.user1)
        self.jwt_token = str(refresh.access_token)
        
    def authenticate(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.jwt_token)

    def test_create_expense_equal_split(self):
        self.authenticate()
        data = {
            'title': 'Test Expense',
            'amount': '100.00',
            'split_type': 'EQUAL',
            'splits': [
                {'user': self.user1.id},
                {'user': self.user2.id}
            ]
        }
        response = self.client.post('/api/expenses/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Expense.objects.count(), 1)
        self.assertEqual(ExpenseSplit.objects.count(), 2)
        self.assertEqual(ExpenseSplit.objects.filter(amount=Decimal('50.00')).count(), 2)

    def test_create_expense_exact_split(self):
        self.authenticate()
        data = {
            'title': 'Test Expense',
            'amount': '100.00',
            'split_type': 'EXACT',
            'splits': [
                {'user': self.user1.id, 'amount': '60.00'},
                {'user': self.user2.id, 'amount': '40.00'}
            ]
        }
        response = self.client.post('/api/expenses/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Expense.objects.count(), 1)
        self.assertEqual(ExpenseSplit.objects.count(), 2)
        self.assertEqual(ExpenseSplit.objects.get(user=self.user1).amount, Decimal('60.00'))
        self.assertEqual(ExpenseSplit.objects.get(user=self.user2).amount, Decimal('40.00'))

    def test_create_expense_percentage_split(self):
        self.authenticate()
        data = {
            'title': 'Test Expense',
            'amount': '100.00',
            'split_type': 'PERCENTAGE',
            'splits': [
                {'user': self.user1.id, 'percentage': '70.00'},
                {'user': self.user2.id, 'percentage': '30.00'}
            ]
        }
        response = self.client.post('/api/expenses/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Expense.objects.count(), 1)
        self.assertEqual(ExpenseSplit.objects.count(), 2)
        self.assertEqual(ExpenseSplit.objects.get(user=self.user1).amount, Decimal('70.00'))
        self.assertEqual(ExpenseSplit.objects.get(user=self.user2).amount, Decimal('30.00'))

    def test_invalid_percentage_split(self):
        self.authenticate()
        data = {
            'title': 'Test Expense',
            'amount': '100.00',
            'split_type': 'PERCENTAGE',
            'splits': [
                {'user': self.user1.id, 'percentage': '60.00'},
                {'user': self.user2.id, 'percentage': '30.00'}
            ]
        }
        response = self.client.post('/api/expenses/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_user_expenses(self):
        self.authenticate()
        Expense.objects.create(title='User1 Expense', amount=100, split_type='EQUAL', created_by=self.user1)
        Expense.objects.create(title='User2 Expense', amount=200, split_type='EQUAL', created_by=self.user2)

        response = self.client.get('/api/expenses/user_expenses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'User1 Expense')

    def test_get_overall_expenses(self):
        # Creating an admin user with necessary permissions
        admin_user = User.objects.create_superuser(username='admin', password='adminpass')
        self.client.force_authenticate(user=admin_user)

        # Creating sample expenses
        Expense.objects.create(title='User1 Expense', amount=100, split_type='EQUAL', created_by=self.user1)
        Expense.objects.create(title='User2 Expense', amount=200, split_type='EQUAL', created_by=self.user2)

        # Accessing the overall expenses endpoint
        response = self.client.get('/api/expenses/overall_expenses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_list_all_expenses_admin_only(self):
        admin_user = User.objects.create_superuser(username='admin', password='adminpass')
        self.client.force_authenticate(user=admin_user)

        Expense.objects.create(title='User1 Expense', amount=100, split_type='EQUAL', created_by=self.user1)
        Expense.objects.create(title='User2 Expense', amount=200, split_type='EQUAL', created_by=self.user2)

        response = self.client.get('/api/expenses/overall_expenses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_user_expenses_admin_only(self):
        admin_user = User.objects.create_superuser(username='admin', password='adminpass')
        self.client.force_authenticate(user=admin_user)

        Expense.objects.create(title='User1 Expense', amount=100, split_type='EQUAL', created_by=self.user1)
        Expense.objects.create(title='User2 Expense', amount=200, split_type='EQUAL', created_by=self.user2)

        response = self.client.get('/api/expenses/user_expenses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(len(response.data), 2)

    def test_download_balance_sheet_admin_only(self):
        admin_user = User.objects.create_superuser(username='admin', password='adminpass')
        self.client.force_authenticate(user=admin_user)

        response = self.client.get('/api/expenses/download_balance_sheet/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Disposition'], 'attachment; filename="balance_sheet.csv"')
