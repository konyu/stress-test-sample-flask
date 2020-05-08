from flask_login import UserMixin


class User(UserMixin):
    # ログインチェックで必要、
    def get_id(self):
        return 1