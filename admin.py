from django.contrib import admin
from .models import UserProfile, Education, ContactMessage

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email_address', 'work_status')
    search_fields = ('full_name', 'email_address')

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'course', 'university', 'passing_year')
    search_fields = ('user_profile__full_name', 'university')

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject')
