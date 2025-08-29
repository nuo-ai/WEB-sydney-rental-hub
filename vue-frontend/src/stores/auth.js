import { defineStore } from 'pinia'
import apiClient from '@/services/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: JSON.parse(localStorage.getItem('juwo-user')),
    token: localStorage.getItem('juwo-token') || null,
    refreshToken: localStorage.getItem('juwo-refresh-token') || null,
    tempToken: null, // 临时token，用于邮箱验证前
    loading: false,
    error: null,
    savedAddresses: [], // 用户保存的地址
  }),

  getters: {
    isAuthenticated: (state) => {
      // Check for testMode in localStorage or environment
      const testMode = localStorage.getItem('auth-testMode') === 'true' || 
                      import.meta.env.VITE_AUTH_TEST_MODE === 'true'
      
      return testMode || (!!state.token && !!state.user)
    },
    
    testMode: () => {
      return localStorage.getItem('auth-testMode') === 'true' || 
             import.meta.env.VITE_AUTH_TEST_MODE === 'true'
    },
  },

  actions: {
    // Initialize auth state and set up interceptors
    initAuth() {
      const token = localStorage.getItem('juwo-token')
      if (token) {
        apiClient.defaults.headers.common['Authorization'] = `Bearer ${token}`
      }
      
      // Set up response interceptor for automatic token refresh
      apiClient.interceptors.response.use(
        (response) => response,
        async (error) => {
          const originalRequest = error.config
          
          if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true
            
            const success = await this.tryRefreshToken()
            if (success) {
              originalRequest.headers['Authorization'] = `Bearer ${this.token}`
              return apiClient(originalRequest)
            }
          }
          
          return Promise.reject(error)
        }
      )
    },
    async register(email, password, fullName = null) {
      this.loading = true
      this.error = null
      try {
        const response = await apiClient.post('/auth/register', { 
          email, 
          password,
          full_name: fullName 
        })
        
        if (response.data.status === 'success') {
          this.tempToken = response.data.temp_token
          console.log(`✅ Registration successful. Verification email sent to ${email}`)
          return true
        } else {
          throw new Error(response.data.message || 'Registration failed')
        }
      } catch (error) {
        this.error = error.response?.data?.detail || error.message || 'Registration failed'
        console.error('Registration error:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async login(email, password) {
      this.loading = true
      this.error = null
      try {
        const response = await apiClient.post('/auth/login', { email, password })
        
        if (response.data.access_token) {
          const { access_token, refresh_token } = response.data
          
          // 获取用户信息
          apiClient.defaults.headers.common['Authorization'] = `Bearer ${access_token}`
          const userResponse = await apiClient.get('/auth/me')
          const user = userResponse.data
          
          this.user = user
          this.token = access_token
          this.refreshToken = refresh_token
          
          localStorage.setItem('juwo-user', JSON.stringify(user))
          localStorage.setItem('juwo-token', access_token)
          localStorage.setItem('juwo-refresh-token', refresh_token)
          
          // 加载用户地址
          await this.loadUserAddresses()
          
          console.log(`✅ Login successful: ${user.email}`)
          return true
        } else {
          throw new Error('No access token received')
        }
      } catch (error) {
        this.error = error.response?.data?.detail || error.message || 'Login failed'
        console.error('Login error:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async verifyEmail(token) {
      try {
        const response = await apiClient.post('/auth/verify-email', null, {
          params: { token }
        })
        
        if (response.data.status === 'success') {
          this.tempToken = null
          console.log('✅ Email verified successfully')
          return true
        }
        return false
      } catch (error) {
        console.error('Email verification failed:', error)
        this.error = error.response?.data?.detail || 'Verification failed'
        return false
      }
    },

    async resendVerificationEmail(email) {
      try {
        const response = await apiClient.post('/auth/resend-verification', { email })
        
        if (response.data.status === 'success') {
          this.tempToken = response.data.temp_token
          console.log(`✅ Verification email resent to ${email}`)
          return true
        }
        return false
      } catch (error) {
        console.error('Failed to resend verification email:', error)
        this.error = error.response?.data?.detail || 'Failed to resend email'
        throw error
      }
    },

    async loadUserAddresses() {
      // In test mode, load from localStorage
      if (this.testMode) {
        const addresses = JSON.parse(localStorage.getItem('juwo-addresses') || '[]')
        this.savedAddresses = addresses
        console.log(`✅ Loaded ${this.savedAddresses.length} saved addresses from localStorage (test mode)`)
        return
      }
      
      if (!this.token) {
        this.savedAddresses = []
        return
      }
      
      try {
        const response = await apiClient.get('/auth/addresses')
        this.savedAddresses = response.data || []
        console.log(`✅ Loaded ${this.savedAddresses.length} saved addresses`)
      } catch (error) {
        console.error('Failed to load user addresses:', error)
        this.savedAddresses = []
        
        // 如果是401错误，可能需要刷新token
        if (error.response?.status === 401) {
          await this.tryRefreshToken()
        }
      }
    },

    async saveUserAddress(address) {
      try {
        // 验证必需字段
        if (!address.latitude || !address.longitude) {
          console.error('Missing latitude or longitude in address:', address)
          throw new Error('Invalid address data: missing coordinates')
        }
        
        // In test mode, save to localStorage instead of API
        if (this.testMode) {
          const savedAddress = {
            id: Date.now().toString(),
            ...address,
            createdAt: new Date().toISOString()
          }
          
          this.savedAddresses.push(savedAddress)
          
          // Save to localStorage
          const addresses = JSON.parse(localStorage.getItem('juwo-addresses') || '[]')
          addresses.push(savedAddress)
          localStorage.setItem('juwo-addresses', JSON.stringify(addresses))
          
          console.log(`✅ Address saved locally (test mode): ${savedAddress.label}`)
          return savedAddress
        }
        
        // Production mode - call API
        const response = await apiClient.post('/auth/addresses', {
          address: address.address,
          label: address.label,
          place_id: address.placeId,
          latitude: address.latitude,
          longitude: address.longitude
        })
        
        const savedAddress = response.data
        this.savedAddresses.push(savedAddress)
        console.log(`✅ Address saved: ${savedAddress.label}`)
        return savedAddress
      } catch (error) {
        console.error('Failed to save address:', error)
        this.error = error.response?.data?.detail || 'Failed to save address'
        throw error
      }
    },

    async removeUserAddress(addressId) {
      try {
        // In test mode, remove from localStorage
        if (this.testMode) {
          const index = this.savedAddresses.findIndex(a => a.id === addressId)
          if (index > -1) {
            const removed = this.savedAddresses.splice(index, 1)[0]
            
            // Update localStorage
            const addresses = JSON.parse(localStorage.getItem('juwo-addresses') || '[]')
            const localIndex = addresses.findIndex(a => a.id === addressId)
            if (localIndex > -1) {
              addresses.splice(localIndex, 1)
              localStorage.setItem('juwo-addresses', JSON.stringify(addresses))
            }
            
            console.log(`✅ Address removed locally (test mode): ${removed.label}`)
          }
          return
        }
        
        // Production mode - call API
        await apiClient.delete(`/auth/addresses/${addressId}`)
        
        // 从本地状态移除
        const index = this.savedAddresses.findIndex(a => a.id === addressId)
        if (index > -1) {
          const removed = this.savedAddresses.splice(index, 1)[0]
          console.log(`✅ Address removed: ${removed.label}`)
        }
      } catch (error) {
        console.error('Failed to remove address:', error)
        this.error = error.response?.data?.detail || 'Failed to remove address'
        throw error
      }
    },

    async tryRefreshToken() {
      if (!this.refreshToken) {
        this.logout()
        return false
      }
      
      try {
        const response = await apiClient.post('/auth/refresh', {
          refresh_token: this.refreshToken
        })
        
        if (response.data.access_token) {
          const { access_token, refresh_token } = response.data
          this.token = access_token
          this.refreshToken = refresh_token
          
          localStorage.setItem('juwo-token', access_token)
          localStorage.setItem('juwo-refresh-token', refresh_token)
          apiClient.defaults.headers.common['Authorization'] = `Bearer ${access_token}`
          
          console.log('✅ Token refreshed successfully')
          return true
        }
      } catch (error) {
        console.error('Token refresh failed:', error)
        this.logout()
      }
      return false
    },

    logout() {
      this.user = null
      this.token = null
      this.refreshToken = null
      this.tempToken = null
      this.savedAddresses = []
      localStorage.removeItem('juwo-user')
      localStorage.removeItem('juwo-token')
      localStorage.removeItem('juwo-refresh-token')
      
      // 移除axios的默认头部
      delete apiClient.defaults.headers.common['Authorization']
    },
    
    // Test mode helpers
    enableTestMode() {
      localStorage.setItem('auth-testMode', 'true')
      console.log('🧪 Test mode enabled - authentication bypassed')
    },
    
    disableTestMode() {
      localStorage.removeItem('auth-testMode')
      console.log('🔒 Test mode disabled - authentication required')
    },
  },
})
