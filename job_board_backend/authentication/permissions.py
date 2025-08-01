from rest_framework import permissions

class IsRecruiterOrJobSeeker(permissions.BasePermission):
    """
    Custom permission to:
    - Allow authenticated applicants to view Jobs
    - Allow authenticated recruiters to view/edit Jobs
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_authenticated and request.user.is_recruiter

class IsOwner(permissions.BasePermission):
    """
    Custom permission to:
    - Allow authenticated users to view/edit their own applications
    - Allow recruiters to view/edit applications for jobs they posted
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.applicant == request.user or (request.user.is_recruiter and obj.job.recruiter == request.user)