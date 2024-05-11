from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Review,Wine ,Cluster
from django.contrib.auth.models import User
from .forms import ReviewForm
from .suggestions import update_clusters
import datetime
from django.contrib.auth.decorators import login_required



def review_list(request):
    latest_review_list = Review.objects.order_by('-pub_date')[:9]
    context = {'latest_review_list':latest_review_list}
    return render(request, 'review_list.html', context)


def review_detail(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    return render(request, 'review_detail.html', {'review': review})


def wine_list(request):
    wine_list = Wine.objects.order_by('-name')
    context = {'wine_list':wine_list}
    return render(request, 'wine_list.html', context)


def wine_detail(request, wine_id):
    wine = get_object_or_404(Wine, pk=wine_id)
    form = ReviewForm()
    return render(request, 'wine_detail.html', {'wine': wine, 'form': form})

@login_required
def add_review(request, wine_id):
    wine = get_object_or_404(Wine, pk=wine_id)
    form = ReviewForm(request.POST)
    if form.is_valid():
        #rating = form.cleaned_data['rating']
        #comment = form.cleaned_data['comment']
        #user_name = request.user.username
        review = Review()
        review.wine = wine
        review.user_name = request.user.username
        review.rating = form.cleaned_data['rating']
        review.comment = form.cleaned_data['comment']
        review.pub_date = datetime.datetime.now()
        review.save()
        update_clusters()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('reviews:wine_detail', args=(wine.id,)))

    return render(request, 'wine_detail.html', {'wine': wine, 'form': form})


def user_review_list(request, username=None):
    if not username:
        username = request.user.username
    latest_review_list = Review.objects.filter(user_name=username).order_by('-pub_date')
    context = {'latest_review_list':latest_review_list, 'username':username}
    return render(request, 'user_review_list.html', context)


@login_required
def user_recommendation_list(request):

    # get request user reviewed wines
    user_reviews = Review.objects.filter(user_name=request.user.username).prefetch_related('wine')
    user_reviews_wine_ids = set(map(lambda x: x.wine.id, user_reviews))

    # get request user cluster name (just the first one righ now)
    try:
        user_cluster_name = \
            User.objects.get(username=request.user.username).cluster_set.first().name
    except: # if no cluster assigned for a user, update clusters
        update_clusters()
        user_cluster_name = \
            User.objects.get(username=request.user.username).cluster_set.first().name

    # get usernames for other memebers of the cluster
    user_cluster_other_members = \
        Cluster.objects.get(name=user_cluster_name).users \
            .exclude(username=request.user.username).all()
    other_members_usernames = set(map(lambda x: x.username, user_cluster_other_members))

    # get reviews by those users, excluding wines reviewed by the request user
    other_users_reviews = \
        Review.objects.filter(user_name__in=other_members_usernames) \
            .exclude(wine__id__in=user_reviews_wine_ids)
    other_users_reviews_wine_ids = set(map(lambda x: x.wine.id, other_users_reviews))

    # then get a wine list including the previous IDs, order by rating
    wine_list = sorted(
        list(Wine.objects.filter(id__in=other_users_reviews_wine_ids)),
        key=lambda x: x.average_rating(),
        reverse=True
    )

    return render(
        request,
        'user_recommendation_list.html',
        {'username': request.user.username,'wine_list': wine_list}
)

'''
def toggle_mode(self):
    if self.actionMode.isChecked():  # Nếu đang ở chế độ tối
        self.setStyleSheet("background-color: #222; color: #FFF;")
    else:  # Nếu đang ở chế độ sáng
        self.setStyleSheet("")  # Đặt lại stylesheet về mặc định

def fontColor(self):
    color = QtWidgets.QColorDialog.getColor(self.currentFontColor)
    if color.isValid():
        self.currentFontColor = color
        self.textEdit.setTextColor(color)

def highlight(self):
    color = QtWidgets.QColorDialog.getColor(self.currentHighlightColor)
    if color.isValid():
        self.currentHighlightColor = color
        self.textEdit.setTextBackgroundColor(color)

def search_text(self):
		search_text, ok = QtWidgets.QInputDialog.getText(self.centralwidget, 'Search Text', 'Enter text to search:')
		if ok and search_text:
			cursor = self.textEdit.textCursor()
			cursor.movePosition(QtGui.QTextCursor.Start)
			cursor = self.textEdit.document().find(search_text, cursor)
			if not cursor.isNull():
				self.textEdit.setTextCursor(cursor)
				self.textEdit.ensureCursorVisible()
def toggle_mode(self):
    if self.mode == 'light':
        self.mode = 'dark'
        self.set_dark_mode()
    else:
        self.mode = 'light'
        self.set_light_mode()

def set_dark_mode(self):
    self.centralwidget.setStyleSheet("background-color: #333; color: #FFF;")
    self.textEdit.setStyleSheet("background-color: #333; color: #FFF;")
    self.menubar.setStyleSheet("background-color: #666; color: #FFF;")  # Đảo màu nền và màu chữ
    self.statusbar.setStyleSheet("background-color: #333; color: #FFF;")
    self.toolBar.setStyleSheet("background-color: #666; color: #FFF;")
    for action in self.toolBar.actions():
        action.setStyleSheet("color: #FFF;")



def set_light_mode(self):
    self.centralwidget.setStyleSheet("")
    self.textEdit.setStyleSheet("")
    self.menubar.setStyleSheet("")
    self.statusbar.setStyleSheet("")
    self.toolBar.setStyleSheet("")
    for action in self.toolBar.actions():
        action.setStyleSheet("")

'''