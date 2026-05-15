<template>
  <div class="profile-setup-container">
    <div class="profile-panel">
      <div class="setup-header">
        <i class="fas fa-user-cog"></i>
        <h2>完善您的信息</h2>
        <p>这些信息将帮助我们为您推荐最适合的汉服</p>
      </div>

      <form @submit.prevent="handleSubmit" class="profile-form">
        <div class="form-group">
          <label><i class="fas fa-venus-mars"></i> 性别</label>
          <div class="option-buttons">
            <button
              type="button"
              v-for="gen in genderOptions"
              :key="gen.value"
              :class="['option-btn', { active: gender === gen.value }]"
              @click="gender = gen.value"
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
              :class="['option-btn', { active: skinTone === skin.value }]"
              @click="skinTone = skin.value"
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
              v-model.number="bodyShape"
              min="1"
              max="5"
              step="1"
              class="body-shape-slider"
            >
            <span class="shape-label">丰腴</span>
          </div>
          <div class="body-shape-text">{{ bodyShapeText }}</div>
        </div>

        <div v-if="errorMessage" class="error-msg">
          <i class="fas fa-exclamation-circle"></i> {{ errorMessage }}
        </div>

        <button type="submit" class="btn-primary" :disabled="loading">
          <i v-if="loading" class="fas fa-spinner fa-pulse"></i>
          <i v-else class="fas fa-check"></i>
          {{ loading ? '保存中...' : '完成设置' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const emit = defineEmits(['complete'])

const gender = ref('')
const skinTone = ref('')
const bodyShape = ref(3)
const errorMessage = ref('')
const loading = ref(false)

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
  return texts[bodyShape.value] || '标准体型'
})

function handleSubmit() {
  errorMessage.value = ''

  if (!gender.value) {
    errorMessage.value = '请选择您的性别'
    return
  }

  if (!skinTone.value) {
    errorMessage.value = '请选择您的肤色'
    return
  }

  loading.value = true

  const phone = localStorage.getItem('hanfu_current_user')
  if (phone) {
    const users = JSON.parse(localStorage.getItem('hanfu_users') || '{}')
    if (users[phone]) {
      users[phone].profile = {
        gender: gender.value,
        skinTone: skinTone.value,
        bodyShape: bodyShape.value
      }
      users[phone].hasCompletedProfile = true
      localStorage.setItem('hanfu_users', JSON.stringify(users))
    }
  }

  setTimeout(() => {
    loading.value = false
    emit('complete')
  }, 500)
}
</script>

<style scoped>
.profile-setup-container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
}

.profile-panel {
  background: #fff;
  border-radius: 20px;
  padding: 40px;
  width: 100%;
  max-width: 500px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
}

.setup-header {
  text-align: center;
  margin-bottom: 35px;
}

.setup-header i {
  font-size: 56px;
  color: #b5654b;
  margin-bottom: 15px;
}

.setup-header h2 {
  color: #3e2a1f;
  margin: 0 0 10px;
  font-size: 1.8rem;
}

.setup-header p {
  color: #7c5f42;
  font-size: 14px;
}

.profile-form {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.form-group > label {
  color: #3e2a1f;
  font-size: 16px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 10px;
}

.form-group > label i {
  color: #b5654b;
  width: 24px;
}

.option-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.option-btn {
  padding: 12px 20px;
  border: 2px solid #e8e0d5;
  border-radius: 10px;
  background: #fff;
  color: #3e2a1f;
  font-size: 15px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s;
}

.option-btn:hover {
  border-color: #c9785a;
  background: #faf5f0;
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
  width: 18px;
  height: 18px;
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
  width: 22px;
  height: 22px;
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
  margin-top: 5px;
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
  padding: 16px;
  border-radius: 10px;
  font-size: 16px;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
  transition: transform 0.2s, box-shadow 0.2s;
  margin-top: 10px;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 5px 20px rgba(181, 101, 75, 0.3);
}

.btn-primary:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}
</style>
