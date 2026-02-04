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