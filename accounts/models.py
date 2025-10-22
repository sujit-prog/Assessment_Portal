from django.db import models
import uuid
import random

# Create your models here.
class BaseModel(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Category(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name

class Question(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    question = models.CharField(max_length=255)
    marks = models.IntegerField(default=1)
    difficulty = models.CharField(
        max_length=50, 
        choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')]
    )

    def __str__(self):
        return self.question

    def get_answers(self):
        # Get all answer objects related to this question
        answers_objs = list(Answer.objects.filter(question=self))
        random.shuffle(answers_objs)  # Shuffle the answers for randomness
        
        data = []
        for answer_obj in answers_objs:
            data.append({
                'answer': answer_obj.answer,
                'is_correct': answer_obj.is_correct

            })
        return data

class Answer(BaseModel):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_answers')
    answer = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.answer

