from app import create_app
from app import db
from app.models import User, Canvas
import os
import sys
import json


app = create_app()

def init_database():
    """初始化数据库（如果不存在）"""
    if not os.path.exists('.\\app\\app.db'):
        print("数据库不存在，正在创建...")
        with app.app_context():
            db.create_all()
        print("数据库创建完成！")
    else:
        print("数据库已存在")

def get_all_users():
    """获取所有用户"""
    with app.app_context():
        users = User.query.all()
        return users

def get_all_canvases():
    """获取所有画布"""
    with app.app_context():
        canvases = Canvas.query.order_by(Canvas.created_at.desc()).all()
        return canvases

def get_user_by_id(user_id):
    """根据ID获取用户"""
    with app.app_context():
        return User.query.get(user_id)

def get_canvas_by_id(canvas_id):
    """根据ID获取画布"""
    with app.app_context():
        return Canvas.query.get(canvas_id)
    
def get_canvases_by_user(user_id):
    """获取用户的画布"""
    with app.app_context():
        return Canvas.query.filter_by(user_id=user_id).all()

def get_public_canvases():
    """获取公开画布"""
    with app.app_context():
        return Canvas.query.filter_by(is_public=True).all()

def show_statistics():
    """显示统计信息"""
    with app.app_context():
        user_count = User.query.count()
        canvas_count = Canvas.query.count()
        public_count = Canvas.query.filter_by(is_public=True).count()
        
        print("=== 数据库统计 ===")
        print(f"用户总数: {user_count}")
        print(f"画布总数: {canvas_count}")
        print(f"公开画布: {public_count}")
        print(f"私有画布: {canvas_count - public_count}")

def show_users():
    """显示所有用户"""
    users = get_all_users()
    print(f"\n=== 所有用户 ({len(users)}个) ===")
    for user in users:
        print(f"ID: {user.id}, 用户名: {user.username}, 邮箱: {user.email}")
        canvases = get_canvases_by_user(user.id)
        print(f"  画布数: {len(canvases)}")

def show_canvases():
    """显示所有画布"""
    canvases = get_all_canvases()
    print(f"\n=== 所有画布 ({len(canvases)}个) ===")
    for canvas in canvases:
        user = get_user_by_id(canvas.user_id)
        username = user.username if user else "未知用户"
        print(f"ID: {canvas.id}, 标题: {canvas.title}")
        print(f"  作者: {username}, 公开: {canvas.is_public}, 创建时间: {canvas.created_at}")

def reset_database(db):
    """
    重置数据库（删除所有表并重建）
    参数: db - SQLAlchemy实例
    返回: (success, message)
    """
    try:
        with app.app_context():
            # 删除所有表
            db.drop_all()
            
            # 重新创建表
            db.create_all()
            print("数据库已重置")
            return True, "数据库已重置"
            
    except Exception as e:
        return False, f"重置失败: {str(e)}"

def add_test_canvas(width:int, height:int):
    
    test_grid_data = json.dumps([[None for _ in range(width)] for _ in range(height)])

    test_canvas = Canvas(
        title = '测试画布',
        width = width,
        height = height,
        grid_data = test_grid_data,
        is_public = True,
        user_id = 1
    )
    try:
        with app.app_context():
            db.session.add(test_canvas)
            db.session.commit()
        print(f'测试画布已添加')
        return True
    except Exception as e:
        print(f'测试画布添加失败')

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("Flask-SQLAlchemy 数据库查询工具")
        print("=" * 40)
        
        # 初始化数据库
        init_database()
        
        # 显示统计信息
        show_statistics()
        
        # 显示用户列表
        show_users()
        
        # 显示画布列表
        show_canvases()
        print("\n查询完成！")
    elif len(sys.argv) == 2: 
        command = sys.argv[1]
        if command == 'reset_database':
            reset_database(db)
        elif command == 'add_test_canvas':
            add_test_canvas(32, 32)
    

if __name__ == "__main__":
    main()