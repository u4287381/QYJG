from datetime import datetime

from wxcloudrun import db


# 计数表
class Counters(db.Model):
    # 设置结构体表格名称
    __tablename__ = 'Counters'

    # 设定结构体对应表格的字段
    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer, default=1)
    created_at = db.Column('createdAt', db.TIMESTAMP, nullable=False, default=datetime.now())
    updated_at = db.Column('updatedAt', db.TIMESTAMP, nullable=False, default=datetime.now())


class User(db.Model):
    # 设置结构体表格名称
    __tablename__ = 'user'

    # 设定结构体对应表格的字段
    username = db.Column(db.VARCHAR, primary_key=True)
    subscribe_time = db.Column(db.TIMESTAMP, default=datetime.now())
    total_pay = db.Column('createdAt', db.Integer, nullable=False, default=0)
    vip_expire_time = db.Column('updatedAt', db.TIMESTAMP, nullable=False, default=datetime.now())