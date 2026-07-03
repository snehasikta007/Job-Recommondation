from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    WORK_STATUS_CHOICES = [
        ('Fresher', 'Fresher'),
        ('Experienced', 'Experienced'),
    ]
    AVAILABILITY_CHOICES = [
        ('15 days or less', '15 days or less'),
        ('1 Month', '1 Month'),
        ('2 Months', '2 Months'),
        ('3 Months', '3 Months'),
        ('More than 3 Months', 'More than 3 Months'),
    ]

    full_name = models.CharField(max_length=255)
    work_status = models.CharField(max_length=50, choices=WORK_STATUS_CHOICES)
    current_location = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=100, default='India')
    state = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15)
    email_address = models.EmailField()
    availability_to_join = models.CharField(max_length=50, choices=AVAILABILITY_CHOICES)
    
    # Skills and Resume
    skills = models.TextField(help_text="Comma-separated skills")
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)

    # Social & Bio
    bio = models.TextField(blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    portfolio_url = models.URLField(blank=True, null=True)
    profile_completion_percentage = models.IntegerField(default=0)

    def __str__(self):
        return self.full_name

class Education(models.Model):
    QUALIFICATION_CHOICES = [
        ("Bachelor's Degree", "Bachelor's Degree"),
        ("Master's Degree", "Master's Degree"),
        ("Diploma", "Diploma"),
    ]
    COURSE_TYPE_CHOICES = [
        ('Regular', 'Regular'),
        ('Distance Learning', 'Distance Learning'),
    ]
    GRADING_CHOICES = [
        ('Percentage', 'Percentage'),
        ('CGPA', 'CGPA'),
    ]

    user_profile = models.ForeignKey(UserProfile, related_name='education', on_delete=models.CASCADE)
    highest_qualification = models.CharField(max_length=100, choices=QUALIFICATION_CHOICES)
    course = models.CharField(max_length=255)
    course_type = models.CharField(max_length=50, choices=COURSE_TYPE_CHOICES)
    specialization = models.CharField(max_length=255)
    university = models.CharField(max_length=255)
    starting_year = models.IntegerField()
    passing_year = models.IntegerField()
    grading_system = models.CharField(max_length=50, choices=GRADING_CHOICES)
    percentage = models.FloatField()

    def __str__(self):
        return f"{self.course} at {self.university}"

class Job(models.Model):
    JOB_TYPE_CHOICES = [
        ('Onsite', 'Onsite'),
        ('Remote', 'Remote'),
        ('Hybrid', 'Hybrid'),
    ]
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    salary_range = models.CharField(max_length=100, blank=True, null=True)
    experience_level = models.CharField(max_length=100)
    job_type = models.CharField(max_length=50, choices=JOB_TYPE_CHOICES)
    description = models.TextField()
    requirements = models.TextField(help_text="Comma-separated skills required")
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} at {self.company}"

class Application(models.Model):
    STATUS_CHOICES = [
        ('Applied', 'Applied'),
        ('Interview', 'Interview'),
        ('Rejected', 'Rejected'),
        ('Selected', 'Selected'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Applied')
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.job.title}"

class SavedJob(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'job')

class JobRecommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jobs_job_recommendations')
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    match_percentage = models.IntegerField(default=0)
    missing_skills = models.TextField(blank=True, help_text="Comma-separated missing skills")
    why_recommended = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'job')

    def __str__(self):
        return f"{self.user.username} - {self.job.title} ({self.match_percentage}%)"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"
