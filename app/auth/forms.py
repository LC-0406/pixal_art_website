# app/auth/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
from app.models import User

class LoginForm(FlaskForm):
    """
    登录表单
    """
    username = StringField(
        '用户名',
        validators=[
            DataRequired(message='请输入用户名'),
            Length(min=3, max=20, message='用户名长度在3-20个字符之间')
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "请输入用户名",
            "autocomplete": "username"
        }
    )
    
    password = PasswordField(
        '密码',
        validators=[
            DataRequired(message='请输入密码'),
            Length(min=6, max=128, message='密码长度至少6位')
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "请输入密码",
            "autocomplete": "current-password"
        }
    )
    
    remember_me = BooleanField(
        '记住我',
        default=False,
        render_kw={"class": "form-check-input"}
    )
    
    submit = SubmitField(
        '登录',
        render_kw={"class": "btn btn-primary btn-block"}
    )


class RegistrationForm(FlaskForm):
    """
    注册表单
    """
    username = StringField(
        '用户名',
        validators=[
            DataRequired(message='请输入用户名'),
            Length(min=3, max=20, message='用户名长度在3-20个字符之间'),
            Regexp('^[a-zA-Z0-9_]+$', 
                  message='用户名只能包含字母、数字和下划线')
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "请输入用户名 (3-20个字符)",
            "autocomplete": "username"
        }
    )
    
    email = StringField(
        '邮箱',
        validators=[
            DataRequired(message='请输入邮箱'),
            #Email(message='请输入有效的邮箱地址'),
            Length(max=120, message='邮箱地址太长')
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "请输入邮箱地址",
            "autocomplete": "email"
        }
    )
    
    password = PasswordField(
        '密码',
        validators=[
            DataRequired(message='请输入密码'),
            Length(min=6, max=128, message='密码长度至少6位')
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "请输入密码 (至少6位)",
            "autocomplete": "new-password"
        }
    )
    
    password2 = PasswordField(
        '确认密码',
        validators=[
            DataRequired(message='请再次输入密码'),
            EqualTo('password', message='两次输入的密码不一致')
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "请再次输入密码",
            "autocomplete": "new-password"
        }
    )
    
    submit = SubmitField(
        '注册',
        render_kw={"class": "btn btn-success btn-block"}
    )
    
    def validate_username(self, username):
        """
        自定义验证：检查用户名是否已存在
        """
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('该用户名已被使用，请换一个')
    
    def validate_email(self, email):
        """
        自定义验证：检查邮箱是否已存在
        """
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('该邮箱已被注册，请使用其他邮箱')


class ChangePasswordForm(FlaskForm):
    """
    修改密码表单
    """
    old_password = PasswordField(
        '当前密码',
        validators=[DataRequired(message='请输入当前密码')],
        render_kw={
            "class": "form-control",
            "placeholder": "请输入当前密码"
        }
    )
    
    new_password = PasswordField(
        '新密码',
        validators=[
            DataRequired(message='请输入新密码'),
            Length(min=6, max=128, message='密码长度至少6位')
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "请输入新密码 (至少6位)"
        }
    )
    
    new_password2 = PasswordField(
        '确认新密码',
        validators=[
            DataRequired(message='请再次输入新密码'),
            EqualTo('new_password', message='两次输入的密码不一致')
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "请再次输入新密码"
        }
    )
    
    submit = SubmitField(
        '修改密码',
        render_kw={"class": "btn btn-warning"}
    )


class ResetPasswordRequestForm(FlaskForm):
    """
    重置密码请求表单
    """
    username = StringField(
        '用户名',
        validators=[
            DataRequired(message='请输入用户名')
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "请输入注册时使用的用户名"
        }
    )
    
    submit = SubmitField(
        '确认',
        render_kw={"class": "btn btn-primary"}
    )


class ResetPasswordForm(FlaskForm):
    """
    重置密码表单
    """
    password = PasswordField(
        '新密码',
        validators=[
            DataRequired(message='请输入新密码'),
            Length(min=6, max=128, message='密码长度至少6位')
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "请输入新密码 (至少6位)"
        }
    )
    
    password2 = PasswordField(
        '确认密码',
        validators=[
            DataRequired(message='请再次输入密码'),
            EqualTo('password', message='两次输入的密码不一致')
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "请再次输入密码"
        }
    )
    
    submit = SubmitField(
        '重置密码',
        render_kw={"class": "btn btn-success"}
    )


class ProfileForm(FlaskForm):
    """
    编辑个人资料表单
    """
    username = StringField(
        '用户名',
        validators=[
            DataRequired(message='请输入用户名'),
            Length(min=3, max=20, message='用户名长度在3-20个字符之间'),
            Regexp('^[a-zA-Z0-9_]+$', 
                  message='用户名只能包含字母、数字和下划线')
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "请输入用户名"
        }
    )
    
    email = StringField(
        '邮箱',
        validators=[
            DataRequired(message='请输入邮箱'),
            Email(message='请输入有效的邮箱地址'),
            Length(max=120, message='邮箱地址太长')
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "请输入邮箱地址"
        }
    )
    
    bio = StringField(
        '个人简介',
        validators=[Length(max=500, message='个人简介不能超过500字')],
        render_kw={
            "class": "form-control",
            "placeholder": "介绍一下你自己吧",
            "rows": 3
        }
    )
    
    submit = SubmitField(
        '保存修改',
        render_kw={"class": "btn btn-primary"}
    )
    
    def __init__(self, original_username, original_email, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email
    
    def validate_username(self, username):
        """
        自定义验证：检查用户名是否已存在（排除自己）
        """
        if username.data != self.original_username:
            user = User.query.filter_by(username=username.data).first()
            if user is not None:
                raise ValidationError('该用户名已被使用，请换一个')
    
    def validate_email(self, email):
        """
        自定义验证：检查邮箱是否已存在（排除自己）
        """
        if email.data != self.original_email:
            user = User.query.filter_by(email=email.data).first()
            if user is not None:
                raise ValidationError('该邮箱已被注册，请使用其他邮箱')