from flask import Blueprint

# 创建认证蓝图
# 第一个参数是蓝图名称，第二个参数是模块名（__name__）
bp = Blueprint('auth', __name__)

# 导入路由（必须在蓝图创建后导入，避免循环导入）
from app.auth import routes