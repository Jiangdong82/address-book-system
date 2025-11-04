<template>
    <div class="container">
        <h1>分组管理</h1>
        <div class="add-group">
            <input v-model="newGroupName" placeholder="输入分组名称" class="input">
            <button @click="addNewGroup" class="btn primary">添加分组</button>
        </div>
        <div class="group-list">
            <div v-for="group in groups" :key="group.id" class="group-item">
                <span>{{ group.name }}</span>
                <div class="actions">
                    <button @click="editGroup(group)" class="btn edit">编辑</button>
                    <button @click="deleteGroup(group.id)" class="btn delete">删除</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '../utils/api';

const groups = ref([]);
const newGroupName = ref('');

// 加载分组
const loadGroups = async () => {
    try {
        const res = await api.get('/groups');
        groups.value = res.data;
    } catch (err) {
        alert('加载分组失败：' + err.message);
    }
};

// 添加分组
const addNewGroup = async () => {
    if (!newGroupName.value.trim()) {
        alert('分组名称不能为空');
        return;
    }
    try {
        await api.post('/groups', { name: newGroupName.value });
        newGroupName.value = '';
        loadGroups();  // 刷新列表
    } catch (err) {
        alert('添加失败：' + (err.response?.data?.error || err.message));
    }
};

// 编辑分组
const editGroup = (group) => {
    const newName = prompt('修改分组名称', group.name);
    if (newName && newName.trim() && newName !== group.name) {
        try {
            api.put(`/groups/${group.id}`, { name: newName });
            group.name = newName;  // 本地更新，无需重新请求
        } catch (err) {
            alert('修改失败：' + err.message);
            loadGroups();  // 失败后刷新
        }
    }
};

// 删除分组
const deleteGroup = async (id) => {
    if (confirm('确定删除该分组吗？分组内的联系人将变为未分组')) {
        try {
            await api.delete(`/groups/${id}`);
            groups.value = groups.value.filter(g => g.id !== id);  // 本地删除
        } catch (err) {
            alert('删除失败：' + err.message);
        }
    }
};

onMounted(loadGroups);
</script>

<style scoped>
    .container {
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
    }

    .add-group {
        margin: 20px 0;
        display: flex;
        gap: 10px;
    }

    .input {
        flex: 1;
        padding: 10px;
        border: 1px solid #ddd;
        border-radius: 4px;
    }

    .btn {
        padding: 8px 16px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
    }

        .btn.primary {
            background: #1890ff;
            color: white;
        }

    .group-list {
        margin-top: 30px;
    }

    .group-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 12px;
        border-bottom: 1px solid #eee;
    }

    .actions {
        display: flex;
        gap: 10px;
    }

    .btn.edit {
        background: #faad14;
        color: white;
    }

    .btn.delete {
        background: #ff4d4f;
        color: white;
    }
</style>