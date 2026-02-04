"""
RBAC权限控制系统的数据模型
定义角色(Role)、权限(Permission)模型及其与用户(User)的关系
"""
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class Permission(models.Model):
    """
    权限模型
    存储系统中的所有权限，每个权限有唯一的codename
    """
    codename = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='权限代码',
        help_text='权限的唯一标识符，如"article.create"'
    )
    name = models.CharField(
        max_length=100,
        verbose_name='权限名称',
        help_text='权限的描述性名称'
    )
    description = models.TextField(
        blank=True,
        verbose_name='权限描述',
        help_text='权限的详细说明'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '权限'
        verbose_name_plural = '权限管理'
        ordering = ['codename']

    def __str__(self):
        return f"{self.name} ({self.codename})"


class Role(models.Model):
    """
    角色模型
    角色可以关联多个权限，用户可以被分配多个角色
    """
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='角色名称'
    )
    permissions = models.ManyToManyField(
        Permission,
        blank=True,
        verbose_name='拥有的权限',
        related_name='roles'
    )
    description = models.TextField(
        blank=True,
        verbose_name='角色描述',
        help_text='角色的职责和权限说明'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '角色'
        verbose_name_plural = '角色管理'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_permission_codenames(self):
        """获取角色所有权限的codename列表"""
        return list(self.permissions.values_list('codename', flat=True))


# 扩展User模型，添加roles字段
# 方法1：使用OneToOneField扩展（推荐，不修改原有User模型）
class UserProfile(models.Model):
    """
    用户扩展模型
    为Django内置User模型添加角色关联
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='关联用户'
    )
    roles = models.ManyToManyField(
        Role,
        blank=True,
        verbose_name='用户角色',
        related_name='users'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '用户扩展信息'
        verbose_name_plural = '用户扩展信息'

    def __str__(self):
        return f"{self.user.username} 的扩展信息"

    def get_all_permissions(self):
        """获取用户所有权限的codename集合"""
        permissions = set()
        for role in self.roles.all():
            permissions.update(role.get_permission_codenames())
        return permissions

    def has_permission(self, permission_codename):
        """检查用户是否拥有指定权限"""
        return permission_codename in self.get_all_permissions()

    def has_any_permission(self, permission_codenames):
        """检查用户是否拥有任意一个指定权限"""
        user_permissions = self.get_all_permissions()
        return any(perm in user_permissions for perm in permission_codenames)

    def has_all_permissions(self, permission_codenames):
        """检查用户是否拥有所有指定权限"""
        user_permissions = self.get_all_permissions()
        return all(perm in user_permissions for perm in permission_codenames)


# 方法2：继承AbstractUser自定义User模型（如果需要完全自定义用户模型）
# 在settings.py中设置AUTH_USER_MODEL = 'rbac.User'
"""
class User(AbstractUser):
    roles = models.ManyToManyField(
        Role,
        blank=True,
        verbose_name='用户角色',
        related_name='users'
    )
    
    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户管理'
    
    def get_all_permissions(self):
        permissions = set()
        for role in self.roles.all():
            permissions.update(role.get_permission_codenames())
        return permissions
    
    def has_permission(self, permission_codename):
        return permission_codename in self.get_all_permissions()
"""