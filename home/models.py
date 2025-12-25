from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="questions")
    question_text = models.CharField(max_length=300, default="Example question")
    option_a = models.CharField(max_length=200, default="Option A")
    option_b = models.CharField(max_length=200, default="Option B")
    option_c = models.CharField(max_length=200, default="Option C")
    option_d = models.CharField(max_length=200, default="Option D")
    correct_option = models.CharField(
        max_length=1,
        choices=[
            ('A', 'Option A'),
            ('B', 'Option B'),
            ('C', 'Option C'),
            ('D', 'Option D'),
        ],
        default='A'
    )

    def __str__(self):
        return f"{self.category.name}: {self.question_text[:40]}"

    
class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Add null=True temporarily
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    score = models.IntegerField()
    total = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    on_delete=models.CASCADE
    def __str__(self):
        return f"{self.user.username} - {self.category.name} - Score: {self.score}/{self.total} at {self.timestamp}"
    

    tab_switches = models.IntegerField(default=0, help_text='Number of times user switched tabs')
    fullscreen_exits = models.IntegerField(default=0, help_text='Number of times user exited fullscreen')
    is_flagged = models.BooleanField(default=False, help_text='Flagged for suspicious activity')
    
    def __str__(self):
        flag_indicator = "🚩" if self.is_flagged else ""
        return f"{flag_indicator}{self.user.username} - {self.category.name} - Score: {self.score}/{self.total} at {self.timestamp}"
    
    def save(self, *args, **kwargs):
        # Auto-flag if violations exceed thresholds
        if self.tab_switches > 3 or self.fullscreen_exits > 2:
            self.is_flagged = True
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['-timestamp']


    class Profile_Type(models.Model):
        user = models.OneToOneField(User, on_delete=models.CASCADE)
        role = models.CharField(max_length=10, choices=[
        ('teacher', 'Teacher'),
        ('student', 'Student')
    ])

    def __str__(self):
        return self.user.username