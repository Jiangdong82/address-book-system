import { createRouter, createWebHistory } from 'vue-router';
import ContactList from '../components/ContactList.vue';
import ContactForm from '../components/ContactForm.vue';
import GroupManager from '../components/GroupManager.vue';

const routes = [
    { path: '/', component: ContactList, name: 'ContactList' },
    { path: '/add', component: ContactForm, name: 'AddContact' },
    { path: '/edit/:id', component: ContactForm, name: 'EditContact' },
    { path: '/groups', component: GroupManager, name: 'GroupManager' }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;