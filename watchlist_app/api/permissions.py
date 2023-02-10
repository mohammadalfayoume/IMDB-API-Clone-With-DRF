from rest_framework import permissions

# Here I just check if the user currently has a permission as admin or not
class IsAdminOrReadOnly(permissions.IsAdminUser):
    def has_permission(self, request, view):
        # admin_permission= bool(request.user and request.user.is_staff)
        # return request.method== 'GET' or admin_permission
        # SAFE_METHODS, which is a tuple containing 'GET', 'OPTIONS' and 'HEAD'
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            # if the method was POST, DELETE, PUT. If the current user == user in the object, return True
            return bool(request.user and request.user.is_staff)

class IsReviewUserOrReadOnly(permissions.BasePermission):
    def has_object_permission(self,request,view,obj):
        # SAFE_METHODS, which is a tuple containing 'GET', 'OPTIONS' and 'HEAD'
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            # if the method was POST, DELETE, PUT. If the current user == user in the object, return True
            return obj.review_user == request.user or request.user.is_staff