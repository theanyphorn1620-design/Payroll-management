import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/lib/api.js'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('authToken') || null)
  const isStaff = ref(null)
  const employee = ref(null)
  const isReady = ref(false)

  const isAuthenticated = computed(() => !!token.value)
  const role = computed(() => (isStaff.value ? 'admin' : 'employee'))

  function login(username, password) {
    return api.post('auth/login/', { username, password }).then((result) => {
      token.value = result.data.token
      isStaff.value = result.data.is_staff
      employee.value = result.data.employee
      localStorage.setItem('authToken', token.value)
    })
  }

  function logout() {
    token.value = null
    isStaff.value = null
    employee.value = null
    localStorage.removeItem('authToken')
  }

  function restore() {
    if (!token.value) {
      isReady.value = true
      return Promise.resolve()
    }

    return api
      .get('auth/me/')
      .then((result) => {
        isStaff.value = result.data.is_staff
        employee.value = result.data.employee
      })
      .catch(() => {
        logout()
      })
      .finally(() => {
        isReady.value = true
      })
  }

  return {
    token,
    isStaff,
    employee,
    isReady,
    isAuthenticated,
    role,
    login,
    logout,
    restore,
  }
})
