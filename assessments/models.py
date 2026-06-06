from django.db import models
from django.core.validators import MinValueValidator
# FIX: Import from 'school.models' instead of 'accounts.models'
from school.models import StudentProfile, Subject, AcademicClass 

class AcademicTerm(models.Model):
    """
    Zambian schools operate on a 3-term calendar system.
    """
    TERM_CHOICES = [
        (1, 'Term 1'),
        (2, 'Term 2'),
        (3, 'Term 3'),
    ]
    academic_year = models.PositiveIntegerField()
    term_number = models.IntegerField(choices=TERM_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        unique_together = ('academic_year', 'term_number')

    def __str__(self):
        return f"Term {self.term_number} - {self.academic_year}"


class AssessmentType(models.Model):
    """
    Defines the categories of assessment according to the Zambian CA Scheme.
    """
    name = models.CharField(max_length=50, help_text="e.g., Formative Task, Mid-Term Test, End of Term Exam")
    weight_percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        help_text="The percentage weight this category holds towards the final term mark."
    )
    is_formative = models.BooleanField(
        default=True, 
        help_text="Check if this is a continuous/formative assessment."
    )

    def __str__(self):
        return f"{self.name} ({self.weight_percentage}%)"


class AssessmentRecord(models.Model):
    """
    The actual assessment task created by the teacher.
    """
    title = models.CharField(max_length=150, help_text="e.g., February Fractions Quiz, Term 1 Final")
    assessment_type = models.ForeignKey(AssessmentType, on_delete=models.PROTECT)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    academic_class = models.ForeignKey(AcademicClass, on_delete=models.CASCADE)
    term = models.ForeignKey(AcademicTerm, on_delete=models.CASCADE)
    
    max_score = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        help_text="The maximum achievable raw score for this specific task."
    )
    date_administered = models.DateField()

    def __str__(self):
        return f"{self.title} - {self.subject.code}"


class StudentGrade(models.Model):
    """
    The individual score obtained by a student on a specific AssessmentRecord.
    """
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="grades")
    assessment = models.ForeignKey(AssessmentRecord, on_delete=models.CASCADE, related_name="student_scores")
    
    raw_score = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    teacher_remarks = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        unique_together = ('student', 'assessment')

    def __str__(self):
        return f"{self.student.user.username}: {self.raw_score}/{self.assessment.max_score}"
    
    @property
    def weighted_score(self):
        """
        Calculates how much this specific score contributes to the term's final mark.
        """
        if self.assessment.max_score > 0:
            percentage_achieved = self.raw_score / self.assessment.max_score
            contribution = percentage_achieved * (self.assessment.assessment_type.weight_percentage / 100)
            return round(contribution * 100, 2)
        return 0
