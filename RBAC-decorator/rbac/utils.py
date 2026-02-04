"""
RBAC工具函数
提供权限相关的辅助功能
"""
from django.core.cache import cache
from .models import UserProfile, Role, Permission


def get_user_permissions(user):
    """
    获取用户的所有权限（带缓存）
    
    参数:
        user: User对象
    
    返回:
        权限codename的集合
    """
    if not user.is_authenticated:
        return set()
    
    # 使用缓存提高性能
    cache_key = f'user_permissions_{user.id}'
    permissions = cache.get(cache_key)
    
    if permissions is None:
        try:
            user_profile = user.profile
            permissions = user_profile.get_all_permissions()
            # 缓存5分钟
            cache.set(cache_key, permissions, 300)
        except Exception:
            permissions = set()
    
    return permissions


def clear_user_permissions_cache(user_id):
    """
    清除用户的权限缓存
    
    参数:
        user_id: 用户ID
    """
    cache_key = f'user_permissions_{user_id}'
    cache.delete(cache_key)


def create_permission(codename, name, description=''):
    """
    创建权限的辅助函数
    
    参数:
        codename: 权限代码
        name: 权限名称
        description: 权限描述
    
    返回:
        创建的Permission对象
    """
    permission, created = Permission.objects.get_or_create(
        codename=codename,
        defaults={
            'name': name,
            'description': description
        }
    )
    return permission


def create_role(name, permissions=None, description=''):
    """
    创建角色的辅助函数
    
    参数:
        name: 角色名称
        permissions: 权限codename列表
        description: 角色描述
    
    返回:
        创建的Role对象
    """
    role, created = Role.objects.get_or_create(
        name=name,
        defaults={'description': description}
    )
    
    if permissions:
        permission_objs = Permission.objects.filter(codename__in=permissions)
        role.permissions.set(permission_objs)
    
    return role


def assign_role_to_user(user, role_name):
    """
    为用户分配角色
    
    参数:
        user: User对象
        role_name: 角色名称
    
    返回:
        bool: 是否分配成功
    """
    try:
        role = Role.objects.get(name=role_name)
        user.profile.roles.add(role)
        # 清除权限缓存
        clear_user_permissions_cache(user.id)
        return True
    except (Role.DoesNotExist, UserProfile.DoesNotExist):
        return False


def check_permission(user, permission_codename):
    """
    检查用户是否拥有指定权限（带缓存）
    
    参数:
        user: User对象
        permission_codename: 权限代码
    
    返回:
        bool: 是否拥有权限
    """
    permissions = get_user_permissions(user)
    return permission_codename in permissions