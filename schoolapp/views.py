from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Grade, Subject, Student, UserProfile
from django.contrib.auth.models import User
from django.db.models import Q


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('admin_dashboard')
            else:
                try:
                    UserProfile.objects.get(user=user)
                    return redirect('student_dashboard')
                except UserProfile.DoesNotExist:
                    messages.error(request, "UserProfile not found. Please contact admin.")
                    return redirect('login')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('student_dashboard')

    search_query = request.GET.get('search', '')

    if search_query:
        students = Student.objects.filter(
            Q(name__icontains=search_query) | Q(email__icontains=search_query)
        )
    else:
        students = Student.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')

        user = User.objects.create_user(username=email, email=email, password='student123')
        profile = UserProfile.objects.create(user=user)
        Student.objects.create(name=name, email=email, user=user)
        messages.success(request, f"Student {name} added successfully!")
        return redirect('admin_dashboard')

    return render(request, 'admin_dashboard.html', {'students': students})


def edit_student(request, student_id):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('login')

    student = get_object_or_404(Student, id=student_id)

    if request.method == 'POST':
        student.name = request.POST.get('name')
        student.email = request.POST.get('email')
        student.user.username = student.email
        student.user.email = student.email
        student.user.save()
        student.save()
        messages.success(request, "Student updated successfully!")
        return redirect('admin_dashboard')

    return render(request, 'edit_student.html', {'student': student})


def delete_student(request, student_id):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('login')

    student = get_object_or_404(Student, id=student_id)
    student.user.delete()
    student.delete()
    messages.success(request, "Student deleted successfully!")
    return redirect('admin_dashboard')


def edit_grade(request, grade_id):
    grade = Grade.objects.get(id=grade_id)
    if request.method == 'POST':
        grade.grade_type = request.POST.get('grade_type')
        grade.score = request.POST.get('score')
        grade.save()
        return redirect('student_detail', grade.subject.student.id)

def delete_grade(request, grade_id):
    grade = Grade.objects.get(id=grade_id)
    student_id = grade.subject.student.id
    grade.delete()
    return redirect('student_detail', student_id)


from django.shortcuts import render, get_object_or_404, redirect
from .models import Subject

def edit_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)

    if request.method == 'POST':
        new_name = request.POST.get('name')
        if new_name:
            subject.name = new_name
            subject.save()
            return redirect('student_detail', student_id=subject.student.id)

    return render(request, 'edit_subject.html', {'subject': subject})


def student_detail(request, student_id):
    if not request.user.is_authenticated:
        return redirect('login')

    student = get_object_or_404(Student, id=student_id)
    subjects = Subject.objects.filter(student=student)
    grades = Grade.objects.filter(subject__student=student)

    if request.method == 'POST':
        if 'subject_name' in request.POST:
            subject_name = request.POST.get('subject_name')
            grade_type = request.POST.get('grade_type')
            grade_value = request.POST.get('grade_value')

            if subject_name and grade_type and grade_value:
                subject = Subject.objects.create(name=subject_name, student=student)
                Grade.objects.create(subject=subject, grade_type=grade_type, score=grade_value)
                messages.success(request, f"Added subject '{subject_name}' with initial grade.")
                return redirect('student_detail', student_id=student.id)

        elif 'grade_subject' in request.POST:
            subject_id = request.POST.get('grade_subject')
            grade_type = request.POST.get('grade_type')
            score = request.POST.get('score')

            if subject_id and grade_type and score:
                try:
                    subject = Subject.objects.get(id=subject_id, student=student)
                    Grade.objects.create(subject=subject, grade_type=grade_type, score=score)
                    messages.success(request, f"Added {grade_type} grade to {subject.name}")
                except Subject.DoesNotExist:
                    messages.error(request, "Invalid subject.")
                return redirect('student_detail', student_id=student.id)

    return render(request, 'student_detail.html', {
        'student': student,
        'subjects': subjects,
        'grades': grades
    })

def student_dashboard(request):
    if not request.user.is_authenticated or request.user.is_superuser:
        return redirect('login')

    try:
        profile = UserProfile.objects.get(user=request.user)
        student = Student.objects.filter(user=request.user).first()
        subjects = Subject.objects.filter(student=student)
        grades = Grade.objects.filter(subject__student=student)
    except (UserProfile.DoesNotExist, Student.DoesNotExist):
        messages.error(request, "Student profile not found.")
        return redirect('logout')

    return render(request, 'student_dashboard.html', {
        'student': student,
        'subjects': subjects,
        'grades': grades
    })

