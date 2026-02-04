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
