import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue';
import RegisterView from '@/views/RegisterView.vue';
import LoginView from '@/views/LoginView.vue';
import DashboardView from '@/views/DashboardView.vue';
import ProfileView from '@/views/ProfileView.vue';
import store from '@/store';


const routes = [
  {
    path: '/',
    name: "Home",
    component: HomeView,
  },
  {
    path: '/register',
    name: 'Register',
    component: RegisterView,
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginView,
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: DashboardView,
    meta: { requiresAuth: true },
  },
  {
    path: '/profile',
    name: 'Profile',
    component: ProfileView,
    meta: { requiresAuth: true },
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

// 在路由跳转前执行的钩子函数
router.beforeEach((to, _, next) => {
  // 检查即将进入的路由是否需要认证
  if (to.matched.some(record => record.meta.requiresAuth)) {
    // 如果用户已经登录
    if (store.getters.isAuthenticated) {
      // 允许导航
      next();
      return;
    }
    // 如果用户未登录，重定向到登录页面
    next('/login');
  } else {
    // 如果不需要认证，允许导航
    next();
  }
});

export default router