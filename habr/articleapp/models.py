import uuid

from django.db import models
from authapp.models import User

class BaseModel(models.Model):
    """
    Global model. Set id and created_timestamp for all children models.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='id')
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Create Date')

    @classmethod
    def get_item_by_id(cls, search_id):
        return cls.objects.filter(id=search_id)


class Article(BaseModel):
    """
    Models for Articles
    """
    article_title = models.CharField(max_length=100, unique=True)
    article_subtitle = models.CharField(max_length=100, unique=True)
    article_main_img = models.ImageField(upload_to='article_images')
    article_text = models.TextField(max_length=300, verbose_name='Text Article')
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='Author article', related_name='article_author')


class ArticleLike(BaseModel):
    """
    Models for Articles Likes
    """
    article_to_like = models.ForeignKey(Article, on_delete=models.DO_NOTHING, verbose_name='Article for like', related_name='article_like')
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING, verbose_name='Like Author', related_name='like_author')


class ArticleComment(BaseModel):
    """
    Models for Articles Comments
    """
    article_to_comment = models.ForeignKey(Article, on_delete=models.DO_NOTHING, verbose_name='Article for comment', related_name='article_comment')
    comment_text = models.TextField(max_length=300, verbose_name='Comment text')
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING, verbose_name='Comment Author', related_name='comment_author')