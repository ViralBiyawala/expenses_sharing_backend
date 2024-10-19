from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import Expense, ExpenseSplit
from decimal import Decimal

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class ExpenseSplitSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    percentage = serializers.DecimalField(max_digits=5, decimal_places=2, required=False)

    class Meta:
        model = ExpenseSplit
        fields = ['user', 'amount', 'percentage']

class ExpenseSerializer(serializers.ModelSerializer):
    splits = ExpenseSplitSerializer(many=True)

    class Meta:
        model = Expense
        fields = ['id', 'title', 'amount', 'split_type', 'created_at', 'splits']

    def validate(self, data):
        split_type = data['split_type']
        splits = data['splits']
        total_amount = data['amount']

        if split_type == 'EQUAL':
            split_amount = total_amount / len(splits)
            for split in splits:
                split['amount'] = split_amount

        elif split_type == 'EXACT':
            total_split = sum(Decimal(split.get('amount', 0)) for split in splits)
            if total_split != total_amount:
                raise serializers.ValidationError("Sum of split amounts must equal the total expense amount")

        elif split_type == 'PERCENTAGE':
            total_percentage = sum(Decimal(split.get('percentage', 0)) for split in splits)
            if total_percentage != 100:
                raise serializers.ValidationError("Sum of percentages must be 100%")
            for split in splits:
                split['amount'] = (Decimal(split['percentage']) / 100) * total_amount

        return data

    def create(self, validated_data):
        splits_data = validated_data.pop('splits')
        expense = Expense.objects.create(**validated_data)
        
        for split_data in splits_data:
            ExpenseSplit.objects.create(expense=expense, **split_data)
        
        return expense