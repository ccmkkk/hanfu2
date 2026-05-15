<template>
  <div class="app">
    <div v-if="!currentView" class="main-menu">
      <div class="hero">
        <h1>🏮 中华衣裳</h1>
        <p> 汉服搭配 · 文化传承 · 同好交流</p>
      </div>

      <div v-if="isLoggedIn" class="user-welcome">
        <span>欢迎，{{ currentUserPhone }}</span>
        <button class="logout-btn" @click="handleLogout">
          <i class="fas fa-sign-out-alt"></i>
        </button>
      </div>

      <div class="menu-cards">
        <div class="menu-card" @click="currentView = 'recommend'">
          <i class="fas fa-tshirt"></i>
          <h2>汉服推荐</h2>
          <p>汉服智能搭配，可选朝代、肤色、季节</p>
        </div>
        <div class="menu-card" @click="currentView = 'forum'">
          <i class="fas fa-comments"></i>
          <h2>论坛讨论</h2>
          <p>同好分享，交流穿搭心得</p>
        </div>
        <div v-if="isLoggedIn" class="menu-card" @click="currentView = 'profile'">
          <i class="fas fa-user-circle"></i>
          <h2>个人信息</h2>
          <p>管理您的账号和偏好设置</p>
        </div>
        <div v-else class="menu-card" @click="currentView = 'login'">
          <i class="fas fa-sign-in-alt"></i>
          <h2>登录/注册</h2>
          <p>登录后享受个性化推荐服务</p>
        </div>
      </div>
      <footer class="main-footer">灵境·华裳 </footer>
    </div>

    <LoginView
      v-if="currentView === 'login'"
      @back="currentView = null"
      @toRegister="currentView = 'register'"
      @loginSuccess="handleLoginSuccess"
    />

    <RegisterView
      v-if="currentView === 'register'"
      @back="currentView = null"
      @toLogin="currentView = 'login'"
      @registerSuccess="handleRegisterSuccess"
    />

    <ProfileSetupView
      v-if="currentView === 'profileSetup'"
      @complete="handleProfileSetupComplete"
    />

    <ProfileView
      v-if="currentView === 'profile'"
      @back="currentView = null"
      @logout="handleLogout"
    />

    <RecommendView
      v-if="currentView === 'recommend'"
      @back="currentView = null"
      :defaultGender="recommendGender"
      :defaultSkinTone="recommendSkinTone"
      :defaultBodyShape="recommendBodyShape"
    />

    <ForumView v-if="currentView === 'forum'" @back="currentView = null" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import LoginView from './components/LoginView.vue'
import RegisterView from './components/RegisterView.vue'
import ProfileSetupView from './components/ProfileSetupView.vue'
import ProfileView from './components/ProfileView.vue'
import RecommendView from './components/RecommendView.vue'
import ForumView from './components/ForumView.vue'

const currentView = ref(null)
const isLoggedIn = ref(false)
const currentUserPhone = ref('')
const userProfile = ref({ gender: '', skinTone: '', bodyShape: 3 })

const recommendGender = computed(() => userProfile.value.gender || '')
const recommendSkinTone = computed(() => userProfile.value.skinTone || '暖皮')
const recommendBodyShape = computed(() => userProfile.value.bodyShape || 3)

onMounted(() => {
  checkLoginStatus()
})

function checkLoginStatus() {
  const phone = localStorage.getItem('hanfu_current_user')
  if (phone) {
    const users = JSON.parse(localStorage.getItem('hanfu_users') || '{}')
    const user = users[phone]
    if (user) {
      isLoggedIn.value = true
      currentUserPhone.value = phone
      userProfile.value = user.profile || { gender: '', skinTone: '', bodyShape: 3 }
    }
  }
}

function handleLoginSuccess(phone) {
  isLoggedIn.value = true
  currentUserPhone.value = phone

  const users = JSON.parse(localStorage.getItem('hanfu_users') || '{}')
  const user = users[phone]
  if (user && user.hasCompletedProfile) {
    userProfile.value = user.profile || { gender: '', skinTone: '', bodyShape: 3 }
    currentView.value = null
  } else {
    currentView.value = 'profileSetup'
  }
}

function handleRegisterSuccess(phone) {
  isLoggedIn.value = true
  currentUserPhone.value = phone
  currentView.value = 'profileSetup'
}

function handleProfileSetupComplete() {
  const phone = localStorage.getItem('hanfu_current_user')
  if (phone) {
    const users = JSON.parse(localStorage.getItem('hanfu_users') || '{}')
    const user = users[phone]
    if (user) {
      userProfile.value = user.profile || { gender: '', skinTone: '', bodyShape: 3 }
    }
  }
  currentView.value = null
}

function handleLogout() {
  isLoggedIn.value = false
  currentUserPhone.value = ''
  userProfile.value = { gender: '', skinTone: '', bodyShape: 3 }
  currentView.value = null
}
</script>

<style>
body {
  background-color: #f3efe7;
  background-image: radial-gradient(circle at 10% 20%, rgba(210, 180, 140, 0.05) 2%, transparent 2.5%);
  background-size: 30px 30px;
  font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
  color: #3e2a1f;
  margin: 0;
  padding: 0;
}
body.festival-midautumn {
  background: linear-gradient(145deg, #1a2a3a 0%, #0f1a24 100%);
  position: relative;
}
body.festival-midautumn::before {
  content: "🌕";
  font-size: 120px;
  position: fixed;
  bottom: 20px;
  right: 30px;
  opacity: 0.2;
  pointer-events: none;
  z-index: 0;
}
body.festival-spring {
  background: #fff0e0;
  position: relative;
}
body.festival-spring::after {
  content: "🧧";
  font-size: 80px;
  position: fixed;
  top: 20px;
  left: 20px;
  opacity: 0.15;
  pointer-events: none;
}
.main-menu {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 40px 20px;
}
.hero {
  text-align: center;
  margin-bottom: 40px;
}
.hero h1 {
  font-size: 5rem;
  color: #b5654b;
  margin-bottom: 30px;
}
.hero p {
  font-size: 1.2rem;
  color: #7c5f42;
}
.user-welcome {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 30px;
  padding: 12px 24px;
  background: rgba(181, 101, 75, 0.1);
  border-radius: 30px;
}
.user-welcome span {
  color: #b5654b;
  font-weight: 600;
}
.logout-btn {
  background: #b5654b;
  color: white;
  border: none;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.3s;
}
.logout-btn:hover {
  background: #8b4534;
}
.menu-cards {
  display: flex;
  gap: 30px;
  flex-wrap: wrap;
  justify-content: center;
}
.menu-card {
  background: #fff;
  border-radius: 20px;
  padding: 40px 30px;
  width: 280px;
  text-align: center;
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
}
.menu-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 15px 40px rgba(181, 101, 75, 0.2);
}
.menu-card i {
  font-size: 48px;
  color: #b5654b;
  margin-bottom: 20px;
}
.menu-card h2 {
  color: #3e2a1f;
  margin: 0 0 12px;
  font-size: 1.4rem;
}
.menu-card p {
  color: #7c5f42;
  font-size: 14px;
  line-height: 1.6;
}
.main-footer {
  margin-top: 60px;
  color: #b5654b;
  font-size: 14px;
  opacity: 0.8;
}
</style>
