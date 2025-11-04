<template>
    <div class="app">
        <nav class="navbar">
            <div class="logo">通讯录管理系统</div>
            <div class="nav-links">
                <router-link to="/">联系人列表</router-link>
                <router-link to="/groups">分组管理</router-link>
            </div>
        </nav>
        <main>
            <router-view />
        </main>
    </div>
</template>

<style>
    .app {
        min-height: 100vh;
        background: #f5f7fa;
    }

    .navbar {
        background: #1890ff;
        color: white;
        padding: 0 20px;
        height: 60px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }

    .logo {
        font-size: 18px;
        font-weight: bold;
    }

    .nav-links {
        display: flex;
        gap: 20px;
    }

        .nav-links a {
            color: white;
            text-decoration: none;
            padding: 8px 12px;
            border-radius: 4px;
            transition: background 0.2s;
        }

            .nav-links a:hover, .nav-links a.router-link-exact-active {
                background: rgba(255,255,255,0.2);
            }

    main {
        padding: 20px;
    }
    /* 全局样式重置 */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
</style>