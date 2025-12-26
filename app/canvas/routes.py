from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.canvas import bp
from app.models import Canvas
import json

@bp.route('/')
def index():
    if current_user.is_authenticated:
        canvases = current_user.canvases.order_by(Canvas.updated_at.desc()).all()
        return render_template('canvas/index.html', title='我的画布', canvases=canvases)
    public_canvases = Canvas.query.filter_by(is_public=True).all()
    return render_template('canvas/index.html', title='像素画', public_canvases=public_canvases)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        title = request.form.get('title', '未命名画布')
        width = int(request.form.get('width', 32))
        height = int(request.form.get('height', 32))
        is_public = request.form.get('is_public') == 'on'
        
        # 创建空白画布数据
        grid_data = json.dumps([[None for _ in range(width)] for _ in range(height)])
        
        canvas = Canvas(
            title=title,
            width=width,
            height=height,
            grid_data=grid_data,
            is_public=is_public,
            user_id=current_user.id
        )
        
        db.session.add(canvas)
        db.session.commit()
        flash('画布创建成功！', 'success')
        return redirect(url_for('canvas.edit', canvas_id=canvas.id))
    
    return render_template('canvas/create.html', title='创建画布')

@bp.route('/canvas/<int:canvas_id>')
def view(canvas_id):
    canvas = Canvas.query.get_or_404(canvas_id)
    
    # 检查权限
    if not canvas.is_public and (not current_user.is_authenticated or canvas.user_id != current_user.id):
        flash('无权访问此画布', 'danger')
        return redirect(url_for('canvas.index'))
    
    return render_template('canvas/view.html', 
                         title=canvas.title, 
                         canvas=canvas)

@bp.route('/canvas/<int:canvas_id>/edit')
@login_required
def edit(canvas_id):
    canvas = Canvas.query.get_or_404(canvas_id)
    
    if canvas.user_id != current_user.id:
        flash('无权编辑此画布', 'danger')
        return redirect(url_for('canvas.index'))
    
    return render_template('canvas/edit.html', 
                         title=f'编辑 - {canvas.title}', 
                         canvas=canvas,
                         editable=True)

@bp.route('/api/canvas/<int:canvas_id>/update', methods=['POST'])
@login_required
def update_canvas(canvas_id):
    canvas = Canvas.query.get_or_404(canvas_id)
    
    if canvas.user_id != current_user.id:
        return jsonify({'error': '无权操作'}), 403
    
    data = request.get_json()
    if 'gridData' in data:
        canvas.grid_data = json.dumps(data['gridData'])
        db.session.commit()
        return jsonify({'success': True})
    
    return jsonify({'error': '无效数据'}), 400

@bp.route('/public')
def public():
    public_canvases = Canvas.query.filter_by(is_public=True).order_by(Canvas.updated_at.desc()).all()
    return render_template('canvas/public_canvas.html', 
                         title='公共画布',
                         canvases=public_canvases)

@bp.route('/canvas/<int:canvas_id>/delete', methods=['GET'])
@login_required
def delete(canvas_id):
    canvas = Canvas.query.get_or_404(canvas_id)
    
    if canvas.user_id != current_user.id:
        flash('无权删除此画布', 'danger')
        return redirect(url_for('canvas.index'))
    
    db.session.delete(canvas)
    db.session.commit()
    flash('画布已删除', 'success')
    return redirect(url_for('canvas.index'))