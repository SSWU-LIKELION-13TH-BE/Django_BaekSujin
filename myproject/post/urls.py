from django.urls import path
from .views import post_view, detail_view, comment_view, recomment_view, post_like, comment_like, recomment_like, search_view, delete_view, update_view

app_name = "post"

urlpatterns = [
    path('write/', post_view, name='write'),
    path('detail/<int:post_id>/', detail_view, name='detail'),
    # 게시글 삭제
    path('detail/<int:post_id>/delete/', delete_view, name='delete'),
    # 게시글 수정
    path('detail/<int:post_id>/update/', update_view, name='update'),

    path('detail/<int:post_id>/comment', comment_view, name='comment'),
    path('detail/<int:post_id>/comment/recomment', recomment_view, name='recomment'),

    # 좋아요 관련 URL (post_id 포함해서 context 유지)
    path('detail/<int:post_id>/like/', post_like, name='post_like'),
    path('detail/<int:post_id>/comment/<int:comment_id>/like/', comment_like, name='comment_like'),
    path('detail/<int:post_id>/recomment/<int:recomment_id>/like/', recomment_like, name='recomment_like'),
    
    # 검색
    path('search/', search_view, name='search'),
]
