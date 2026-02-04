"""
权限检查装饰器
提供@permission_required装饰器用于保护视图函数和类视图方法
"""
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from functools import wraps
import logging

logger = logging.getLogger(__name__)


def permission_required(permissions, logical_operator='AND'):
    """
    权限检查装饰器
    
    参数:
        permissions: 字符串或字符串列表，需要的权限代码
        logical_operator: 逻辑运算符，'AND'表示需要所有权限，'OR'表示需要任意一个权限
    
    返回:
        装饰器函数
    """
    # 统一处理权限参数，确保是列表形式
    if isinstance(permissions, str):
        required_permissions = [permissions]
    else:
        required_permissions = list(permissions)
    
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # 检查用户是否已认证
            if not request.user.is_authenticated:
                return JsonResponse(
                    {'detail': '请先登录。', 'code': 'authentication_failed'},
                    status=401
                )
            
            # 获取用户扩展信息
            try:
                user_profile = request.user.profile
            except Exception as e:
                logger.error(f"获取用户扩展信息失败: {e}")
                return JsonResponse(
                    {'detail': '用户信息异常，请联系管理员。', 'code': 'user_profile_error'},
                    status=500
                )
            
            # 检查权限
            has_access = False
            if logical_operator.upper() == 'AND':
                # 需要所有权限
                has_access = user_profile.has_all_permissions(required_permissions)
            else:
                # 需要任意一个权限
                has_access = user_profile.has_any_permission(required_permissions)
            
            if has_access:
                # 权限检查通过，执行原视图函数
                return view_func(request, *args, **kwargs)
            else:
                # 权限检查失败，返回403错误
                permission_str = ', '.join(required_permissions)
                return JsonResponse(
                    {
                        'detail': f'您没有执行此操作的权限。所需权限: {permission_str}',
                        'code': 'permission_denied',
                        'required_permissions': required_permissions
                    },
                    status=403
                )
        
        return _wrapped_view
    
    return decorator


def permission_required_any(permissions):
    """
    简化装饰器：检查用户是否拥有任意一个指定权限
    
    参数:
        permissions: 字符串或字符串列表，需要的权限代码
    
    返回:
        装饰器函数
    """
    return permission_required(permissions, logical_operator='OR')


def permission_required_all(permissions):
    """
    简化装饰器：检查用户是否拥有所有指定权限
    
    参数:
        permissions: 字符串或字符串列表，需要的权限代码
    
    返回:
        装饰器函数
    """
    return permission_required(permissions, logical_operator='AND')


# 为基于类的视图提供装饰器
class PermissionRequiredMixin:
    """
    基于类的视图权限检查Mixin
    可以在Django的类视图中使用
    """
    
    @classmethod
    def as_view(cls, **initkwargs):
        """
        重写as_view方法，为视图添加权限检查
        """
        view = super().as_view(**initkwargs)
        
        # 获取类中定义的权限要求
        required_permissions = getattr(cls, 'required_permissions', None)
        logical_operator = getattr(cls, 'permission_logical_operator', 'AND')
        
        if required_permissions:
            # 应用权限检查装饰器
            return permission_required(required_permissions, logical_operator)(view)
        
        return view