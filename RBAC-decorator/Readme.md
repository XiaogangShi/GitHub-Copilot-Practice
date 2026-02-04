# by Dify "小助手苗苗"

# 1， initial Prompt

使用 Web 框架 Django，实现一个简单的、基于 RBAC 的 API 权限控制装饰器。

# 2, Final

**需求已澄清，最终需求为**

**总结**：用户的需求澄清完毕

**最终的详细需求**：
1.  **核心目标**：在 Django 项目中，实现一个基于角色（Role-Based Access Control, RBAC）的权限控制装饰器，用于保护 API 视图（View）或视图集（ViewSet）。
2.  **功能要求**：
    *   **装饰器形式**：提供一个 Python 装饰器（例如 `@permission_required`），可以方便地应用于 Django 的视图函数或基于类的视图（CBV）的方法上。
    *   **权限检查逻辑**：装饰器应检查当前请求的用户（`request.user`）是否拥有执行该 API 端点所需的权限。
    *   **权限定义**：权限应基于“角色”进行定义。一个用户可以拥有一个或多个角色，一个角色可以关联一个或多个权限。
    *   **权限粒度**：权限的标识符（Permission Code）应为字符串，例如 `"article.create"`, `"user.delete"`。装饰器应能接受单个权限字符串或一个权限字符串列表。
    *   **失败处理**：当用户权限检查失败时，应返回一个标准的、易于理解的错误响应（例如，HTTP 403 Forbidden 状态码，并附带 JSON 格式的错误信息 `{"detail": "您没有执行此操作的权限。"}`）。
    *   **与 Django 认证系统集成**：应能无缝与 Django 内置的 `User` 模型和认证中间件协同工作。
    *   **简单性**：实现应保持轻量和清晰，避免引入过度复杂的 RBAC 特性（如权限继承、数据级权限等），除非后续明确要求。
3.  **非功能性要求**：
    *   **可维护性**：代码结构清晰，易于理解和扩展。
    *   **可测试性**：应便于编写单元测试来验证装饰器的行为。

**最终的技术实现方案**：

1.  **技术栈**：
    *   **后端框架**：Django (>= 3.2)
    *   **数据库**：项目配置的任何数据库（如 SQLite, PostgreSQL），用于存储用户、角色、权限关系。
    *   **主要组件**：Django 模型（Models）、自定义装饰器、Django 中间件（用于提供 `request.user`，已内置）。

2.  **核心实现步骤与项目结构**：
    ```
    your_project/
    ├── manage.py
    ├── your_project/
    │   ├── __init__.py
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    └── rbac/  # 新建的RBAC核心应用
        ├── __init__.py
        ├── admin.py      # 可选，用于在Django Admin管理角色和权限
        ├── models.py     # 定义Role和Permission模型，以及与User的关联
        ├── decorators.py # 实现权限检查装饰器
        ├── utils.py      # 可选，存放权限检查等辅助函数
        └── tests.py      # 单元测试
    ```

3.  **详细实现方案**：
    *   **A. 数据模型 (rbac/models.py)**:
        *   `Permission` 模型：字段至少包含 `codename` (字符串，唯一，如 `"article.publish"`) 和 `name` (描述)。
        *   `Role` 模型：字段至少包含 `name` (字符串，唯一，如 `"管理员"`)。与 `Permission` 模型建立多对多关系 (`ManyToManyField`)。
        *   **扩展 Django User 模型**：推荐使用 `OneToOneField` 或继承 `AbstractUser` 的方式，为 `User` 模型添加一个与 `Role` 模型的多对多关系字段 (`roles`)。
    *   **B. 权限检查装饰器 (rbac/decorators.py)**:
        *   实现一个名为 `permission_required` 的函数，它接受一个或多个权限字符串作为参数。
        *   装饰器内部逻辑：
            1.  获取当前请求的 `user` 对象。
            2.  检查用户是否已认证 (`user.is_authenticated`)。
            3.  获取用户所有角色关联的权限集合（可通过 `user.roles.all().values_list('permissions__codename', flat=True)` 查询，建议缓存优化）。
            4.  判断所需权限是否是用户拥有权限的子集。
            5.  如果检查通过，则执行原视图函数；如果不通过，则使用 `django.http.JsonResponse` 返回一个 403 错误。
        *   需要处理装饰器应用于函数视图和基于类的视图（如 `APIView` 的 `get`, `post` 方法）的兼容性。可以使用 `django.utils.decorators.method_decorator` 来适配 CBV。
    *   **C. 使用示例**:
        ```python
        # views.py
        from django.http import JsonResponse
        from rbac.decorators import permission_required

        # 用于函数视图
        @permission_required('article.create')
        def create_article(request):
            return JsonResponse({'status': 'Article created!'})

        # 用于基于类的视图 (DRF APIView 或 Django View)
        from rest_framework.views import APIView
        from django.utils.decorators import method_decorator

        class ArticleAPIView(APIView):
            @method_decorator(permission_required(['article.read', 'article.list']))
            def get(self, request):
                return JsonResponse({'data': '...'})

            @method_decorator(permission_required('article.create'))
            def post(self, request):
                return JsonResponse({'status': 'created'})
        ```
    *   **D. 数据库迁移与管理员配置**:
        *   运行 `python manage.py makemigrations rbac` 和 `python manage.py migrate` 创建数据库表。
        *   在 `rbac/admin.py` 中注册 `Role` 和 `Permission` 模型，方便通过 Django Admin 界面进行管理。

4.  **后续可扩展方向**：
    *   将权限信息缓存到内存（如 Redis）以提高性能。
    *   支持更复杂的权限逻辑（如基于对象的权限检查）。
    *   与 Django REST framework (DRF) 的 `permission_classes` 进行更深度集成，提供 DRF 风格的权限类。**最终代码（DeepSeek 生成** ：
我将为您实现一个完整的Django RBAC权限控制系统。以下是完整的代码实现：

## 1. 首先创建RBAC应用

```bash
python manage.py startapp rbac
```

## 2. 数据模型 (rbac/models.py)

```python
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
```

## 3. 信号处理器 (rbac/signals.py)

```python
"""
信号处理器
自动创建用户扩展信息
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    当创建新用户时，自动创建对应的UserProfile
    """
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    保存用户时，同时保存UserProfile
    """
    # 使用try-except防止在迁移时出现错误
    try:
        instance.profile.save()
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=instance)
```

## 4. 权限检查装饰器 (rbac/decorators.py)

```python
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
```

## 5. 工具函数 (rbac/utils.py)

```python
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
```

## 6. 管理员配置 (rbac/admin.py)

```python
"""
Django Admin配置
在管理后台管理角色和权限
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Permission, Role, UserProfile


class PermissionAdmin(admin.ModelAdmin):
    """权限管理后台配置"""
    list_display = ['codename', 'name', 'created_at']
    list_filter = ['created_at']
    search_fields = ['codename', 'name', 'description']
    ordering = ['codename']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('基本信息', {
            'fields': ('codename', 'name', 'description')
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


class RoleAdmin(admin.ModelAdmin):
    """角色管理后台配置"""
    list_display = ['name', 'get_permission_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    filter_horizontal = ['permissions']  # 更好的多对多选择界面
    readonly_fields = ['created_at', 'updated_at']
    
    def get_permission_count(self, obj):
        """显示角色拥有的权限数量"""
        return obj.permissions.count()
    get_permission_count.short_description = '权限数量'


class UserProfileInline(admin.StackedInline):
    """在User管理页面内联显示UserProfile"""
    model = UserProfile
    can_delete = False
    verbose_name_plural = '用户扩展信息'
    filter_horizontal = ['roles']  # 更好的多对多选择界面


class UserAdmin(BaseUserAdmin):
    """扩展User管理页面"""
    inlines = [UserProfileInline]
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'get_roles']
    
    def get_roles(self, obj):
        """显示用户的角色"""
        try:
            return ", ".join([role.name for role in obj.profile.roles.all()])
        except UserProfile.DoesNotExist:
            return "无"
    get_roles.short_description = '角色'


# 注册模型到管理后台
admin.site.register(Permission, PermissionAdmin)
admin.site.register(Role, RoleAdmin)

# 重新注册User模型，使用自定义的UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
```

## 7. 应用配置 (rbac/apps.py)

```python
from django.apps import AppConfig


class RbacConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rbac'
    verbose_name = 'RBAC权限管理'
    
    def ready(self):
        """
        应用启动时执行
        导入信号处理器
        """
        import rbac.signals
```

## 8. 测试用例 (rbac/tests.py)

```python
"""
RBAC系统测试用例
"""
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Permission, Role, UserProfile
from .decorators import permission_required
from django.http import JsonResponse


# 测试视图函数
@permission_required('article.create')
def test_create_article_view(request):
    return JsonResponse({'status': 'success', 'message': '文章创建成功'})


@permission_required(['article.read', 'article.list'], logical_operator='OR')
def test_read_article_view(request):
    return JsonResponse({'status': 'success', 'message': '文章读取成功'})


class RBACModelTests(TestCase):
    """模型测试"""
    
    def setUp(self):
        """测试前准备数据"""
        # 创建权限
        self.permission1 = Permission.objects.create(
            codename='article.create',
            name='创建文章'
        )
        self.permission2 = Permission.objects.create(
            codename='article.read',
            name='读取文章'
        )
        self.permission3 = Permission.objects.create(
            codename='article.delete',
            name='删除文章'
        )
        
        # 创建角色
        self.editor_role = Role.objects.create(name='编辑')
        self.editor_role.permissions.add(self.permission1, self.permission2)
        
        self.admin_role = Role.objects.create(name='管理员')
        self.admin_role.permissions.add(self.permission1, self.permission2, self.permission3)
        
        # 创建用户
        self.editor_user = User.objects.create_user(
            username='editor',
            password='password123'
        )
        self.editor_user.profile.roles.add(self.editor_role)
        
        self.admin_user = User.objects.create_user(
            username='admin',
            password='password123'
        )
        self.admin_user.profile.roles.add(self.admin_role)
        
        self.normal_user = User.objects.create_user(
            username='normal',
            password='password123'
        )
    
    def test_permission_creation(self):
        """测试权限创建"""
        self.assertEqual(self.permission1.codename, 'article.create')
        self.assertEqual(self.permission1.name, '创建文章')
    
    def test_role_creation(self):
        """测试角色创建"""
        self.assertEqual(self.editor_role.name, '编辑')
        self.assertEqual(self.editor_role.permissions.count(), 2)
    
    def test_user_profile_creation(self):
        """测试用户扩展信息创建"""
        self.assertIsNotNone(self.editor_user.profile)
        self.assertEqual(self.editor_user.profile.roles.count(), 1)
    
    def test_user_permissions(self):
        """测试用户权限获取"""
        editor_permissions = self.editor_user.profile.get_all_permissions()
        self.assertIn('article.create', editor_permissions)
        self.assertIn('article.read', editor_permissions)
        self.assertNotIn('article.delete', editor_permissions)
        