from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)  # unique names for categories

    def __str__(self):
        return self.name


class Question(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="questions")
    question_text = models.CharField(max_length=300, default="Example question")  # default to avoid migration issues
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
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    score = models.IntegerField()
    total = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Attempt on {self.category.name} - Score: {self.score}/{self.total} at {self.timestamp}"
