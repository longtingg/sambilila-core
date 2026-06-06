from django.shortcuts import render, get_object_or_40000, redirect
from django.views import View
from django.contrib import messages
from .models import AssessmentRecord, StudentGrade
from .forms import BaseStudentGradeFormSet
from core_models import StudentProfile # Imported from our core setup

class AssessmentGradeInputView(View):
    def get(self, request, assessment_id):
        assessment = get_object_or_404(AssessmentRecord, pk=assessment_id)
        # Fetch all students currently assigned to this specific class
        students = StudentProfile.objects.filter(current_class=assessment.academic_class).select_related('user')
        
        # Pull existing grades or build an initial dataset structure for missing ones
        initial_data = []
        existing_grades = StudentGrade.objects.filter(assessment=assessment).values_list('student_id', flat=True)
        
        for student in students:
            if student.id not in existing_grades:
                # If a student doesn't have a record yet, instantiate a placeholder
                StudentGrade.objects.create(student=student, assessment=assessment, raw_score=0.0)
        
        # Query the exact queryset to feed directly into the formset matrix
        queryset = StudentGrade.objects.filter(assessment=assessment).order_by('student__user__last_name')
        formset = BaseStudentGradeFormSet(queryset=queryset)
        
        context = {
            'assessment': assessment,
            'formset': formset,
            'zipped_data': zip(students, formset)
        }
        return render(request, 'assessments/grade_input.html', context)

    def post(self, request, assessment_id):
        assessment = get_object_or_404(AssessmentRecord, pk=assessment_id)
        queryset = StudentGrade.objects.filter(assessment=assessment)
        
        formset = BaseStudentGradeFormSet(request.POST, queryset=queryset)
        if formset.is_valid():
            formset.save()
            messages.success(request, f"Continuous Assessment grades for '{assessment.title}' successfully updated!")
            return redirect('assessment_detail', assessment_id=assessment.id)
        
        messages.error(request, "There was an issue validation error on some scores. Please check and retry.")
        return render(request, 'assessments/grade_input.html', {'assessment': assessment, 'formset': formset})
