from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import UserProfile, Education, ContactMessage, Job, Application, SavedJob, Notification
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import json

def home(request):
    return render(request, 'landing.html')

def register_user(request):
    if request.method == 'POST':
        if request.content_type == 'application/json':
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)
        else:
            data = request.POST
            
        full_name = data.get('full_name')
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        phone_number = data.get('phone_number') or data.get('phone')
        status = data.get('status') or 'Fresher'
        
        print(f"Registration attempt: {email}") # Debugging

        if password != confirm_password:
            return JsonResponse({'status': 'error', 'message': 'Passwords do not match'}, status=400)
        
        if User.objects.filter(email=email).exists() or User.objects.filter(username=email).exists():
            return JsonResponse({'status': 'error', 'message': 'Email already registered'}, status=400)
            
        try:
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=full_name
            )
            login(request, user)
            print(f"User created and logged in: {email}")

            # Store initial registration data in session for next steps
            request.session['basic_data'] = {
                'full_name': full_name,
                'email_address': email,
                'mobile_number': phone_number,
                'work_status': status,
            }
            
            return JsonResponse({'status': 'success', 'redirect': '/basic/'})
        except Exception as e:
            print(f"Registration Error for {email}: {str(e)}")
            return JsonResponse({'status': 'error', 'message': f'Server error: {str(e)}'}, status=500)

    return render(request, 'Landing page/Registation/Registation.html')

def login_user(request):
    if request.method == 'POST':
        if request.content_type == 'application/json':
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)
        else:
            data = request.POST
            
        email = data.get('email')
        password = data.get('password')
        
        print(f"Login attempt: {email}") # Debugging

        if not email or not password:
             return JsonResponse({'status': 'error', 'message': 'Email and password are required'}, status=400)
             
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            print(f"Login successful: {email}")
            return JsonResponse({'status': 'success', 'redirect': '/dashboard/'})
        else:
            print(f"Login failed - Invalid credentials: {email}")
            return JsonResponse({'status': 'error', 'message': 'Invalid credentials. Please check your email and password.'}, status=401)
            
    return render(request, 'Landing page/Login page/login.html')

def logout_user(request):
    logout(request)
    return redirect('/')

def basic_details(request):
    profile = None
    if request.user.is_authenticated:
        try:
            profile = UserProfile.objects.get(email_address=request.user.email)
        except UserProfile.DoesNotExist:
            pass

    if request.method == 'POST':
        data = request.POST
        print(f"Basic Details attempt for user: {request.user.email if request.user.is_authenticated else 'Anonymous'}")

        basic_data = request.session.get('basic_data', {})
        basic_data.update({
            'full_name': data.get('full_name'),
            'work_status': data.get('work_status'),
            'current_location': data.get('current_location'),
            'country': data.get('country'),
            'state': data.get('state'),
            'mobile_number': data.get('mobile_number'),
            'email_address': data.get('email_address'),
            'availability_to_join': data.get('availability_to_join'),
        })
        request.session['basic_data'] = basic_data
        print(f"Basic details stored in session for: {data.get('email_address')}")
        return JsonResponse({'status': 'success', 'redirect': '/education/'})
    
    return render(request, 'Basic details/basic.html', {'profile': profile})

def education_details(request):
    education = None
    if request.user.is_authenticated:
        try:
            profile = UserProfile.objects.get(email_address=request.user.email)
            education = Education.objects.filter(user_profile=profile).first()
        except UserProfile.DoesNotExist:
            pass

    if request.method == 'POST':
        data = request.POST
        print(f"Education Details attempt for user: {request.user.email if request.user.is_authenticated else 'Anonymous'}")

        request.session['education_data'] = {
            'highest_qualification': data.get('highest_qualification'),
            'course': data.get('course'),
            'course_type': data.get('course_type'),
            'specialization': data.get('specialization'),
            'university': data.get('university'),
            'starting_year': data.get('starting_year'),
            'passing_year': data.get('passing_year'),
            'grading_system': data.get('grading_system'),
            'percentage': data.get('percentage'),
        }
        print(f"Education details stored in session")
        return JsonResponse({'status': 'success', 'redirect': '/skills/'})
    
    return render(request, 'Registation1/education.html', {'education': education})

def skills_details(request):
    profile = None
    if request.user.is_authenticated:
        try:
            profile = UserProfile.objects.get(email_address=request.user.email)
        except UserProfile.DoesNotExist:
            pass

    if request.method == 'POST':
        # Final step, save all data
        print(f"Skills Details/Final Save attempt for user: {request.user.email if request.user.is_authenticated else 'Anonymous'}")

        basic_data = request.session.get('basic_data', {})
        education_data = request.session.get('education_data', {})
        
        # Files are in request.FILES
        profile_photo = request.FILES.get('profile_photo')
        resume = request.FILES.get('resume')
        skills = request.POST.get('skills')

        try:
            if request.user.is_authenticated:
                # Update mode
                try:
                    profile = UserProfile.objects.get(email_address=request.user.email)
                    for key, value in basic_data.items():
                        setattr(profile, key, value)
                    
                    profile.skills = skills
                    if profile_photo:
                        profile.profile_photo = profile_photo
                    if resume:
                        profile.resume = resume
                    profile.save()

                    education = Education.objects.filter(user_profile=profile).first()
                    if education:
                        for key, value in education_data.items():
                            setattr(education, key, value)
                        education.save()
                    else:
                        Education.objects.create(user_profile=profile, **education_data)
                    
                    print(f"Profile and Education updated for: {request.user.email}")
                except UserProfile.DoesNotExist:
                    # Create mode if not exists (regular case for new registrations)
                    profile = UserProfile.objects.create(**basic_data, skills=skills, profile_photo=profile_photo, resume=resume)
                    profile.user = request.user # Ensure it's linked
                    profile.save()
                    Education.objects.create(user_profile=profile, **education_data)
                    print(f"New Profile and Education created for (auth): {request.user.email}")
            else:
                # Create mode - this should rarely happen if they are logged in during registration
                if not basic_data:
                    return JsonResponse({'status': 'error', 'message': 'Registration session expired. Please start over.'}, status=400)
                
                profile = UserProfile.objects.create(**basic_data, skills=skills, profile_photo=profile_photo, resume=resume)
                Education.objects.create(user_profile=profile, **education_data)
                print(f"New Profile and Education created for (non-auth): {basic_data.get('email_address')}")
            
            # Clear session
            if 'basic_data' in request.session: del request.session['basic_data']
            if 'education_data' in request.session: del request.session['education_data']
            
            msg = 'Profile Updated Successfully!' if request.user.is_authenticated else 'Registration Completed Successfully!'
            return JsonResponse({'status': 'success', 'message': msg})

        except Exception as e:
            print(f"Final Step Error: {str(e)}")
            return JsonResponse({'status': 'error', 'message': f'Server error: {str(e)}'}, status=500)

    return render(request, 'registation2/skills.html', {'profile': profile})

def about_us(request):
    return render(request, 'Aboutus/us.html')

def contact_us(request):
    if request.method == 'POST':
        data = request.POST
        ContactMessage.objects.create(
            name=data.get('name'),
            email=data.get('email'),
            subject=data.get('subject'),
            message=data.get('message')
        )
        return JsonResponse({'status': 'success', 'message': 'Message sent successfully!'})
    return render(request, 'contact us/contact.html')

@login_required
def dashboard(request):
    try:
        profile = UserProfile.objects.get(email_address=request.user.email)
    except UserProfile.DoesNotExist:
        profile = None

    # Calculate Profile Completion (Simple Version)
    completion = 0
    if profile:
        steps = [
            profile.full_name, profile.skills, profile.profile_photo, profile.resume,
            profile.github_url, profile.bio
        ]
        completed_steps = len([s for s in steps if s])
        completion = int((completed_steps / len(steps)) * 100)
        profile.profile_completion_percentage = completion
        profile.save()

    # Get Stats
    stats = {
        'completion': completion,
        'recommended_count': Job.objects.count(),
        'applied_count': Application.objects.filter(user=request.user).count(),
        'saved_count': SavedJob.objects.filter(user=request.user).count(),
    }

    # Get Recommendations natively
    from jobs.models import JobRecommendation
    from jobs.utils.ai_matcher import update_job_recommendations
    
    # Refresh recommendations for the user on dashboard load (or only once ideally, doing it here for simplicity)
    if profile:
        update_job_recommendations(request.user)
    
    # Fetch top recommended jobs
    recommended_jobs = JobRecommendation.objects.filter(user=request.user).order_by('-match_percentage')[:4]

    return render(request, 'dashboard/dashboard.html', {
        'profile': profile,
        'stats': stats,
        'recommended_jobs': recommended_jobs
    })

@login_required
def profile(request):
    try:
        profile = UserProfile.objects.get(email_address=request.user.email)
        education = Education.objects.filter(user_profile=profile).first()
    except UserProfile.DoesNotExist:
        profile = None
        education = None

    if request.method == 'POST':
        if not profile:
             profile = UserProfile.objects.create(user=request.user, email_address=request.user.email)
        
        # Update User model
        request.user.first_name = request.POST.get('first_name', request.user.first_name)
        request.user.last_name = request.POST.get('last_name', request.user.last_name)
        request.user.save()

        # Update UserProfile model (System B)
        profile.full_name = f"{request.user.first_name} {request.user.last_name}".strip()
        profile.mobile_number = request.POST.get('phone', profile.mobile_number)
        profile.current_location = request.POST.get('location', profile.current_location)
        profile.bio = request.POST.get('bio', profile.bio)
        profile.github_url = request.POST.get('github', profile.github_url)
        profile.linkedin_url = request.POST.get('linkedin', profile.linkedin_url)
        profile.save()

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success', 'message': 'Profile updated successfully!'})
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')

    return render(request, 'profile page/profile.html', {'profile': profile, 'education': education})

@login_required
def about_user(request):
    try:
        profile = UserProfile.objects.get(email_address=request.user.email)
    except UserProfile.DoesNotExist:
        profile = None
    
    if request.method == 'POST':
        # Custom logic to save 'About User' details can be added here
        return JsonResponse({'status': 'success', 'message': 'Data saved'})
    return render(request, 'Aboutuser/about.html', {'profile': profile})

@login_required
def resume_analysis(request):
    return render(request, 'resume analysis/index.html')

from core.models import JobRecommendation

@login_required
def career_advice(request):
    recommendations = JobRecommendation.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'carrier.html', {'recommendations': recommendations})

@login_required
def find_jobs(request):
    query = request.GET.get('q', '')
    location = request.GET.get('location', '')
    job_type = request.GET.get('type', '')
    
    jobs = Job.objects.all()
    if query:
        jobs = jobs.filter(title__icontains=query) | jobs.filter(company__icontains=query)
    if location:
        jobs = jobs.filter(location__icontains=location)
    if job_type:
        jobs = jobs.filter(job_type=job_type)

    saved_job_ids = []
    if request.user.is_authenticated:
        saved_job_ids = list(SavedJob.objects.filter(user=request.user).values_list('job_id', flat=True))

    return render(request, 'dashboard/find_jobs.html', {
        'jobs': jobs,
        'saved_job_ids': saved_job_ids
    })

@login_required
def toggle_save_job(request, job_id):
    try:
        job = Job.objects.get(id=job_id)
        saved_job, created = SavedJob.objects.get_or_create(user=request.user, job=job)
        if not created:
            saved_job.delete()
            status = 'removed'
        else:
            status = 'saved'
        return JsonResponse({'status': 'success', 'job_status': status})
    except Job.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Job not found'})

@login_required
def apply_job(request, job_id):
    try:
        job = Job.objects.get(id=job_id)
        
        # Check if already applied
        if Application.objects.filter(user=request.user, job=job).exists():
            return JsonResponse({'status': 'error', 'message': 'You have already applied to this job.'})
            
        Application.objects.create(user=request.user, job=job)
        Notification.objects.create(
            user=request.user,
            message=f"You successfully applied to {job.title} at {job.company}."
        )
        return JsonResponse({'status': 'success', 'message': 'Application submitted'})
    except Job.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Job not found'})

@login_required
def ai_chat_response(request):
    user_query = request.GET.get('query', '').lower()
    
    # Simple mock AI logic
    if 'skill' in user_query:
        response = "To improve your profile, I recommend learning React or Cloud Computing (AWS/Azure)."
    elif 'job' in user_query or 'recommend' in user_query:
        response = "I've found 4 new job matches for you! Check your dashboard for details."
    elif 'salary' in user_query:
        response = "Based on your role, typical salaries range from ₹6L to ₹12L per annum."
    else:
        response = "I'm your AI Career Assistant. Ask me about skills, jobs, or career paths!"
        
    return JsonResponse({'status': 'success', 'response': response})

@login_required
def applications_tracker(request):
    applications = Application.objects.filter(user=request.user).select_related('job')
    return render(request, 'dashboard/application_tracker.html', {'applications': applications})

from django.views.decorators.http import require_POST
import json

@login_required
@require_POST
def update_application_status(request, app_id):
    try:
        data = json.loads(request.body)
        new_status = data.get('status')
        if not new_status:
            return JsonResponse({'status': 'error', 'message': 'No status provided'})
            
        app = Application.objects.get(id=app_id, user=request.user)
        app.status = new_status
        app.save()
        return JsonResponse({'status': 'success'})
    except Application.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Application not found'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
