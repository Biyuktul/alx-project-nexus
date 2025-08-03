from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from .models import Category, Job
from .serializers import JobSerializer, CategorySerializer
from authentication.permissions import IsRecruiterOrJobSeeker
from django.db.models import Q

class CategoryListView(APIView):
    permission_classes = [IsRecruiterOrJobSeeker]

    @swagger_auto_schema(
        operation_description="List all categories",
        responses={200: CategorySerializer(many=True), 201: CategorySerializer, 400: "Bad Request"},
    )
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    @swagger_auto_schema(
        operation_description="Create a new category (admin only)",
        request_body=CategorySerializer,
        responses={201: CategorySerializer, 400: "Bad Request"}
    )
    def post(self, request):
        serializer = CategorySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryDetailView(APIView):
    permission_classes = [IsRecruiterOrJobSeeker]

    @swagger_auto_schema(
        operation_description="Get a category",
        responses={200: CategorySerializer, 400: "Bad Request", 404: "Not Found"}
    )
    def get(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
            serialzer = CategorySerializer(category)
            return Response(serialzer.data, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
    @swagger_auto_schema(
        operation_description="Update a category (admin only)",
        request_body=CategorySerializer,
        responses={200: CategorySerializer, 400: "Bad Request", 404: "Not Found"}
    )
    def put(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(category, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Category.DoesNotExist:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
    @swagger_auto_schema(
        operation_description="Delete a category (admin only)",
        responses={204: "No Content", 404: "Not Found"}
    )
    def delete(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
            category.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Category.DoesNotExist:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

class JobListView(APIView):
    permission_classes = [IsRecruiterOrJobSeeker]

    @swagger_auto_schema(
          operation_description="List all published jobs with optional filters: location, category, keyword",
          responses={200: JobSerializer(many=True), 201: JobSerializer, 400: "Bad Request"}
      )
    def get(self, request):
        queryset = Job.objects.select_related('category', 'posted_by').all()
        keyword = request.query_params.get('keyword')
        location = request.query_params.get('location')
        category = request.query_params.get('category')

        if keyword:
            queryset = queryset.filter(Q(title__icontains=keyword) | Q(description__icontains=keyword))
        if location:
            queryset = queryset.filter(location__icontains=location)
        if category:
            try:
                category_obj = Category.objects.get(name=category)
                queryset = queryset.filter(category=category_obj)
            except Category.DoesNotExist:
                return Response({"error": "Category not found"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = JobSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Create a new job (admin only)",
        request_body=JobSerializer,
        responses={200: JobSerializer, 400: "Bad Request", 404: "Not Found"}
    )
    def post(self, request):
        serializer = JobSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class JobDetailView(APIView):
    permission_classes = [IsRecruiterOrJobSeeker]

    @swagger_auto_schema(
        operation_description="Get a job",
        responses={200: JobSerializer, 404: "Not Found", 400: "Bad Request"}
    )
    def get(self, request, pk):
        try:
            job = Job.objects.get(pk=pk)
            serializer = JobSerializer(job)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Job.DoesNotExist:
            return Response({"error": "Job not found"}, status=status.HTTP_404_NOT_FOUND)
    @swagger_auto_schema(
        operation_description="Update a Job (admin only)",
        request_body=JobSerializer,
        responses={200: JobSerializer, 400: "Bad Request", 404: "Not Found"}
    )
    def put(self, request, pk):
        try:
            job = Job.objects.get(pk=pk)
            serializer = JobSerializer(job, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Job.DoesNotExist:
            return Response({"error": "Job not found"}, status=status.HTTP_404_NOT_FOUND)
    @swagger_auto_schema(
        operation_description="Delete a job (admin only)",
        responses={204: "No Content", 404: "Not Found"}
    )
    def delete(self, request, pk):
        try:
            job = Job.objects.get(pk=pk)
            job.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Job.DoesNotExist:
            return Response({"error": "Job not found"}, status=status.HTTP_404_NOT_FOUND)
