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
	def setup_chatbot_frame(self):
		self.chatbot_frame = QWidget(self.centralwidget)
		self.chat_input = QLineEdit(self.chatbot_frame)
		self.chat_button = QPushButton("Send", self.chatbot_frame)
		self.api_info_button = QPushButton("API Info", self.chatbot_frame)  # Nút mới

		# Tạo layout chính cho cửa sổ
		vbox_main = QVBoxLayout()
		vbox_main.addWidget(self.textEdit)

		# Tạo layout cho khung chat và nút gửi tin nhắn, nhưng ẩn nó ban đầu
		self.chatbot_frame.hide()
		hbox_chat = QHBoxLayout()
		hbox_chat.addWidget(self.chat_input)
		hbox_chat.addWidget(self.chat_button)
		hbox_chat.addWidget(self.api_info_button)  # Thêm nút mới vào layout
		self.chatbot_frame.setLayout(hbox_chat)
		vbox_main.addWidget(self.chatbot_frame)

		self.horizontalLayout.addLayout(vbox_main)

		# Kết nối sự kiện clicked của nút gửi tin nhắn
		self.chat_button.clicked.connect(self.send_message)

		# Kết nối sự kiện clicked của nút thông tin API
		self.api_info_button.clicked.connect(self.show_api_content)

		# Kết nối sự kiện enter của QLineEdit để gửi tin nhắn
		self.chat_input.returnPressed.connect(self.send_message)

def set_dark_mode(self):
    self.centralwidget.setStyleSheet("background-color: #333; color: #FFF;")
    self.textEdit.setStyleSheet("background-color: #333; color: #FFF;")
    self.menubar.setStyleSheet("background-color: #666; color: #FFF;")  # Đảo màu nền và màu chữ
    self.statusbar.setStyleSheet("background-color: #333; color: #FFF;")
    self.toolBar.setStyleSheet("background-color: #666; color: #FFF;")
    for action in self.toolBar.actions():
        action.setStyleSheet("color: #FFF;")

	def send_message(self):
		user_input = self.chat_input.text().strip()
		if user_input:
			try:
				response = openai.ChatCompletion.create(
					model="gpt-3.5-turbo-0125",
					messages=[
						{"role": "system", "content": "You are a helpful assistant."},
						{"role": "user", "content": user_input}
					],
					max_tokens=1000,
					api_key=config.API_KEY  # Sử dụng API từ cấu hình
				)
				text = response.choices[0].message["content"]
				self.textEdit.append(f"\nUser: {user_input}\nChatbot: {text}\n")
				self.chat_input.clear()
			except AuthenticationError as e:
				# Hiển thị cảnh báo lỗi
				QMessageBox.warning(self.centralwidget, 'Authentication Error', str(e))
				# Yêu cầu nhập API mới
				api_key, ok = QInputDialog.getItem(self.centralwidget, 'Enter API Key', 
													'Enter your API key:', self.previous_api_keys, editable=True)
				if ok:
					config.API_KEY = api_key
					if api_key not in self.previous_api_keys:
						self.previous_api_keys.append(api_key)
					# Thử lại gửi tin nhắn
					self.send_message()
			except Exception as e:
				# Xử lý các loại lỗi khác nếu cần
				QMessageBox.warning(self.centralwidget, 'Error', str(e))

def set_light_mode(self):
    self.centralwidget.setStyleSheet("")
    self.textEdit.setStyleSheet("")
    self.menubar.setStyleSheet("")
    self.statusbar.setStyleSheet("")
    self.toolBar.setStyleSheet("")
    for action in self.toolBar.actions():
        action.setStyleSheet("")

def start_spell_check_timer(self):
    if self.spell_check_checked:
        self.spell_check_timer.start(1000) 
def stop_spell_check_timer(self):
    self.spell_check_timer.stop() 

def check_spelling(self):
    self.spell_check_timer.stop()  # Dừng bộ đếm thời gian
    cursor = self.textEdit.textCursor()
    cursor_pos = cursor.position()  # Lưu lại vị trí của con trỏ

    # Lấy văn bản trong textEdit
    text = self.textEdit.toPlainText()

    # Tạo một danh sách để lưu trữ màu chữ của từng phần văn bản
    char_formats = []

    # Tách văn bản thành các từ và kiểm tra chính tả
    for start_pos, end_pos, word in self.iterate_words(text):
        if not self.spell_checker.check(word):
            # Nếu từ không đúng chính tả, lưu màu chữ hiện tại và áp dụng gạch chân nhiễu
            cursor.setPosition(start_pos)
            cursor.movePosition(QtGui.QTextCursor.Right, QtGui.QTextCursor.KeepAnchor, end_pos - start_pos)
            char_format = cursor.charFormat()
            char_formats.append((start_pos, char_format.foreground()))  # Lưu trữ màu chữ hiện tại
            char_format.setUnderlineStyle(QtGui.QTextCharFormat.SpellCheckUnderline)
            char_format.setUnderlineColor(Qt.red)  # Đặt màu gạch chân nhiễu là màu đỏ
            cursor.setCharFormat(char_format)
        else:
            char_formats.append(None)  # Không áp dụng gạch chân nhiễu, để màu chữ không thay đổi

    # Khôi phục màu chữ ban đầu cho các từ không cần áp dụng gạch chân nhiễu
    for i, char_format in enumerate(char_formats):
        if char_format is None:
            continue
        start_pos, color = char_format
        cursor.setPosition(start_pos)
        cursor.movePosition(QtGui.QTextCursor.Right, QtGui.QTextCursor.KeepAnchor, 1)
        char_format = cursor.charFormat()
        char_format.setForeground(color)  # Thiết lập màu chữ trở lại
        cursor.setCharFormat(char_format)

    # Khôi phục vị trí của con trỏ
    cursor.setPosition(cursor_pos)



def iterate_words(self, text):
    """
    Hàm này tách văn bản thành các từ và trả về vị trí bắt đầu và kết thúc của từ trong văn bản cùng với từ đó.
    """
    in_word = False
    start_pos = 0
    for pos, char in enumerate(text):
        if char.isalnum():
            if not in_word:
                start_pos = pos
                in_word = True
        else:
            if in_word:
                yield start_pos, pos, text[start_pos:pos]
                in_word = False
    if in_word:
        yield start_pos, len(text), text[start_pos:]
    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "About"))
        self.label.setText(_translate("Dialog", "<html><head/><body><p align=\"center\"><img src=\":/res/icons/text-editor.png\"/></p><p align=\"center\">Awasome Notepad</p></body></html>"))
        self.label_2.setText(_translate("Dialog", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">Author : Team-28-Software-Engineering</span></p><p align=\"center\"><span style=\" font-size:12pt;\">Build Date : 15-5-2024</span></p><p align=\"center\"><span style=\" font-size:12pt;\">Version : 1.0</span></p></body></html>"))

'''