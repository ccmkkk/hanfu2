<template>
  <div class="profile-container">
    <div class="profile-panel">
      <div class="back-button" @click="$emit('back')">
        <i class="fas fa-arrow-left"></i> 返回
      </div>

      <div class="profile-header">
        <i class="fas fa-user-circle"></i>
        <h2>个人信息</h2>
        <p>管理您的账号和偏好设置</p>
      </div>

      <div class="profile-content">
        <div class="account-info">
          <div class="info-row">
            <span class="info-label"><i class="fas fa-phone"></i> 手机号</span>
            <span class="info-value">{{ phone }}</span>
          </div>
          <div class="info-row">
            <span class="info-label"><i class="fas fa-calendar"></i> 注册时间</span>
            <span class="info-value">{{ formatDate(userInfo.createdAt) }}</span>
          </div>
        </div>

        <div class="divider"></div>

        <div class="profile-section">
          <h3><i class="fas fa-sliders-h"></i> 基础信息</h3>

          <div class="form-group">
            <label><i class="fas fa-venus-mars"></i> 性别</label>
            <div class="option-buttons">
              <button
                type="button"
                v-for="gen in genderOptions"
                :key="gen.value"
                :class="['option-btn', { active: profile.gender === gen.value }]"
                @click="updateProfile('gender', gen.value)"
              >
                <i :class="gen.icon"></i>
                {{ gen.label }}
              </button>
            </div>
          </div>

          <div class="form-group">
            <label><i class="fas fa-palette"></i> 肤色</label>
            <div class="option-buttons">
              <button
                type="button"
                v-for="skin in skinOptions"
                :key="skin.value"
                :class="['option-btn', { active: profile.skinTone === skin.value }]"
                @click="updateProfile('skinTone', skin.value)"
              >
                <span :class="['skin-dot', skin.class]"></span>
                {{ skin.label }}
              </button>
            </div>
          </div>

          <div class="form-group">
            <label><i class="fas fa-chart-line"></i> 体型</label>
            <div class="body-shape-display">
              <span class="shape-label">纤瘦</span>
              <input
                type="range"
                v-model.number="profile.bodyShape"
                min="1"
                max="5"
                step="1"
                class="body-shape-slider"
                @change="updateProfile('bodyShape', profile.bodyShape)"
              >
              <span class="shape-label">丰腴</span>
            </div>
            <div class="body-shape-text">{{ bodyShapeText }}</div>
          </div>

          <button class="btn-secondary" @click="goToRecommend">
            <i class="fas fa-tshirt"></i> 根据此信息查看推荐
          </button>
        </div>

        <div class="divider"></div>

        <div class="profile-section">
          <h3><i class="fas fa-key"></i> 修改密码</h3>

          <div class="password-form">
            <div class="form-group">
              <label>当前密码</label>
              <input
                type="password"
                v-model="currentPassword"
                placeholder="请输入当前密码"
              >
            </div>

            <div class="form-group">
              <label>新密码</label>
              <input
                type="password"
                v-model="newPassword"
                placeholder="请输入新密码（至少6位）"
                minlength="6"
              >
            </div>

            <div class="form-group">
              <label>确认新密码</label>
              <input
                type="password"
                v-model="confirmPassword"
                placeholder="请再次输入新密码"
              >
            </div>

            <div v-if="passwordError" class="error-msg">
              <i class="fas fa-exclamation-circle"></i> {{ passwordError }}
            </div>

            <div v-if="passwordSuccess" class="success-msg">
              <i class="fas fa-check-circle"></i> {{ passwordSuccess }}
            </div>

            <button class="btn-primary" @click="changePassword">
              <i class="fas fa-save"></i> 保存新密码
            </button>
          </div>
        </div>

        <div class="divider"></div>

        <button class="btn-logout" @click="handleLogout">
          <i class="fas fa-sign-out-alt"></i> 退出登录
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const emit = defineEmits(['back', 'logout'])

const phone = ref('')
const userInfo = ref({ createdAt: '' })
const profile = ref({
  gender: '',
  skinTone: '',
  bodyShape: 3
})

const currentPassword = ref('')
const newPassword = ref('')
const confirmPassword = ref('')
const passwordError = ref('')
const passwordSuccess = ref('')

const genderOptions = [
  { label: '女性', value: '女', icon: 'fas fa-venus' },
  { label: '男性', value: '男', icon: 'fas fa-mars' },
  { label: '通用', value: '', icon: 'fas fa-genderless' }
]

const skinOptions = [
  { label: '冷皮', value: '冷皮', class: 'skin-cold-white' },
  { label: '暖皮', value: '暖皮', class: 'skin-warm-yellow' },
  { label: '通用', value: '通用', class: 'skin-natural' }
]

const bodyShapeText = computed(() => {
  const texts = {
    1: '偏瘦体型',
    2: '苗条体型',
    3: '标准体型',
    4: '微胖体型',
    5: '丰腴体型'
  }
  return texts[profile.value.bodyShape] || '标准体型'
})

onMounted(() => {
  const currentPhone = localStorage.getItem('hanfu_current_user')
  if (currentPhone) {
    phone.value = currentPhone
    const users = JSON.parse(localStorage.getItem('hanfu_users') || '{}')
    const user = users[currentPhone]
    if (user) {
      userInfo.value = user
      profile.value = {
        gender: user.profile?.gender || '',
        skinTone: user.profile?.skinTone || '',
        bodyShape: user.profile?.bodyShape || 3
      }
    }
  }
})

function formatDate(dateStr) {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`
}

function updateProfile(key, value) {
  profile.value[key] = value
  saveProfile()
}

function saveProfile() {
  const users = JSON.parse(localStorage.getItem('hanfu_users') || '{}')
  if (users[phone.value]) {
    users[phone.value].profile = { ...profile.value }
    localStorage.setItem('hanfu_users', JSON.stringify(users))
  }
}

function goToRecommend() {
  emit('back')
}

function changePassword() {
  passwordError.value = ''
  passwordSuccess.value = ''

  const users = JSON.parse(localStorage.getItem('hanfu_users') || '{}')
  const user = users[phone.value]

  if (!user) {
    passwordError.value = '用户不存在'
    return
  }

  if (user.password !== currentPassword.value) {
    passwordError.value = '当前密码错误'
    return
  }

  if (newPassword.value.length < 6) {
    passwordError.value = '新密码至少需要6位'
    return
  }

  if (newPassword.value !== confirmPassword.value) {
    passwordError.value = '两次输入的新密码不一致'
    return
  }

  users[phone.value].password = newPassword.value
  localStorage.setItem('hanfu_users', JSON.stringify(users))

  currentPassword.value = ''
  newPassword.value = ''
  confirmPassword.value = ''
  passwordSuccess.value = '密码修改成功！'

  setTimeout(() => {
    passwordSuccess.value = ''
  }, 3000)
}

function handleLogout() {
  localStorage.removeItem('hanfu_current_user')
  emit('logout')
}
</script>

<style scoped>
.profile-container {
  min-height: 100vh;
  padding: 20px;
}

.profile-panel {
  background: #fff;
  border-radius: 20px;
  padding: 30px;
  max-width: 600px;
  margin: 0 auto;
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

.profile-header {
  text-align: center;
  margin-bottom: 30px;
}

.profile-header i {
  font-size: 56px;
  color: #b5654b;
  margin-bottom: 10px;
}

.profile-header h2 {
  color: #3e2a1f;
  margin: 0 0 8px;
  font-size: 1.6rem;
}

.profile-header p {
  color: #7c5f42;
  font-size: 14px;
}

.account-info {
  background: #faf5f0;
  border-radius: 12px;
  padding: 20px;
}

.info-row {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
}

.info-label {
  color: #7c5f42;
  display: flex;
  align-items: center;
  gap: 8px;
}

.info-label i {
  color: #b5654b;
  width: 20px;
}

.info-value {
  color: #3e2a1f;
  font-weight: 600;
}

.divider {
  height: 1px;
  background: #e8e0d5;
  margin: 25px 0;
}

.profile-section h3 {
  color: #3e2a1f;
  margin: 0 0 20px;
  font-size: 1.1rem;
  display: flex;
  align-items: center;
  gap: 10px;
}

.profile-section h3 i {
  color: #b5654b;
}

.form-group {
  margin-bottom: 20px;
}

.form-group > label {
  color: #3e2a1f;
  font-size: 14px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 10px;
}

.form-group > label i {
  color: #b5654b;
  width: 20px;
}

.option-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.option-btn {
  padding: 10px 16px;
  border: 2px solid #e8e0d5;
  border-radius: 8px;
  background: #fff;
  color: #3e2a1f;
  font-size: 14px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: all 0.3s;
}

.option-btn:hover {
  border-color: #c9785a;
}

.option-btn.active {
  border-color: #b5654b;
  background: linear-gradient(135deg, #b5654b, #c9785a);
  color: white;
}

.option-btn.active i {
  color: white;
}

.skin-dot {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  border: 2px solid rgba(0, 0, 0, 0.1);
}

.skin-cold-white { background: #fdf5f5; }
.skin-warm-yellow { background: #f5e6d3; }
.skin-natural { background: #d4a574; }
.skin-wheat { background: #c68642; }
.skin-dark { background: #8d5524; }

.body-shape-display {
  display: flex;
  align-items: center;
  gap: 15px;
}

.shape-label {
  color: #7c5f42;
  font-size: 13px;
  min-width: 40px;
}

.body-shape-slider {
  flex: 1;
  height: 8px;
  border-radius: 4px;
  background: linear-gradient(to right, #e8e0d5, #c9785a);
  outline: none;
  -webkit-appearance: none;
}

.body-shape-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #b5654b;
  cursor: pointer;
  border: 3px solid white;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
}

.body-shape-text {
  text-align: center;
  color: #b5654b;
  font-size: 14px;
  font-weight: 600;
  margin-top: 8px;
}

.password-form {
  background: #faf5f0;
  border-radius: 12px;
  padding: 20px;
}

.password-form .form-group input {
  width: 100%;
  padding: 12px;
  border: 2px solid #e8e0d5;
  border-radius: 8px;
  font-size: 14px;
  box-sizing: border-box;
}

.password-form .form-group input:focus {
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
  margin-bottom: 15px;
}

.success-msg {
  background: #f0fff4;
  color: #27ae60;
  padding: 12px;
  border-radius: 8px;
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 15px;
}

.btn-secondary {
  width: 100%;
  background: #faf5f0;
  color: #b5654b;
  border: 2px solid #b5654b;
  padding: 12px;
  border-radius: 10px;
  font-size: 15px;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
  transition: all 0.3s;
}

.btn-secondary:hover {
  background: #b5654b;
  color: white;
}

.btn-primary {
  width: 100%;
  background: linear-gradient(135deg, #b5654b, #c9785a);
  color: white;
  border: none;
  padding: 14px;
  border-radius: 10px;
  font-size: 15px;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
  transition: transform 0.2s, box-shadow 0.2s;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 20px rgba(181, 101, 75, 0.3);
}

.btn-logout {
  width: 100%;
  background: #fff;
  color: #d63031;
  border: 2px solid #d63031;
  padding: 14px;
  border-radius: 10px;
  font-size: 15px;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
  transition: all 0.3s;
}

.btn-logout:hover {
  background: #d63031;
  color: white;
}
</style>
