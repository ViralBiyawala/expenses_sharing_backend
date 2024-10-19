# expenses/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from .models import Expense
from .serializers import UserSerializer, ExpenseSerializer
import csv
from django.http import HttpResponse

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=False, methods=['GET'])
    def user_expenses(self, request):
        user_expenses = Expense.objects.filter(created_by=request.user)
        serializer = self.get_serializer(user_expenses, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def overall_expenses(self, request):
        overall_expenses = Expense.objects.all()
        serializer = self.get_serializer(overall_expenses, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def download_balance_sheet(self, request):
        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="balance_sheet.csv"'

        writer = csv.writer(response)
        writer.writerow(['Title', 'Amount', 'Split Type', 'Created By', 'Created At', 'Split Info'])

        expenses = Expense.objects.all()
        for expense in expenses:
            split_info = "; ".join(
                [f"{split.user.username}: {split.amount} ({split.percentage}%)" for split in expense.splits.all()]
            )
            writer.writerow([
                expense.title, 
                expense.amount, 
                expense.get_split_type_display(), 
                expense.created_by.username, 
                expense.created_at,
                split_info
            ])

        return response
