from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group # Import Group
from .models import User, UserProfile, RegistrationCode, EventRegistration, ParticipantRegistrationLog
from import_export.admin import ImportExportModelAdmin

# --- Inlines ---
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'

# --- Custom User Admin ---
# We unregister the default Group admin to inline it with our User.
admin.site.unregister(Group) 

@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_groups')
    list_filter = ('is_staff', 'is_active', 'groups') 

    @admin.display(description='Roles')
    def get_groups(self, obj):
        return ", ".join([g.name for g in obj.groups.all()])

# --- Registration Code Admin ---
@admin.register(RegistrationCode)
class RegistrationCodeAdmin(ImportExportModelAdmin):
    list_display = ('code', 'event', 'is_active', 'uses_count', 'max_uses', 'expires_at', 'created_by')
    list_filter = ('is_active', 'event', 'created_at')
    search_fields = ('code', 'event__event_name', 'created_by__username')
    readonly_fields = ('uses_count', 'created_at', 'updated_at', 'created_by')
    
    def save_model(self, request, obj, form, change):
        if not obj.pk: obj.created_by = request.user
        super().save_model(request, obj, form, change)

# --- Event Registration Admin ---
@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ('participant', 'event', 'status', 'registered_at')
    list_filter = ('status', 'event')
    search_fields = ('participant__username', 'event__event_name')
    readonly_fields = ('registered_at',)

# --- Registration Log Admin ---
@admin.register(ParticipantRegistrationLog)
class RegistrationLogAdmin(admin.ModelAdmin):
    list_display = ('email_attempt', 'code_used', 'status', 'reason', 'timestamp', 'ip_address')
    list_filter = ('status', 'timestamp')
    search_fields = ('email_attempt', 'code_used', 'ip_address')
    
    # Make the log completely read-only in the admin
    def has_add_permission(self, request): return False
    def has_change_permission(self, request, obj=None): return False
    def has_delete_permission(self, request, obj=None): return False
