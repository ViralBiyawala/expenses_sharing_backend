# expenses/tests.py
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Expense, ExpenseSplit
from decimal import Decimal

class ExpenseAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(username='user1', password='password1')
        self.user2 = User.objects.create_user(username='user2', password='password2')
        self.client.force_authenticate(user=self.user1)

    def test_create_expense_equal_split(self):
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
        Expense.objects.create(title='User1 Expense', amount=100, split_type='EQUAL', created_by=self.user1)
        Expense.objects.create(title='User2 Expense', amount=200, split_type='EQUAL', created_by=self.user2)

        response = self.client.get('/api/expenses/user_expenses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'User1 Expense')

    def test_get_overall_expenses(self):
        Expense.objects.create(title='User1 Expense', amount=100, split_type='EQUAL', created_by=self.user1)
        Expense.objects.create(title='User2 Expense', amount=200, split_type='EQUAL', created_by=self.user2)

        response = self.client.get('/api/expenses/overall_expenses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)