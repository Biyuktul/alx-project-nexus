from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from .models import Application
from .serializers import ApplicationSerializer
from authentication.permissions import IsOwner

class ApplicationListView(APIView):
    permission_classes = [IsOwner]

    @swagger_auto_schema(
        operation_description="List applications (users see own, recruiters see for their jobs)",
        responses={200: ApplicationSerializer(many=True)}
    )
    def get(self, request):
        if request.user.is_recruiter:
            applications = Application.objects.filter(job__recruiter=request.user)
        else:
            applications = Application.objects.filter(applicant=request.user)
        serializer = ApplicationSerializer(applications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Create a job application (authenticated users)",
        request_body=ApplicationSerializer,
        responses={201: ApplicationSerializer, 400: "Bad Request"}
    )
    def post(self, request):
        serializer = ApplicationSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ApplicationDetailView(APIView):
    permission_classes = [IsOwner]

    @swagger_auto_schema(
        operation_description="Retrieve an application (owner or recruiter)",
        responses={200: ApplicationSerializer, 404: "Not Found"}
    )
    def get(self, request, pk):
        try:
            application = Application.objects.get(pk=pk)
            self.check_object_permissions(request, application)
            serializer = ApplicationSerializer(application)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Application.DoesNotExist:
            return Response({"error": "Application not found"}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description="Update an application (owner or recruiter)",
        request_body=ApplicationSerializer,
        responses={200: ApplicationSerializer, 400: "Bad Request", 404: "Not Found"}
    )
    def put(self, request, pk):
        try:
            application = Application.objects.get(pk=pk)
            self.check_object_permissions(request, application)
            serializer = ApplicationSerializer(application, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Application.DoesNotExist:
            return Response({"error": "Application not found"}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description="Delete an application (owner or recruiter)",
        responses={204: "No Content", 404: "Not Found"}
    )
    def delete(self, request, pk):
        try:
            application = Application.objects.get(pk=pk)
            self.check_object_permissions(request, application)
            application.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Application.DoesNotExist:
            return Response({"error": "Application not found"}, status=status.HTTP_404_NOT_FOUND)