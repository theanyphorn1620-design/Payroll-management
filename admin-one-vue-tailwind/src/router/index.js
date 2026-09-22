import { createRouter, createWebHashHistory } from 'vue-router'
import Style from '@/views/StyleView.vue'
import Home from '@/views/HomeView.vue'
import { useAuthStore } from '@/stores/auth.js'

const routes = [
  {
    meta: {
      title: 'Select style',
    },
    path: '/',
    name: 'style',
    component: Style,
  },
  {
    // Document title tag
    // We combine it with defaultDocumentTitle set in `src/main.js` on router.afterEach hook
    meta: {
      title: 'Dashboard',
      requiresAuth: true,
      adminOnly: true,
    },
    path: '/dashboard',
    name: 'dashboard',
    component: Home,
  },
  {
    meta: {
      title: 'My Portal',
      requiresAuth: true,
    },
    path: '/my-portal',
    name: 'my-portal',
    component: () => import('@/views/MyPortalView.vue'),
  },
  {
    meta: {
      title: 'Employees',
      requiresAuth: true,
      adminOnly: true,
    },
    path: '/employees',
    name: 'employees',
    component: () => import('@/views/EmployeesView.vue'),
  },
  {
    meta: {
      title: 'Attendance',
      requiresAuth: true,
      adminOnly: true,
    },
    path: '/attendance',
    name: 'attendance',
    component: () => import('@/views/AttendanceView.vue'),
  },
  {
    meta: {
      title: 'Salary Structures',
      requiresAuth: true,
      adminOnly: true,
    },
    path: '/salary-structures',
    name: 'salary-structures',
    component: () => import('@/views/SalaryStructuresView.vue'),
  },
  {
    meta: {
      title: 'Payslips',
      requiresAuth: true,
      adminOnly: true,
    },
    path: '/payslips',
    name: 'payslips',
    component: () => import('@/views/PayslipsView.vue'),
  },
  {
    meta: {
      title: 'Reports',
      requiresAuth: true,
      adminOnly: true,
    },
    path: '/reports',
    name: 'reports',
    component: () => import('@/views/ReportsView.vue'),
  },
  {
    meta: {
      title: 'Holidays',
      requiresAuth: true,
      adminOnly: true,
    },
    path: '/holidays',
    name: 'holidays',
    component: () => import('@/views/HolidaysView.vue'),
  },
  {
    meta: {
      title: 'Check In',
      requiresAuth: true,
    },
    path: '/check-in/:token',
    name: 'check-in',
    component: () => import('@/views/CheckInView.vue'),
  },
  {
    meta: {
      title: 'Tables',
    },
    path: '/tables',
    name: 'tables',
    component: () => import('@/views/TablesView.vue'),
  },
  {
    meta: {
      title: 'Forms',
    },
    path: '/forms',
    name: 'forms',
    component: () => import('@/views/FormsView.vue'),
  },
  {
    meta: {
      title: 'Profile',
    },
    path: '/profile',
    name: 'profile',
    component: () => import('@/views/ProfileView.vue'),
  },
  {
    meta: {
      title: 'Ui',
    },
    path: '/ui',
    name: 'ui',
    component: () => import('@/views/UiView.vue'),
  },
  {
    meta: {
      title: 'Responsive layout',
    },
    path: '/responsive',
    name: 'responsive',
    component: () => import('@/views/ResponsiveView.vue'),
  },
  {
    meta: {
      title: 'Login',
    },
    path: '/login',
    name: 'login',
    component: () => import('@/views/LoginView.vue'),
  },
  {
    meta: {
      title: 'Error',
    },
    path: '/error',
    name: 'error',
    component: () => import('@/views/ErrorView.vue'),
  },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    return savedPosition || { top: 0 }
  },
})

router.beforeEach(async (to) => {
  const authStore = useAuthStore()

  if (!authStore.isReady) {
    await authStore.restore()
  }

  if (!to.meta.requiresAuth) {
    return true
  }

  if (!authStore.isAuthenticated) {
    return { name: 'login', query: { redirect: to.fullPath } }
  }

  if (to.meta.adminOnly && authStore.role !== 'admin') {
    return { name: 'my-portal' }
  }

  return true
})

export default router
