from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm
from app.models import User

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('canvas.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('用户名或密码错误', 'danger')
            return redirect(url_for('auth.login'))
        
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or not next_page.startswith('/'):
            next_page = url_for('canvas.index')
        return redirect(next_page)
    
    return render_template('auth/login.html', title='登录', form=form)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('canvas.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('注册成功！请登录', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', title='注册', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('canvas.index'))

@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('canvas.index'))
    
    resetrequestform = ResetPasswordRequestForm()
    if resetrequestform.validate_on_submit():
        user = User.query.filter_by(username=resetrequestform.username.data).first()
        if user is None:
            flash('用户还未注册', 'danger')
        else:
            return redirect(url_for('auth.reset_password', user_id = user.id))
    
    return render_template('auth/reset_password_request.html', 
                           title='输入用户名', 
                           form=resetrequestform)

@bp.route('/reset_password/<int:user_id>', methods=['GET', 'POST'])
def reset_password(user_id):
    """根据用户ID重置密码"""
    if current_user.is_authenticated:
        return redirect(url_for('canvas.index'))
    
    # 查找用户
    user = User.query.get(user_id)
    if user is None:
        flash('用户不存在', 'danger')
        return redirect(url_for('auth.reset_password_request'))
    
    # 创建重置密码表单
    resetform = ResetPasswordForm()
    
    if resetform.validate_on_submit():
        # 更新密码
        user.set_password(resetform.password.data)
        
        # 如果有记录最后修改时间的字段，可以更新
        # user.password_changed_at = datetime.utcnow()
        
        db.session.commit()
        
        flash('密码重置成功！请使用新密码登录', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/reset_password.html',
                           title='重置密码',
                           form=resetform,
                           username=user.username) 
