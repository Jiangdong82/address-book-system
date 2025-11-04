class Config:
    # 数据库连接配置（替换为你的MySQL密码）
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:jxs20051005@localhost:3306/address_book?charset=utf8mb4"
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 关闭追踪修改，提升性能
    DEBUG = True  # 开发模式