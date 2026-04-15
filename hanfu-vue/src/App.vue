<template>
  <div class="app">
    <div v-if="!currentView" class="main-menu">
      <div class="hero">
        <h1>🏮 中华衣裳</h1>
        <p> 汉服搭配 · 文化传承 · 同好交流</p>
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
      </div>
      <footer class="main-footer">灵境·华裳 </footer>
    </div>
    <RecommendView v-if="currentView === 'recommend'" @back="currentView = null" />
    <ForumView v-if="currentView === 'forum'" @back="currentView = null" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import RecommendView from './components/RecommendView.vue'
import ForumView from './components/ForumView.vue'

const currentView = ref(null)
</script>

<style>
/* 全局样式 */
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
  margin-bottom: 60px;
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
.menu-cards {
  display: flex;
  gap: 40px;
  flex-wrap: wrap;
  justify-content: center;
}
.menu-card {
  background: rgba(255,250,240,0.95);
  backdrop-filter: blur(4px);
  border-radius: 40px;
  padding: 40px 30px;
  width: 260px;
  text-align: center;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  box-shadow: 0 10px 20px rgba(0,0,0,0.1);
  border: 1px solid #eeddcc;
}
.menu-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 30px rgba(0,0,0,0.15);
}
.menu-card i {
  font-size: 3rem;
  color: #b5654b;
  margin-bottom: 20px;
}
.menu-card h2 {
  font-size: 1.8rem;
  margin-bottom: 10px;
  color: #5a3e2b;
}
.menu-card p {
  color: #8b694c;
}
.main-footer {
  margin-top: 60px;
  font-size: 0.8rem;
  color: #b7a287;
}
</style>