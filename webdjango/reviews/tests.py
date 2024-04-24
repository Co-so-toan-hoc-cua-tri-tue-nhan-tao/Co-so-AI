from django.test import TestCase




"""
from django.test import TestCase
from .models import Wine, Review, Cluster
from django.contrib.auth.models import User

class YourAppNameTestCase(TestCase):
    
    def setUp(self):
        # Tạo các đối tượng cho các bài kiểm tra
        self.user1 = User.objects.create(username='user1')
        self.user2 = User.objects.create(username='user2')
        self.wine1 = Wine.objects.create(name='Wine 1')
        self.wine2 = Wine.objects.create(name='Wine 2')
        Review.objects.create(user_name='user1', wine=self.wine1, rating=4)
        Review.objects.create(user_name='user2', wine=self.wine1, rating=5)

    def test_review_str_method(self):
        # Kiểm tra phương thức __str__ của đối tượng Review
        review = Review.objects.get(rating=4)
        self.assertEqual(str(review), f"{review.wine.name} - {review.rating}")

    def test_cluster_member_display(self):
        # Kiểm tra hiển thị các thành viên của cụm
        cluster = Cluster.objects.create(name='Test Cluster')
        cluster.users.add(self.user1)
        cluster.users.add(self.user2)
        self.assertEqual(cluster.get_members(), "user1\nuser2")

    # Bổ sung các hàm kiểm tra khác nếu cần thiết

"""
