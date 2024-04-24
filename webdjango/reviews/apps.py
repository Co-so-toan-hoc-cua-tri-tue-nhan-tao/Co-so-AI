from django.apps import AppConfig


class ReviewsConfig(AppConfig):
    name = 'reviews'



"""
from django.apps import AppConfig
from django.db.models.signals import post_migrate

class ReviewsConfig(AppConfig):
    name = 'reviews'

    def ready(self):
        # Đăng ký hàm xử lý sự kiện cho sự kiện post_migrate
        post_migrate.connect(my_post_migrate_handler, sender=self)

def my_post_migrate_handler(sender, **kwargs):
    """
    Hàm xử lý sự kiện post_migrate.
    Thực hiện các hành động sau khi các migraions đã được áp dụng.
    """
    # Thêm bất kỳ hành động nào bạn muốn thực hiện ở đây
    pass

"""