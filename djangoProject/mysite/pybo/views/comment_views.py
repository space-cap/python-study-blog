from django.shortcuts import get_object_or_404, redirect
from ..models import Question, Answer, Comment
from ..forms import QuestionForm, AnswerForm, CommentForm
from django.utils import timezone


def comment_add(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.question = question
            comment.save()
    
    return redirect('pybo:detail', question_id=question.id)

