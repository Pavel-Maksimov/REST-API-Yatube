from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField(verbose_name="Название группы",
                             max_length=200,
                             help_text="Придумайте название для группы")
    description = models.TextField(verbose_name="Описание",
                                   help_text="Опишите группу")

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(
        "Дата публикации", auto_now_add=True
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts"
    )
    group = models.ForeignKey(
        Group, on_delete=models.SET_NULL,
        related_name="posts",
        verbose_name="Группа",
        help_text=("Выберите группу, в которой будет опубликован пост"),
        blank=True,
        null=True
    )

    class Meta:
        ordering = ("-pub_date",)

    def __str__(self):
        return (f'Пост {self.post.id} пользователя'
                f'{self.author}, создана {self.created}')


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments"
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments"
    )
    text = models.TextField()
    created = models.DateTimeField(
        "Дата добавления", auto_now_add=True, db_index=True
    )

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return (f"Коментарий пользователя {self.author} к посту"
                f"{self.post.id}, создана {self.created}")


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="follower")
    following = models.ForeignKey(User, on_delete=models.CASCADE,
                                  related_name="following")

    class Meta:
        models.UniqueConstraint(
            fields=['user', 'following'],
            name='unique_follow'
        )

        def __str__(self):
            return f"Пописка позоателя {self.user} на автора {self.following}"
