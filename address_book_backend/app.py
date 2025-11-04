from flask import Flask, request, jsonify
from flask_cors import CORS
from config import Config
from models import db, Contact, Group

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)  # 允许跨域请求
db.init_app(app)

# 初始化数据库（首次运行时会创建表，已创建可注释）
with app.app_context():
    db.create_all()

# ---------------------- 分组接口 ----------------------
# 获取所有分组
@app.route('/api/groups', methods=['GET'])
def get_groups():
    groups = Group.query.all()
    return jsonify([g.to_dict() for g in groups])

# 创建分组
@app.route('/api/groups', methods=['POST'])
def add_group():
    data = request.get_json()
    if not data.get('name'):
        return jsonify({'error': '分组名称不能为空'}), 400
    if Group.query.filter_by(name=data['name']).first():
        return jsonify({'error': '分组已存在'}), 400
    new_group = Group(name=data['name'])
    db.session.add(new_group)
    db.session.commit()
    return jsonify(new_group.to_dict()), 201

# 更新分组
@app.route('/api/groups/<int:id>', methods=['PUT'])
def update_group(id):
    group = Group.query.get_or_404(id)
    data = request.get_json()
    if not data.get('name'):
        return jsonify({'error': '分组名称不能为空'}), 400
    if Group.query.filter_by(name=data['name']).first() and data['name'] != group.name:
        return jsonify({'error': '分组已存在'}), 400
    group.name = data['name']
    db.session.commit()
    return jsonify(group.to_dict())

# 删除分组
@app.route('/api/groups/<int:id>', methods=['DELETE'])
def delete_group(id):
    group = Group.query.get_or_404(id)
    db.session.delete(group)
    db.session.commit()
    return jsonify({'message': '分组已删除'}), 200

# ---------------------- 联系人接口 ----------------------
# 获取所有联系人（支持按分组筛选）
@app.route('/api/contacts', methods=['GET'])
def get_contacts():
    group_id = request.args.get('group_id')
    if group_id == 'ungrouped':  # 筛选未分组
        contacts = Contact.query.filter_by(group_id=None).all()
    elif group_id:  # 筛选指定分组
        contacts = Contact.query.filter_by(group_id=group_id).all()
    else:  # 所有联系人
        contacts = Contact.query.all()
    return jsonify([c.to_dict() for c in contacts])

# 获取单个联系人（编辑用）
@app.route('/api/contacts/<int:id>', methods=['GET'])
def get_contact(id):
    contact = Contact.query.get_or_404(id)
    return jsonify(contact.to_dict())

# 添加联系人
@app.route('/api/contacts', methods=['POST'])
def add_contact():
    data = request.get_json()
    if not data.get('name') or not data.get('phone'):
        return jsonify({'error': '姓名和电话不能为空'}), 400
    new_contact = Contact(
        name=data['name'],
        phone=data['phone'],
        email=data.get('email'),
        address=data.get('address'),
        group_id=data.get('group_id') or None  # 空值处理为未分组
    )
    db.session.add(new_contact)
    db.session.commit()
    return jsonify(new_contact.to_dict()), 201

# 更新联系人
@app.route('/api/contacts/<int:id>', methods=['PUT'])
def update_contact(id):
    contact = Contact.query.get_or_404(id)
    data = request.get_json()
    if not data.get('name') or not data.get('phone'):
        return jsonify({'error': '姓名和电话不能为空'}), 400
    contact.name = data['name']
    contact.phone = data['phone']
    contact.email = data.get('email')
    contact.address = data.get('address')
    contact.group_id = data.get('group_id') or None  # 支持改为未分组
    db.session.commit()
    return jsonify(contact.to_dict())

# 删除联系人
@app.route('/api/contacts/<int:id>', methods=['DELETE'])
def delete_contact(id):
    contact = Contact.query.get_or_404(id)
    db.session.delete(contact)
    db.session.commit()
    return jsonify({'message': '联系人已删除'}), 200

if __name__ == '__main__':
    app.run(port=5000)  # 固定端口5000，与前端匹配