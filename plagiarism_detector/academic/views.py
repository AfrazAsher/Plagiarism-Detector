# from django.contrib.auth import login, authenticate
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from django.shortcuts import render, redirect
# from django.http import HttpResponse
# from django.contrib.auth.decorators import login_required
# from .models import UserProfile

# def register(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             user_profile = UserProfile(user=user)
#             user_profile.is_student = 'student' in request.POST
#             user_profile.is_teacher = 'teacher' in request.POST
#             user_profile.save()
#             username = form.cleaned_data.get('username')
#             raw_password = form.cleaned_data.get('password1')
#             user = authenticate(username=username, password=raw_password)
#             login(request, user)
#             return redirect('home')
#     else:
#         form = UserCreationForm()
#     return render(request, 'academic/register.html', {'form': form})

# def login_user(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 if hasattr(user, 'userprofile'):
#                     if user.userprofile.is_teacher:
#                         return redirect('teacher_dashboard')
#                     elif user.userprofile.is_student:
#                         return redirect('student_dashboard')
#                 return redirect('home')
#             else:
#                 return HttpResponse("Invalid username or password.")
#         else:
#             return HttpResponse("Invalid username or password.")
#     else:
#         form = AuthenticationForm()
#     return render(request, 'academic/login.html', {'form': form})

# @login_required
# def teacher_dashboard(request):
#     return render(request, 'academic/teacher_dashboard.html')

# @login_required
# def student_dashboard(request):
#     return render(request, 'academic/student_dashboard.html')


### New Code for PyMongo

# academic/views.py
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import RegistrationForm, AssignmentForm
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from .forms import CourseForm, AssignmentForm, AddStudentForm, SubmissionForm
from .models import Course, Assignment, Submission, UserProfile#StudentAssignment, PlagiarismReport
from .plagiarism_detection import compare_assignments
from django.contrib import messages
from django.core.files.storage import default_storage


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'academic/register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if hasattr(user, 'userprofile'):
                    if user.userprofile.is_teacher:
                        return redirect('teacher_dashboard')
                    elif user.userprofile.is_student:
                        return redirect('student_dashboard')
                return redirect('home')
            else:
                return HttpResponse("Invalid username or password.")
        else:
            return HttpResponse("Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'academic/login.html', {'form': form})

def logout_user(request):
    logout(request)
    return redirect('home')

@login_required
def teacher_dashboard(request):
    return render(request, 'academic/teacher_dashboard.html')

@login_required
def list_assignments(request):
    assignments = Assignment.objects.all()
    return render(request, 'academic/list_assignments.html', {'assignments': assignments})

# @login_required
# def student_dashboard(request):
#     user_profile = UserProfile.objects.get(user=request.user)
#     # Assuming `enrolled_courses` is a many-to-many field linking users to courses
#     courses = user_profile.user.enrolled_courses.all()

#     # Optionally, you could fetch assignments directly if needed
#     # This could be useful if you want to show assignments directly on the dashboard without further navigation
#     assignments_by_course = {
#         course.id: list(Assignment.objects.filter(course=course).values(
#             'title', 'description', 'due_date', 'submission_format', 'max_marks', 'attachments'))
#         for course in courses
#     }

#     return render(request, 'academic/student_dashboard.html', {
#         'courses': courses,
#         'assignments_by_course': assignments_by_course
#     })

# @login_required
# def student_dashboard(request):
#     user_profile = UserProfile.objects.get(user=request.user)
#     courses = user_profile.user.enrolled_courses.all()
#     return render(request, 'academic/student_dashboard.html', {
#         'courses': courses
#     })
    
# @login_required
# def student_dashboard(request):
#     user_profile = UserProfile.objects.get(user=request.user)
#     courses = user_profile.user.enrolled_courses.all()
#     assignments_by_course = {
#         course: course.assignments.all()
#         for course in courses
#     }
#     return render(request, 'academic/student_dashboard.html', {
#         'courses': courses,
#         'assignments_by_course': assignments_by_course
#     })

# @login_required
# def student_dashboard(request):
#     user_profile = UserProfile.objects.get(user=request.user)
#     courses = user_profile.user.enrolled_courses.all()
#     student_assignments = Submission.objects.filter(student=request.user).select_related('assignment__course')

#     assignments_by_course = {}
#     for assignment in student_assignments:
#         course = assignment.assignment.course
#         if course not in assignments_by_course:
#             assignments_by_course[course] = []
#         assignments_by_course[course].append(assignment)

#     return render(request, 'academic/student_dashboard.html', {
#         'courses': courses,
#         'assignments_by_course': assignments_by_course
#     })

# @login_required
# def student_dashboard(request):
#     user_profile = UserProfile.objects.get(user=request.user)
#     courses = user_profile.user.enrolled_courses.all()
#     student_assignments = Submission.objects.filter(student=request.user).select_related('assignment__course')

#     assignments_by_course = {}
#     for sa in student_assignments:
#         course = sa.assignment.course
#         if course not in assignments_by_course:
#             assignments_by_course[course] = []
#         assignments_by_course[course].append(sa)

#     return render(request, 'academic/student_dashboard.html', {
#         'courses': courses,
#         'assignments_by_course': assignments_by_course
#     })
# def student_dashboard(request):
#     # Assuming 'Course' and 'Submission' are your model names
#     courses = Course.objects.prefetch_related('submissions').all()
#     # Organize data
#     courses_data = []
#     for course in courses:
#         submissions = Submission.objects.filter(course=course)
#         courses_data.append({
#             'course': course,
#             'submissions': submissions
#         })
    
#     context = {'courses_data': courses_data}
#     return render(request, 'academic/student_dashboard.html', context)

def student_dashboard(request):
    courses = Course.objects.prefetch_related('assignments__submissions').filter(students=request.user)
    return render(request, 'academic/student_dashboard.html', {'courses': courses})

# @login_required
# def upload_submission(request, submission_id):
#     submission = get_object_or_404(Submission, id=submission_id, student=request.user)
#     if request.method == 'POST':
#         form = SubmissionForm(request.POST, request.FILES, instance=submission)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Assignment uploaded successfully.")
#             return redirect('student_dashboard')
#     else:
#         form = SubmissionForm(instance=submission)
#     return render(request, 'academic/upload_form.html', {'form': form})

def upload_submission(request, assignment_id):
    if request.method == 'POST':
        try:
            assignment = Assignment.objects.get(id=assignment_id)
            submission, created = Submission.objects.get_or_create(
                student=request.user,
                assignment=assignment,
                defaults={'submitted_file': request.FILES.get('submitted_file')}
            )

            if not created and request.FILES.get('submitted_file'):
                # Delete the previous file if it exists to avoid storage overflow
                if submission.submitted_file:
                    default_storage.delete(submission.submitted_file.path)
                submission.submitted_file = request.FILES['submitted_file']
                submission.save()

            print('Your file has been successfully uploaded.')
        except Exception as e:
            print(f'Error uploading file: {str(e)}')

        # Redirect to the student_dashboard
        return redirect('student_dashboard')  # Ensure 'student_dashboard' is correctly named in your URL configuration

    # If not a POST request, redirect to the dashboard or appropriate page
    return redirect('student_dashboard')

    
@login_required
def get_assignments_for_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    assignments = Assignment.objects.filter(course=course).values(
        'title', 'description', 'due_date', 'submission_format', 'max_marks', 'attachments'
    )
    return JsonResponse(list(assignments), safe=False)
    
def home(request):
    return render(request, 'academic/home.html')

@login_required
def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            new_course = form.save(commit=False)
            new_course.teacher = request.user
            new_course.save()
            return redirect('teacher_dashboard')
    else:
        form = CourseForm()
    return render(request, 'academic/create_course.html', {'form': form})

# @login_required
# def create_assignment(request, course_id):
#     course = get_object_or_404(Course, id=course_id, teacher=request.user)
#     if request.method == 'POST':
#         form = AssignmentForm(request.POST, request.FILES)
#         if form.is_valid():
#             new_assignment = form.save(commit=False)
#             new_assignment.course = course
#             new_assignment.save()
#             return redirect('course_details', course_id=course_id)
#     else:
#         form = AssignmentForm()
#     return render(request, 'academic/create_assignment.html', {'form': form, 'course': course})

@login_required
def manage_courses(request):
    # Fetch courses that the current user is teaching
    courses = Course.objects.filter(teacher=request.user)
    return render(request, 'academic/manage_courses.html', {'courses': courses})

def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    form = CourseForm(request.POST, instance=course)
    if request.method == 'POST':
        #form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('manage_courses')
    else:
        form = CourseForm(instance=course)
    return render(request, 'academic/edit_course.html', {'form': form})

def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    course.delete()
    return redirect('manage_courses')

@login_required
def view_assignments(request):
    teacher = request.user
    courses = Course.objects.filter(teacher=teacher)
    assignments = Assignment.objects.filter(course__in=courses)
    return render(request, 'academic/view_assignments.html', {'assignments': assignments})

@login_required
def plagiarism_reports(request):
    # Example: Fetching all reports or perform related logic
    reports = PlagiarismReport.objects.all()  # Adjust according to your model
    return render(request, 'academic/plagiarism_reports.html', {'reports': reports})

@login_required
def create_assignment(request):
    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            new_assignment = form.save(commit=False)
            new_assignment.teacher = request.user  # make sure your Assignment model can store the teacher
            new_assignment.save()
            return redirect('course_details', course_id=new_assignment.course.id)
    else:
        form = AssignmentForm()
    return render(request, 'academic/create_assignment.html', {'form': form})

@login_required
def course_details(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return redirect('teacher_dashboard')

# def generate_report(request, assignment_id):
#     # Fetch the assignment using the ID or return a 404 error if it doesn't exist
#     assignment = get_object_or_404(Assignment, pk=assignment_id)

#     # Retrieve all submissions for this assignment
#     submissions = Submission.objects.filter(assignment=assignment)

#     # Prepare to collect plagiarism reports
#     plagiarism_reports = []
#     total_submissions = len(submissions)
#     for i, submission in enumerate(submissions):
#         report = {'student': submission.student, 'file': submission.submitted_file.url, 'plagiarism': []}
#         for j in range(total_submissions):
#             if i != j:
#                 plagiarism_score = compare_assignments(submission.submitted_file.path, submissions[j].submitted_file.path)
#                 report['plagiarism'].append({
#                     'compared_with': submissions[j].student,
#                     'score': plagiarism_score
#                 })
        
#         # Calculate the average plagiarism and assign marks accordingly
#         average_plagiarism = sum([p['score'] for p in report['plagiarism']]) / len(report['plagiarism']) if report['plagiarism'] else 0
#         max_score = assignment.max_marks
#         report['final_marks'] = max_score * (1 - (average_plagiarism / 100))  # Deduct marks based on plagiarism percentage
#         plagiarism_reports.append(report)

#     context = {
#         'assignment': assignment,
#         'plagiarism_reports': plagiarism_reports,
#         'total_submissions': total_submissions,
#     }

#     return render(request, 'academic/assignment_report.html', context)

# def generate_report(request, assignment_id):
#     # Fetch the assignment using the ID or return a 404 error if it doesn't exist
#     assignment = get_object_or_404(Assignment, pk=assignment_id)

#     # Retrieve all submissions for this assignment
#     submissions = Submission.objects.filter(assignment=assignment)

#     # Prepare to collect plagiarism reports
#     results = []
#     total_submissions = len(submissions)
#     for i, submission in enumerate(submissions):
#         # Assume a function to calculate plagiarism score
#         plagiarism_scores = []
#         for j in range(total_submissions):
#             if i != j:
#                 plagiarism_score = compare_assignments(submission.submitted_file.path, submissions[j].submitted_file.path)
#                 plagiarism_scores.append(plagiarism_score)
        
#         # Calculate the average plagiarism
#         average_plagiarism = sum(plagiarism_scores) / len(plagiarism_scores) if plagiarism_scores else 0
#         deducted_marks = int(average_plagiarism)  # Simplified deduction calculation
#         results.append({
#             'assignment_name': assignment.title,
#             'student_name': submission.student.username,
#             'plagiarism_percentage': f"{average_plagiarism:.2f}%",
#             'deducted_marks': deducted_marks,
#             'file_url': submission.submitted_file.url
#         })

#     context = {
#         'assignment': assignment,
#         'results': results,
#         'total_submissions': total_submissions,
#     }

#     return render(request, 'academic/assignment_report.html', context)

def show_assignments(request, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    submissions = Submission.objects.filter(assignment=assignment)
    results = [{
        'student_name': submission.student.username,
        'assignment_name': assignment.title,
        'file_url': submission.submitted_file.url
    } for submission in submissions]

    context = {
        'assignment': assignment,
        'results': results,
    }

    return render(request, 'academic/assignment_report.html', context)



# def calculate_plagiarism(request, assignment_id):
#     if request.method == 'POST':
#         assignment = get_object_or_404(Assignment, pk=assignment_id)
#         submissions = Submission.objects.filter(assignment=assignment)
#         results = []
#         total_submissions = len(submissions)

#         for i, submission in enumerate(submissions):
#             plagiarism_scores = []
#             for j in range(total_submissions):
#                 if i != j:
#                     plagiarism_score = compare_assignments(submission.submitted_file.path, submissions[j].submitted_file.path)
#                     plagiarism_scores.append(plagiarism_score)
            
#             average_plagiarism = sum(plagiarism_scores) / len(plagiarism_scores) if plagiarism_scores else 0
#             deducted_marks = int(average_plagiarism)  # Simplified deduction calculation

#             results.append({
#                 'assignment_name': assignment.title,
#                 'plagiarism_percentage': f"{average_plagiarism:.2f}%",
#                 'deducted_marks': deducted_marks,
#                 'file_url': submission.submitted_file.url
#             })

#         context = {
#             'assignment': assignment,
#             'results': results,
#         }

#         return render(request, 'academic/assignment_report.html', context)
#     else:
#         return redirect('show_assignments', assignment_id=assignment_id)

# def calculate_plagiarism(request, assignment_id):
#     if request.method == 'POST':
#         assignment = get_object_or_404(Assignment, pk=assignment_id)
#         submissions = Submission.objects.filter(assignment=assignment)
#         results = []
#         total_submissions = len(submissions)

#         for i, submission in enumerate(submissions):
#             plagiarism_scores = []
#             for j in range(total_submissions):
#                 if i != j:
#                     # Assuming compare_assignments returns a float percentage
#                     plagiarism_score = compare_assignments(
#                         submission.submitted_file.path,
#                         submissions[j].submitted_file.path
#                     )
#                     # Print the plagiarism score for debugging
#                     print(f"Plagiarism between file {submission.submitted_file.path} and {submissions[j].submitted_file.path} is {plagiarism_score}%")
                    
#                     # Ensure plagiarism_score is a float and add it to the list
#                     if isinstance(plagiarism_score, float):
#                         plagiarism_scores.append(plagiarism_score)

#             if plagiarism_scores:  # Check if there are scores to calculate average
#                 average_plagiarism = sum(plagiarism_scores) / len(plagiarism_scores)
#             else:
#                 average_plagiarism = 0

#             deducted_marks = int(average_plagiarism)  # Simplified deduction calculation

#             results.append({
#                 'student_name': submission.student.username,  # Assuming there's a student relation
#                 'assignment_name': assignment.title,
#                 'plagiarism_percentage': f"{average_plagiarism:.2f}%",
#                 'deducted_marks': deducted_marks,
#                 'file_url': submission.submitted_file.url
#             })

#         context = {
#             'assignment': assignment,
#             'results': results,
#         }
#         return render(request, 'academic/assignment_report.html', context)
#     else:
#         return redirect('show_assignments', assignment_id=assignment_id)

def calculate_plagiarism(request, assignment_id):
    if request.method == 'POST':
        assignment = get_object_or_404(Assignment, pk=assignment_id)
        submissions = Submission.objects.filter(assignment=assignment)

        # Read the submitted text or files
        texts = [open(sub.submitted_file.path).read() for sub in submissions]

        # Get the selected algorithm from the form
        selected_algorithm = request.POST.get('algorithm', 'jaccard')

        # Compare each submission against each other using the selected algorithm
        plagiarism_results = compare_assignments(texts, method=selected_algorithm)
        results = []

        for result in plagiarism_results:
            student1 = submissions[result['text1_index']].student.username
            student2 = submissions[result['text2_index']].student.username
            plagiarism_percentage = result['plagiarism_percentage']
            
            # Ensure the plagiarism percentage does not exceed 100%
            if plagiarism_percentage > 100:
                plagiarism_percentage = 100

            # Calculate the marks after plagiarism deduction
            total_marks = max(0, 100 - plagiarism_percentage)  # Prevent negative total marks

            results.append({
                'student1': student1,
                'student2': student2,
                'plagiarism_percentage': f"{plagiarism_percentage:.2f}%",
                'total_marks': f"{total_marks:.2f}",
                'file_url': submissions[result['text1_index']].submitted_file.url
            })

        context = {
            'assignment': assignment,
            'results': results,
        }
        return render(request, 'academic/assignment_results.html', context)
    else:
        return redirect('show_assignments', assignment_id=assignment_id)



@login_required
def add_students_to_course(request):
    if request.method == 'POST':
        course_id = request.POST.get('course')
        student_id = request.POST.get('student')
        course = Course.objects.get(id=course_id)
        student = UserProfile.objects.get(id=student_id).user

        # Ensure the student is not already enrolled
        if not course.students.filter(id=student_id).exists():
            course.students.add(student)
            messages.success(request, "Student added successfully.")
        else:
            messages.error(request, "Student is already enrolled in this course.")

        return redirect('add_students')

    # Fetch only users where UserProfile is_student is true
    students = UserProfile.objects.filter(is_student=True).select_related('user')
    courses = Course.objects.all()
    return render(request, 'academic/add_students.html', {'courses': courses, 'students': students})

# @login_required
# def add_students_to_course(request):
#     students = UserProfile.objects.filter(is_student=True).select_related('user')
#     courses = Course.objects.all()
#     return render(request, 'academic/add_students.html', {'courses': courses, 'students': students})

def edit_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    if request.method == 'POST':
        form = AssignmentForm(request.POST, instance=assignment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Assignment updated successfully!')
            return redirect('view_assignments')
    else:
        form = AssignmentForm(instance=assignment)
    return render(request, 'academic/edit_assignment.html', {'form': form})

def delete_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    assignment.delete()
    return redirect('view_assignments')


