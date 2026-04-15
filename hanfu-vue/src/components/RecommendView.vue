<template>
  <div class="recommend-container">
    <div class="back-button" @click="$emit('back')">
      <i class="fas fa-arrow-left"></i> 返回主菜单
    </div>
    <div class="recommend-dashboard">
      <!-- 左侧：用户画像编辑器 -->
      <div class="card-panel user-editor">
        <div class="editor-title"><i class="fas fa-user-circle"></i> 画中人 · 定制</div>

        <!-- 体型滑块（无业务逻辑） -->
        <div class="control-group">
          <label><i class="fas fa-chart-line"></i> 体型 (纤瘦→丰腴)</label>
          <input type="range" v-model="bodyShape" min="1" max="5" step="1">
        </div>

        <!-- 肤色：冷白皮、暖黄皮、通用 -->
        <div class="control-group">
          <label><i class="fas fa-palette"></i> 肤色</label>
          <div class="skin-options">
            <button v-for="skin in skinOptions" :key="skin.value"
                    :class="['skin-btn', { active: skin_tone === skin.value }]"
                    @click="skin_tone = skin.value">
              {{ skin.label }}
            </button>
          </div>
        </div>

        <!-- 性别 -->
        <div class="control-group">
          <label><i class="fas fa-venus-mars"></i> 性别</label>
          <div class="gender-options">
            <button v-for="gen in genderOptions" :key="gen.value"
                    :class="['gender-btn', { active: gender === gen.value }]"
                    @click="gender = gen.value">
              {{ gen.label }}
            </button>
          </div>
        </div>

        <!-- 朝代 -->
        <div class="control-group">
          <label><i class="fas fa-landmark"></i> 朝代</label>
          <select v-model="dynasty">
            <option v-for="d in dynasties" :key="d" :value="d">{{ d }}制</option>
          </select>
        </div>

        <!-- 季节 -->
        <div class="control-group">
          <label><i class="fas fa-leaf"></i> 季节</label>
          <select v-model="season">
            <option value="春">春</option><option value="夏">夏</option>
            <option value="秋">秋</option><option value="冬">冬</option>
          </select>
        </div>

        <!-- 场景 -->
        <div class="control-group">
          <label><i class="fas fa-umbrella-beach"></i> 场景</label>
          <select v-model="scene">
            <option v-for="s in scenes" :key="s" :value="s">{{ s }}</option>
          </select>
        </div>

        <button class="btn-primary" @click="getRecommend">
          <i class="fas fa-magic"></i> 灵境推荐
        </button>
      </div>

      <!-- 中央：试衣镜 + 推荐列表 -->
      <div class="mirror-area">
        <div class="outfit-display">
          <div class="outfit-img">
            <i class="fas fa-user-circle"></i>
            <div class="outfit-name">{{ currentOutfit ? currentOutfit.套装 : '华裳未启' }}</div>
            <div v-if="currentOutfit" class="outfit-detail">
              🎨 {{ currentOutfit.颜色 }} &nbsp;| 🌸 {{ currentOutfit.纹样 }}<br>
              ⭐ 综合评分: {{ currentOutfit.综合评分 || currentOutfit.朝代兼容分 }}
            </div>
            <div v-else class="outfit-detail">点击推荐套装预览</div>
          </div>
        </div>
        <div class="recommend-list">
          <div v-if="loading" class="loading"><i class="fas fa-spinner fa-pulse"></i> 霓裳推演中...</div>
          <div v-else-if="recommendList.length === 0" class="loading">😔 暂无匹配推荐，调整选项试试</div>
          <div v-else>
            <div v-for="(item, idx) in recommendList" :key="idx"
                 :class="['rec-card', { active: currentIndex === idx }]"
                 @click="setActiveRecommendation(idx)">
              <div class="rec-title">🏮 {{ item.套装 }}</div>
              <div class="rec-score">🎯 综合评分: {{ item.综合评分 || item.朝代兼容分 }}</div>
              <div class="rec-colors">{{ item.颜色 }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧：文化解读 -->
      <div class="card-panel culture-box">
        <div class="editor-title"><i class="fas fa-feather-alt"></i> 华裳文脉</div>
        <div class="meaning-section">
          <div class="meaning-label"><i class="fas fa-paintbrush"></i> 纹样寓意</div>
          <div class="meaning-text">{{ patternMeaning }}</div>
        </div>
        <div class="meaning-section">
          <div class="meaning-label"><i class="fas fa-vest"></i> 制式解读</div>
          <div class="meaning-text">{{ styleMeaning }}</div>
        </div>
        <div class="meaning-section">
          <div class="meaning-label"><i class="fas fa-star-of-life"></i> 综合寓意</div>
          <div class="meaning-text">{{ comprehensiveMeaning }}</div>
        </div>
      </div>

      <!-- 底部控制栏 -->
      <div class="bottom-bar">
        <div>
          <button class="icon-btn" @click="toggleFestival" :title="festivalEnabled ? '关闭特效' : '开启节令特效'">
            <i :class="festivalEnabled ? 'fas fa-sun' : 'fas fa-moon'"></i>
          </button>
          <button class="share-btn" @click="shareOutfit"><i class="fas fa-share-alt"></i> 分享穿搭</button>
        </div>
        <div class="season-info">
          <i class="fas fa-cloud-sun"></i> <span>{{ seasonInfoText }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

defineEmits(['back'])

// ===================== 用户选项 =====================
const bodyShape = ref(3)
const skin_tone = ref('暖黄皮')
const gender = ref('女')
const dynasty = ref('唐')
const season = ref('春')
const scene = ref('日常')

const skinOptions = [
  { label: '冷白皮', value: '冷白皮' },
  { label: '暖黄皮', value: '暖黄皮' },
  { label: '通用', value: '' }
]
const genderOptions = [
  { label: '女', value: '女' },
  { label: '男', value: '男' },
  { label: '通用', value: '' }
]
const dynasties = ['唐', '宋', '明', '汉', '魏晋', '南北朝', '隋', '五代十国', '辽', '金', '元']
const scenes = ['日常', '通勤', '出游', '拍照', '结婚', '礼仪']

// ===================== 推荐数据 =====================
const loading = ref(false)
const recommendList = ref([])
const currentIndex = ref(0)
const currentOutfit = computed(() => recommendList.value[currentIndex.value] || null)

// 寓意拆分
const patternMeaning = ref('—')
const styleMeaning = ref('—')
const comprehensiveMeaning = ref('—')

// 节令特效
const festivalEnabled = ref(false)

// 季节信息
const seasonInfoText = ref('')
const seasonInfoFromApi = ref({ season: '春', fabric: '真丝', layers: '2-3层', festival: null })

// ===================== API 调用 =====================
async function getRecommend() {
  loading.value = true
  try {
    const payload = {
      season: season.value,
      scene: scene.value,
      dynasty: dynasty.value,
      gender: gender.value,
      skin_tone: skin_tone.value
    }
    const res = await axios.post('/api/recommend', payload)
    const list = res.data['推荐方案'] || []
    recommendList.value = list
    if (list.length > 0) {
      currentIndex.value = 0
      updateMeaningPanel(list[0])
    } else {
      patternMeaning.value = styleMeaning.value = comprehensiveMeaning.value = '—'
    }
  } catch (err) {
    console.error(err)
    alert('请求失败，请检查后端是否启动！')
    recommendList.value = []
  } finally {
    loading.value = false
  }
}

function parseMeaning(meaningStr) {
  if (!meaningStr) return { pattern: '—', style: '—', comprehensive: '—' }
  if (meaningStr.includes('【纹样寓意】') && meaningStr.includes('【制式解读】')) {
    const patternMatch = meaningStr.match(/【纹样寓意】(.*?)【制式解读】/)
    const styleMatch = meaningStr.match(/【制式解读】(.*?)【整体寓意】/)
    const overallMatch = meaningStr.match(/【整体寓意】(.*)/)
    return {
      pattern: patternMatch ? patternMatch[1].trim() : '—',
      style: styleMatch ? styleMatch[1].trim() : '—',
      comprehensive: overallMatch ? overallMatch[1].trim() : meaningStr
    }
  }
  return { pattern: meaningStr, style: '传统制式，端庄典雅', comprehensive: meaningStr }
}

function updateMeaningPanel(item) {
  patternMeaning.value = item.纹样寓意 || '—'
  styleMeaning.value = item.制式解读 || '—'
  comprehensiveMeaning.value = item.寓意 || '—'
}

function setActiveRecommendation(idx) {
  currentIndex.value = idx
  updateMeaningPanel(recommendList.value[idx])
}

// ===================== 节令感知 =====================
async function fetchSeasonInfo() {
  try {
    const res = await axios.get('/api/season_info')
    const data = res.data
    seasonInfoFromApi.value = data
    seasonInfoText.value = `${data.season}季 · ${data.fabric} ${data.layers}`
    applyColorScheme(data.color_scheme)
    if (data.festival && !festivalEnabled.value) {
      festivalEnabled.value = true
      toggleFestival()
    }
  } catch (err) {
    console.warn('季节信息获取失败', err)
    seasonInfoText.value = '春 · 真丝 2-3层'
  }
}

function applyColorScheme(colors) {
  if (!colors) return
  document.documentElement.style.setProperty('--season-primary', colors.primary)
  document.documentElement.style.setProperty('--season-secondary', colors.secondary)
  document.body.style.backgroundColor = colors.primary
}

function toggleFestival() {
  festivalEnabled.value = !festivalEnabled.value
  const body = document.body
  if (festivalEnabled.value) {
    const festival = seasonInfoFromApi.value.festival
    if (festival === '中秋') {
      body.classList.add('festival-midautumn')
      body.classList.remove('festival-spring')
    } else if (festival === '春节') {
      body.classList.add('festival-spring')
      body.classList.remove('festival-midautumn')
    } else {
      body.classList.add('festival-midautumn')
    }
  } else {
    body.classList.remove('festival-midautumn', 'festival-spring')
  }
}

// ===================== 分享功能 =====================
async function shareOutfit() {
  if (!currentOutfit.value) {
    alert('请先获取推荐')
    return
  }
  const item = currentOutfit.value
  const shareText = `【汉服推荐】${item.套装} | 配色:${item.颜色} | 纹样:${item.纹样} | 寓意:${item.寓意} —— 来自灵境华裳AI推荐`
  try {
    await navigator.clipboard.writeText(shareText)
    alert('✅ 穿搭文案已复制，分享给朋友吧！')
  } catch (err) {
    alert('手动复制吧：' + shareText)
  }
}

onMounted(() => {
  fetchSeasonInfo()
  getRecommend()
})
</script>

<style scoped>
.recommend-dashboard {
  max-width: 1400px;
  margin: 20px auto;
  padding: 20px;
  display: grid;
  grid-template-columns: 280px 1fr 320px;
  gap: 24px;
  align-items: start;
}
.back-button {
  margin: 10px 20px;
  cursor: pointer;
  display: inline-block;
  background: #b5654b;
  color: white;
  padding: 6px 15px;
  border-radius: 30px;
  font-size: 0.9rem;
  width: fit-content;
}
.card-panel {
  background: rgba(255, 250, 240, 0.92);
  backdrop-filter: blur(2px);
  border-radius: 28px;
  box-shadow: 0 8px 20px rgba(0,0,0,0.08);
  padding: 20px;
  border: 1px solid #eeddcc;
}
.user-editor {
  position: sticky;
  top: 20px;
}
.editor-title {
  font-size: 1.3rem;
  font-weight: 600;
  border-left: 5px solid #b5654b;
  padding-left: 12px;
  margin-bottom: 20px;
  color: #5a3e2b;
}
.control-group {
  margin-bottom: 20px;
}
.control-group label {
  display: block;
  font-weight: 500;
  margin-bottom: 8px;
  color: #7c5f42;
  font-size: 0.9rem;
}
input[type="range"] {
  width: 100%;
  accent-color: #b5654b;
}
.skin-options, .gender-options {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}
.skin-btn, .gender-btn {
  background: #f0e3d8;
  border: none;
  padding: 6px 14px;
  border-radius: 40px;
  cursor: pointer;
  font-size: 0.85rem;
  transition: 0.2s;
}
.skin-btn.active, .gender-btn.active {
  background: #b5654b;
  color: white;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}
select, .btn-primary {
  width: 100%;
  padding: 10px 12px;
  border-radius: 40px;
  border: 1px solid #e2cfbc;
  background: white;
  font-size: 0.9rem;
  outline: none;
}
.btn-primary {
  background: #b5654b;
  color: white;
  font-weight: bold;
  cursor: pointer;
  transition: 0.2s;
  border: none;
  margin-top: 10px;
}
.btn-primary:hover {
  background: #9b4a32;
  transform: translateY(-2px);
}
.mirror-area {
  background: #fffaf5;
  border-radius: 36px;
  box-shadow: 0 15px 30px rgba(0,0,0,0.1);
  overflow: hidden;
}
.outfit-display {
  background: #f9efe5;
  min-height: 280px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px;
  border-bottom: 1px solid #e6d5c5;
}
.outfit-img {
  width: 100%;
  max-width: 240px;
  background: #e8d9ce;
  border-radius: 32px;
  padding: 20px;
  text-align: center;
  box-shadow: inset 0 0 0 1px rgba(255,255,240,0.8), 0 8px 18px rgba(0,0,0,0.05);
}
.outfit-img i {
  font-size: 80px;
  color: #c09a7a;
  margin-bottom: 10px;
}
.outfit-name {
  font-size: 1.2rem;
  font-weight: bold;
  margin: 15px 0 5px;
}
.outfit-detail {
  font-size:0.8rem;
  color:#a27c62;
}
.recommend-list {
  padding: 20px;
  max-height: 320px;
  overflow-y: auto;
}
.rec-card {
  background: #fef6ef;
  border-radius: 20px;
  padding: 12px 16px;
  margin-bottom: 12px;
  cursor: pointer;
  transition: 0.1s;
  border: 1px solid #f0e0d0;
}
.rec-card.active {
  border: 2px solid #b5654b;
  background: #fff3ea;
  box-shadow: 0 4px 12px rgba(181,101,75,0.2);
}
.rec-card:hover {
  transform: translateX(4px);
}
.rec-title {
  font-weight: bold;
}
.rec-score {
  font-size: 0.8rem;
  color: #b5654b;
}
.rec-colors {
  font-size:0.75rem;
  color:#8b694c;
}
.culture-box {
  position: sticky;
  top: 20px;
}
.meaning-section {
  margin-bottom: 20px;
  padding-bottom: 12px;
  border-bottom: 1px dashed #e2cfbc;
}
.meaning-label {
  font-weight: bold;
  color: #b5654b;
  margin-bottom: 6px;
  font-size: 0.9rem;
}
.meaning-text {
  line-height: 1.5;
  font-size: 0.9rem;
  color: #4a3729;
}
.bottom-bar {
  grid-column: 1 / -1;
  background: #f0e7dd;
  border-radius: 60px;
  padding: 12px 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 15px;
  margin-top: 10px;
}
.season-info {
  font-size: 0.85rem;
  background: #fff3e8;
  padding: 6px 15px;
  border-radius: 50px;
}
.icon-btn {
  background: none;
  border: none;
  font-size: 1.4rem;
  cursor: pointer;
  margin: 0 8px;
  color: #7c5f42;
}
.share-btn {
  background: #b5654b;
  color: white;
  padding: 6px 18px;
  border-radius: 30px;
  font-size: 0.9rem;
  border: none;
  cursor: pointer;
}
.loading {
  text-align: center;
  padding: 40px;
  color: #b5654b;
}
@media (max-width: 1000px) {
  .recommend-dashboard {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  .user-editor, .culture-box {
    position: static;
  }
}
</style>