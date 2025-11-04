<template>
    <div class="container">
        <h1>{{ isEdit ? '编辑联系人' : '添加联系人' }}</h1>
        <form @submit.prevent="submitForm" class="form">
            <div class="form-group">
                <label>姓名 *</label>
                <input type="text" v-model="form.name" required>
            </div>
            <div class="form-group">
                <label>电话 *</label>
                <input type="text" v-model="form.phone" required>
            </div>
            <div class="form-group">
                <label>邮箱</label>
                <input type="email" v-model="form.email">
            </div>
            <div class="form-group">
                <label>地址</label>
                <textarea v-model="form.address" rows="3"></textarea>
            </div>
            <div class="form-group">
                <label>分组</label>
                <select v-model="form.group_id">
                    <option value="">未分组</option>
                    <option v-for="group in groups" :value="group.id" :key="group.id">
                        {{ group.name }}
                    </option>
                </select>
            </div>
            <div class="form-actions">
                <button type="submit" class="btn primary">{{ isEdit ? '更新' : '添加' }}</button>
                <button type="button" @click="$router.back()" class="btn secondary">取消</button>
            </div>
        </form>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '../utils/api';

const route = useRoute();
const router = useRouter();
const isEdit = !!route.params.id;
const form = ref({
    name: '',
    phone: '',
    email: '',
    address: '',
    group_id: ''  // 空字符串表示未分组
});
const groups = ref([]);

// 加载分组和联系人数据
const loadData = async () => {
    try {
        // 先加载分组
        const groupsRes = await api.get('/groups');
        groups.value = groupsRes.data;

        // 编辑模式：加载联系人数据
        if (isEdit) {
            const contactRes = await api.get(`/contacts/${route.params.id}`);
            const data = contactRes.data;
            form.value = {
                ...data,
                group_id: data.group_id ?? ''  // 后端null转为空字符串（匹配未分组）
            };
        }
    } catch (err) {
        alert('数据加载失败：' + err.message);
        router.push('/');
    }
};

// 提交表单
const submitForm = async () => {
    try {
        // 处理分组：空字符串转为null（后端识别为未分组）
        const submitData = {
            ...form.value,
            group_id: form.value.group_id || null
        };

        if (isEdit) {
            await api.put(`/contacts/${route.params.id}`, submitData);
        } else {
            await api.post('/contacts', submitData);
        }
        router.push('/');  // 成功后返回列表页
    } catch (err) {
        alert('操作失败：' + (err.response?.data?.error || err.message));
    }
};

onMounted(loadData);
</script>

<style scoped>
.container {
    max-width: 600px;
    margin: 0 auto;
    padding: 20px;
}
.form {
    background: white;
    padding: 30px;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
.form-group {
    margin-bottom: 20px;
}
label {
    display: block;
    margin-bottom: 8px;
    font-weight: 500;
}
input, textarea, select {
    width: 100%;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
    box-sizing: border-box;
}
.form-actions {
    margin-top: 30px;
    display: flex;
    gap: 10px;
}
.btn {
    padding: 10px 20px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}
.btn.primary {
    background: #42b983;
    color: white;
}
.btn.secondary {
    background: #999;
    color: white;
}
</style>