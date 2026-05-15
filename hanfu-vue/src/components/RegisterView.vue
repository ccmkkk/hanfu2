<template>
  <div class="auth-container">
    <div class="auth-panel">
      <div class="back-button" @click="$emit('back')">
        <i class="fas fa-arrow-left"></i> 返回
      </div>

      <div class="auth-header">
        <i class="fas fa-user-plus"></i>
        <h2>用户注册</h2>
        <p>创建账号开始您的汉服之旅</p>
      </div>

      <form @submit.prevent="handleRegister" class="auth-form">
        <div class="form-group">
          <label><i class="fas fa-phone"></i> 手机号</label>
          <input
            type="tel"
            v-model="phone"
            placeholder="请输入手机号作为账号"
            maxlength="11"
            required
          >
        </div>

        <div class="form-group">
          <label><i class="fas fa-lock"></i> 密码</label>
          <input
            type="password"
            v-model="password"
            placeholder="请输入密码（至少6位）"
            minlength="6"
            required
          >
        </div>

        <div class="form-group">
          <label><i class="fas fa-lock"></i> 确认密码</label>
          <input
            type="password"
            v-model="confirmPassword"
            placeholder="请再次输入密码"
            minlength="6"
            required
          >
        </div>

        <div v-if="errorMessage" class="error-msg">
          <i class="fas fa-exclamation-circle"></i> {{ errorMessage }}
        </div>

        <button type="submit" class="btn-primary" :disabled="loading">
          <i v-if="loading" class="fas fa-spinner fa-pulse"></i>
          <i v-else class="fas fa-user-plus"></i>
          {{ loading ? '注册中...' : '注册' }}
        </button>
      </form>

      <div class="auth-footer">
        已有账号？<span @click="$emit('toLogin')">立即登录</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const emit = defineEmits(['back', 'toLogin', 'registerSuccess'])

const phone = ref('')
const password = ref('')
const confirmPassword = ref('')
const errorMessage = ref('')
const loading = ref(false)

function handleRegister() {
  errorMessage.value = ''

  if (!phone.value || phone.value.length !== 11) {
    errorMessage.value = '请输入正确的11位手机号'
    return
  }

  if (!/^1[3-9]\d{9}$/.test(phone.value)) {
    errorMessage.value = '手机号格式不正确'
    return
  }

  if (password.value.length < 6) {
    errorMessage.value = '密码至少需要6位'
    return
  }

  if (password.value !== confirmPassword.value) {
    errorMessage.value = '两次输入的密码不一致'
    return
  }

  const users = JSON.parse(localStorage.getItem('hanfu_users') || '{}')

  if (users[phone.value]) {
    errorMessage.value = '该手机号已注册，请直接登录'
    return
  }

  loading.value = true

  setTimeout(() => {
    users[phone.value] = {
      password: password.value,
      phone: phone.value,
      createdAt: new Date().toISOString(),
      hasCompletedProfile: false,
      profile: {
        gender: '',
        skinTone: '',
        bodyShape: 3
      }
    }

    localStorage.setItem('hanfu_users', JSON.stringify(users))
    localStorage.setItem('hanfu_current_user', phone.value)

    loading.value = false
    emit('registerSuccess', phone.value)
  }, 500)
}
</script>

<style scoped>
.auth-container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
}

.auth-panel {
  background: #fff;
  border-radius: 20px;
  padding: 40px;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
}

.back-button {
  color: #b5654b;
  cursor: pointer;
  margin-bottom: 20px;
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.back-button:hover {
  color: #8b4534;
}

.auth-header {
  text-align: center;
  margin-bottom: 30px;
}

.auth-header i {
  font-size: 48px;
  color: #b5654b;
  margin-bottom: 15px;
}

.auth-header h2 {
  color: #3e2a1f;
  margin: 0 0 10px;
  font-size: 1.8rem;
}

.auth-header p {
  color: #7c5f42;
  font-size: 14px;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  color: #3e2a1f;
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.form-group label i {
  color: #b5654b;
  width: 20px;
}

.form-group input {
  padding: 12px 15px;
  border: 2px solid #e8e0d5;
  border-radius: 10px;
  font-size: 16px;
  transition: border-color 0.3s;
}

.form-group input:focus {
  outline: none;
  border-color: #b5654b;
}

.error-msg {
  background: #fff5f5;
  color: #d63031;
  padding: 12px;
  border-radius: 8px;
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn-primary {
  background: linear-gradient(135deg, #b5654b, #c9785a);
  color: white;
  border: none;
  padding: 14px;
  border-radius: 10px;
  font-size: 16px;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
  transition: transform 0.2s, box-shadow 0.2s;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 5px 20px rgba(181, 101, 75, 0.3);
}

.btn-primary:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.auth-footer {
  text-align: center;
  margin-top: 25px;
  color: #7c5f42;
  font-size: 14px;
}

.auth-footer span {
  color: #b5654b;
  cursor: pointer;
  font-weight: 600;
}

.auth-footer span:hover {
  text-decoration: underline;
}
</style>
