
from django.db.models import Sum

def calculate_term_average(student_profile, subject, term):
    """
    Aggregates all CA and Exam scores for a student in a specific term, 
    applying the Zambian weighting criteria automatically.
    """
    grades = StudentGrade.objects.filter(
        student=student_profile,
        assessment__subject=subject,
        assessment__term=term
    )
    
    # Using the property method defined in the model to sum the weighted contributions
    final_term_mark = sum(grade.weighted_score for grade in grades)
    
    return min(final_term_mark, 100) # Ensure it never exceeds 100%
