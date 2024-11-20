from django.shortcuts import get_object_or_404, redirect
from django.contrib.contenttypes.models import ContentType
from .models import Question, Answer, Comment

def add_comment(request, content_type_id, object_id):
    if request.method == 'POST':
        content_type = get_object_or_404(ContentType, id=content_type_id)
        content_object = content_type.get_object_for_this_type(id=object_id)
        content = request.POST.get('content')
        author = request.user

        # 댓글 생성
        Comment.objects.create(
            content_type=content_type,
            object_id=object_id,
            content=content,
            author=author
        )
        # 리디렉션 처리
        return redirect('app_name:detail', pk=object_id)





