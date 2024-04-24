from django.apps import AppConfig


class ReviewsConfig(AppConfig):
    name = 'reviews'

"""
from django.apps import AppConfig

class ReviewsConfig(AppConfig):
    name = 'reviews'

    def ready(self):
        # Gọi hàm cập nhật cụm khi ứng dụng sẵn sàng
        update_clusters()
"""
