<template>
  <div class="auth-container">
    <div class="auth-panel">
      <div class="back-button" @click="$emit('back')">
        <i class="fas fa-arrow-left"></i> 返回
      </div>

      <div class="auth-header">
        <i class="fas fa-user"></i>
        <h2>用户登录</h2>
        <p>欢迎回来，开始您的汉服之旅</p>
      </div>

      <form @submit.prevent="handleLogin" class="auth-form">
        <div class="form-group">
          <label><i class="fas fa-phone"></i> 手机号</label>
          <input
            type="tel"
            v-model="phone"
            placeholder="请输入注册时的手机号"
            maxlength="11"
            required
          >
        </div>

        <div class="form-group">
          <label><i class="fas fa-lock"></i> 密码</label>
          <input
            type="password"
            v-model="password"
            placeholder="请输入密码"
            required
          >
        </div>

        <div v-if="errorMessage" class="error-msg">
          <i class="fas fa-exclamation-circle"></i> {{ errorMessage }}
        </div>

        <button type="submit" class="btn-primary" :disabled="loading">
          <i v-if="loading" class="fas fa-spinner fa-pulse"></i>
          <i v-else class="fas fa-sign-in-alt"></i>
          {{ loading ? '登录中...' : '登录' }}
        </button>
      </form>

      <div class="auth-footer">
        还没有账号？<span @click="$emit('toRegister')">立即注册</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const emit = defineEmits(['back', 'toRegister', 'loginSuccess'])

const phone = ref('')
const password = ref('')
const errorMessage = ref('')
const loading = ref(false)

function handleLogin() {
  errorMessage.value = ''

  if (!phone.value || phone.value.length !== 11) {
    errorMessage.value = '请输入正确的11位手机号'
    return
  }

  if (!password.value) {
    errorMessage.value = '请输入密码'
    return
  }

  const users = JSON.parse(localStorage.getItem('hanfu_users') || '{}')
  const user = users[phone.value]

  if (!user) {
    errorMessage.value = '该账号未注册，请先注册'
    return
  }

  if (user.password !== password.value) {
    errorMessage.value = '密码错误，请重新输入'
    return
  }

  loading.value = true

  setTimeout(() => {
    localStorage.setItem('hanfu_current_user', phone.value)
    loading.value = false
    emit('loginSuccess', phone.value)
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
