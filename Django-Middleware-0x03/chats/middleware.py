from django.http import HttpResponseForbidden

class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only restrict access to certain paths, e.g., admin/mod-only actions
        protected_paths = ['/chat/manage/', '/chat/delete/', '/chat/moderate/']
        
        if request.path in protected_paths:
            user = request.user
            if not user.is_authenticated:
                return HttpResponseForbidden("Authentication required.")

            # Check for admin or moderator roles
            user_roles = getattr(user, 'groups', None)
            if user.is_superuser:
                return self.get_response(request)

            if not user_roles.filter(name__in=['admin', 'moderator']).exists():
                return HttpResponseForbidden("You do not have permission to access this resource.")
        
        return self.get_response(request)
