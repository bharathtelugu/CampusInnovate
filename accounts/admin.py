from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User as DefaultUser # Import the default User
from .models import (
    User, 
    UserProfile, 
    RegistrationCode, 
    EventRegistration, 
    ParticipantRegistrationLog
)
from import_export.admin import ImportExportModelAdmin # For the Import/Export feature

# --- 1. Inlines ---
# This lets you edit a User's Profile from the User's admin page
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'

# --- 2. Custom User Admin ---

# First, unregister the default User admin that Django makes
admin.site.unregister(DefaultUser)

@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    # Add the UserProfile editor to the bottom of the User page
    inlines = (UserProfileInline,)
    
    # Customize the columns in the User list
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_groups')
    
    # Add filters for staff, active status, and roles (groups)
    list_filter = ('is_staff', 'is_active', 'groups') 

    @admin.display(description='Roles')
    def get_groups(self, obj):
        # This shows all groups (roles) in a clean, comma-separated list
        return ", ".join([g.name for g in obj.groups.all()])

# --- 3. Registration Code Admin ---
# We use ImportExportModelAdmin to get the "Export as CSV" and "Import" buttons
@admin.register(RegistrationCode)
class RegistrationCodeAdmin(ImportExportModelAdmin):
    list_display = ('code', 'event', 'is_active', 'uses_count', 'max_uses', 'expires_at', 'created_by')
    list_filter = ('is_active', 'event', 'created_at')
    search_fields = ('code', 'event__event_name', 'created_by__username')
    readonly_fields = ('uses_count', 'created_at', 'updated_at', 'created_by')
    
    # This automatically sets the creator to the logged-in admin
    def save_model(self, request, obj, form, change):
        if not obj.pk: # If this is a new code
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

# --- 4. Event Registration Admin ---
@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ('participant', 'event', 'status', 'registered_at')
    list_filter = ('status', 'event')
    search_fields = ('participant__username', 'event__event_name')
    readonly_fields = ('registered_at',)

# --- 5. Registration Log Admin ---
@admin.register(ParticipantRegistrationLog)
class RegistrationLogAdmin(admin.ModelAdmin):
    list_display = ('email_attempt', 'code_used', 'status', 'reason', 'timestamp', 'ip_address')
    list_filter = ('status', 'timestamp')
    search_fields = ('email_attempt', 'code_used', 'ip_address')
    
    # Make the log read-only. No one should edit or add logs.
    readonly_fields = [f.name for f in ParticipantRegistrationLog._meta.fields]

    def has_add_permission(self, request):
        return False # Nobody should be adding logs manually

    def has_change_permission(self, request, obj=None):
        return False # Or changing them
        
    def has_delete_permission(self, request, obj=None):
        return False # Or deleting them