import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: JSON.parse(localStorage.getItem('juwo-user')),
    token: localStorage.getItem('juwo-token') || null,
    loading: false,
    error: null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.token && !!state.user,
  },

  actions: {
    async login() {
      this.loading = true
      this.error = null
      try {
        // 这应该调用真实的API
        // const response = await userAPI.login(credentials);
        // const { user, token } = response.data;
        
        // 模拟API响应
        const user = { id: 1, name: 'Lucy', email: 'lucy@example.com' };
        const token = 'fake-jwt-token';
        
        this.user = user
        this.token = token
        
        localStorage.setItem('juwo-user', JSON.stringify(user))
        localStorage.setItem('juwo-token', token)
        
        // 可选：设置axios的默认头部
        // import apiClient from '@/services/api';
        // apiClient.defaults.headers.common['Authorization'] = `Bearer ${token}`;

        return true
      } catch (error) {
        this.error = error.response?.data?.message || '登录失败'
        return false
      } finally {
        this.loading = false
      }
    },

    logout() {
      this.user = null
      this.token = null
      localStorage.removeItem('juwo-user')
      localStorage.removeItem('juwo-token')
      
      // 可选：移除axios的默认头部
      // import apiClient from '@/services/api';
      // delete apiClient.defaults.headers.common['Authorization'];
    },
  },
})
