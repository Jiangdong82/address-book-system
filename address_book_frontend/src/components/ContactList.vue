<template>
    <div class="container">
        <div class="header">
            <h1>通讯录</h1>
            <div class="actions">
                <button @click="$router.push('/add')" class="btn primary">添加联系人</button>
                <button @click="$router.push('/groups')" class="btn secondary">分组管理</button>
            </div>
        </div>

        <!-- 分组筛选 -->
        <div class="filter">
            <select v-model="selectedGroup" @change="filterContacts">
                <option value="">所有联系人</option>
                <option value="ungrouped">未分组</option>
                <option v-for="group in groups" :value="group.id" :key="group.id">
                    {{ group.name }}
                </option>
            </select>
        </div>

        <!-- 联系人列表 -->
        <div class="contact-grid">
            <div v-for="contact in filteredContacts" :key="contact.id" class="contact-card">
                <div class="info">
                    <h3>{{ contact.name }}</h3>
                    <p><strong>电话：</strong>{{ contact.phone }}</p>
                    <p><strong>邮箱：</strong>{{ contact.email || '-' }}</p>
                    <p><strong>地址：</strong>{{ contact.address || '-' }}</p>
                    <p><strong>分组：</strong>{{ contact.group_name }}</p>
                </div>
                <div class="actions">
                    <button @click="$router.push(`/edit/${contact.id}`)" class="btn edit">编辑</button>
                    <button @click="deleteContact(contact.id)" class="btn delete">删除</button>
                </div>
            </div>
        </div>

        <!-- 空状态 -->
        <div v-if="filteredContacts.length === 0" class="empty">
            暂无联系人，请添加...
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import api from '../utils/api';

const contacts = ref([]);
const groups = ref([]);
const selectedGroup = ref('');

// 加载数据
const loadData = async () => {
    try {
        const [contactsRes, groupsRes] = await Promise.all([
            api.get('/contacts'),
            api.get('/groups')
        ]);
        contacts.value = contactsRes.data;
        groups.value = groupsRes.data;
    } catch (err) {
        alert('数据加载失败：' + err.message);
    }
};

// 筛选联系人
const filteredContacts = computed(() => {
    if (!selectedGroup.value) return contacts.value;
    if (selectedGroup.value === 'ungrouped') {
        return contacts.value.filter(c => !c.group_id);
    }
    return contacts.value.filter(c => c.group_id == selectedGroup.value);
});

// 手动筛选
const filterContacts = () => {};

// 删除联系人
const deleteContact = async (id) => {
    if (confirm('确定删除该联系人吗？')) {
        try {
            await api.delete(`/contacts/${id}`);
            contacts.value = contacts.value.filter(c => c.id !== id); // 本地删除，无需重新请求
        } catch (err) {
            alert('删除失败：' + err.message);
        }
    }
};

onMounted(loadData);
</script>

<style scoped>
.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}
.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}
.actions {
    display: flex;
    gap: 10px;
}
.btn {
    padding: 8px 16px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}
.btn.primary {
    background: #42b983;
    color: white;
}
.btn.secondary {
    background: #1890ff;
    color: white;
}
.filter {
    margin: 20px 0;
}
.filter select {
    padding: 8px;
    min-width: 200px;
    border-radius: 4px;
    border: 1px solid #ddd;
}
.contact-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
    margin-top: 20px;
}
.contact-card {
    background: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
.info p {
    margin: 5px 0;
}
.contact-card .actions {
    margin-top: 15px;
    justify-content: flex-end;
}
.btn.edit {
    background: #faad14;
    color: white;
}
.btn.delete {
    background: #ff4d4f;
    color: white;
}
.empty {
    text-align: center;
    padding: 50px;
    color: #999;
    font-size: 18px;
}
</style>