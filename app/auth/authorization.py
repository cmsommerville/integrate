import functools
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request


class ResourcePermissions:
    """
    A class that defines the roles allowed to perform the HTTP methods of a REST API resource
    """

    def __init__(self, *args, **kwargs):
        self.get = kwargs.get('get', ['*'])
        self.post = kwargs.get('post', ['*'])
        self.patch = kwargs.get('patch', ['*'])
        self.put = kwargs.get('put', ['*'])
        self.delete = kwargs.get('delete', ['*'])
        
    def add(self, method: str, permission: str, *args, **kwargs):
        permissions = getattr(self, method)
        if isinstance(permissions, list):
            setattr(self, method, permissions.append(permission))
        else:
            raise Exception('Cannot append permission to method')

    def remove(self, method: str, permission: str, *args, **kwargs):
        permissions = getattr(self, method)
        if isinstance(permissions, list):
            setattr(self, method, [p for p in permissions if p != permission])
        else:
            raise Exception('Cannot remove permission from method')



def authorize(func):
    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        cls = args[0]
        permissions = getattr(cls, 'permissions', None)
        if permissions is None:
            return func(*args, **kwargs)
        if not isinstance(permissions, ResourcePermissions):
            return {"status": "error", "message": "The permissions for this resource should be an instance of the `ResourcePermissions` class"}

        permitted_roles = getattr(permissions, func.__name__, None)
        if permitted_roles is None:
            return {"status": "error", "message": f"Cannot find the permitted roles for the provided HTTP method, {func.__name__}"}
        if not isinstance(permitted_roles, (list, tuple,)):
            permitted_roles = [permitted_roles]
        if '*' in permitted_roles: 
            return func(*args, **kwargs)
        
        verify_jwt_in_request()
        identity = get_jwt_identity()
        user_roles = identity.get('roles')

        user_permitted_roles = set(user_roles) & set(permitted_roles)
        if len(user_permitted_roles) > 0:
            return func(*args, **kwargs)
        return {'status': 'error', 'message': 'User is not authorized'}, 403
    return wrapper_decorator
    
