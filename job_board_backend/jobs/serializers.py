from rest_framework import serializers
from .models import Category, Job

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

class JobSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )

    class Meta:
        model = Job
        fields = [
            'id', 'title', 'description', 'location', 'salary', 'type',
            'category', 'category_id', 'created_at', 'updated_at'
        ]