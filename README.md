# pixal_art_website
同一个项目，未上传虚拟环境和数据库
flowchart TD
    A[客户端(浏览器)<br>发起HTTP请求<br>GET /login] --> B{Flask应用<br>接收请求}
    
    B --> C[URL路由器<br>匹配路由规则<br>找到对应函数]
    
    C --> D[执行路由函数<br>@bp.route('/login')]
    
    D --> E{业务逻辑处理<br>与数据交互}
    E --> E1[验证表单数据]
    E1 --> E2[查询数据库User表]
    E2 --> E3[校验密码哈希]
    E3 --> E4[会话管理<br>login_user()]
    
    E --> F{生成响应}
    
    F --> G{响应类型判断}
    
    G -->|重定向| H[redirect<br>返回302状态码<br>Location: /canvas]
    G -->|渲染页面| I[render_template<br>渲染login.html<br>返回HTML页面]
    G -->|JSON API| J[jsonify<br>返回JSON数据<br>{success: true}]
    G -->|错误| K[abort/错误页面<br>返回4xx/5xx状态码]
    
    H & I & J & K --> L[HTTP响应<br>返回给客户端]
    
    L --> M[客户端<br>接收并处理响应<br>跳转/显示/解析]
    
    style A fill:#e1f5fe
    style B fill:#f3e5f5
    style C fill:#e8f5e8
    style D fill:#fff3e0
    style E fill:#ffebee
    style F fill:#e8f5e8
    style G fill:#f3e5f5
    style L fill:#fff3e0
    style M fill:#e1f5fe
