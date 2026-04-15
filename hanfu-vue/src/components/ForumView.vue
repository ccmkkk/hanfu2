<template>
  <div class="forum-container">
    <div class="back-button" @click="$emit('back')">
      <i class="fas fa-arrow-left"></i> 返回主菜单
    </div>
    <div class="forum-panel">
      <h2><i class="fas fa-comments"></i> 汉服交流论坛</h2>
      <div class="post-list">
        <div v-if="loading" class="loading">加载中...</div>
        <div v-else-if="posts.length === 0" class="empty">暂无帖子，快来发表第一条吧！</div>
        <div v-else>
          <div v-for="post in posts" :key="post.id" class="post-card">
            <div class="post-header">
              <span class="nickname"><i class="fas fa-user"></i> {{ post.nickname }}</span>
              <span class="time">{{ formatTime(post.time) }}</span>
            </div>
            <div class="post-content">{{ post.content }}</div>
            <div class="post-actions">
              <button class="like-btn" @click="likePost(post.id)">
                <i class="fas fa-heart" :class="{ liked: post.liked }"></i>
                <span>{{ post.likes }}</span>
              </button>
              <button class="comment-btn" @click="toggleCommentForm(post.id)">
                <i class="fas fa-comment"></i>
                <span>{{ post.comments.length }}</span>
              </button>
              <button class="delete-btn" @click="deletePost(post.id)">
                <i class="fas fa-trash"></i>
                <span>删除</span>
              </button>
            </div>
            
            <!-- 评论列表 -->
            <div class="comment-list" v-if="post.comments.length > 0">
              <div v-for="comment in post.comments" :key="comment.id" class="comment-item">
                <div class="comment-header">
                  <span class="comment-nickname">{{ comment.nickname }}</span>
                  <span class="comment-time">{{ formatTime(comment.time) }}</span>
                </div>
                <div class="comment-content">{{ comment.content }}</div>
                <div class="comment-actions">
                  <button class="comment-like-btn" @click="likeComment(post.id, comment.id)">
                    <i class="fas fa-heart" :class="{ liked: comment.liked }"></i>
                    <span>{{ comment.likes }}</span>
                  </button>
                  <button class="comment-delete-btn" @click="deleteComment(post.id, comment.id)">
                    <i class="fas fa-trash"></i>
                    <span>删除</span>
                  </button>
                </div>
              </div>
            </div>
            
            <!-- 评论输入框 -->
            <div class="comment-form" v-if="openCommentForm === post.id">
              <input type="text" v-model="commentNickname" placeholder="昵称（选填，默认匿名）" maxlength="20">
              <textarea v-model="commentContent" rows="2" placeholder="写下你的评论..."></textarea>
              <button @click="submitComment(post.id)" :disabled="!commentContent.trim()">发布评论</button>
            </div>
          </div>
          <div v-if="hasMore" class="load-more" @click="loadMore">加载更多</div>
        </div>
      </div>
      <div class="post-form">
        <input type="text" v-model="nickname" placeholder="昵称（选填，默认匿名）" maxlength="20">
        <textarea v-model="newContent" rows="3" placeholder="分享你的汉服心得、搭配经验..."></textarea>
        <button @click="submitPost" :disabled="!newContent.trim()">发布帖子</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

defineEmits(['back'])

const posts = ref([])
const loading = ref(false)
const hasMore = ref(true)
const page = ref(1)
const nickname = ref('')
const newContent = ref('')
const commentNickname = ref('')
const commentContent = ref('')
const openCommentForm = ref(null)

const formatTime = (timestamp) => {
  const date = new Date(timestamp)
  return `${date.getMonth()+1}/${date.getDate()} ${date.getHours()}:${date.getMinutes().toString().padStart(2,'0')}`
}

const getPostsFromLocalStorage = () => {
  const postsData = localStorage.getItem('forumPosts')
  return postsData ? JSON.parse(postsData) : []
}

const savePostsToLocalStorage = (postsData) => {
  localStorage.setItem('forumPosts', JSON.stringify(postsData))
}

const fetchPosts = async (reset = true) => {
  if (reset) {
    page.value = 1
    posts.value = []
    hasMore.value = true
  }
  if (!hasMore.value) return
  loading.value = true
  try {
    const allPosts = getPostsFromLocalStorage()
    const perPage = 20
    const startIndex = (page.value - 1) * perPage
    const endIndex = startIndex + perPage
    const newPosts = allPosts.slice(startIndex, endIndex)
    
    if (newPosts.length === 0) {
      hasMore.value = false
    } else {
      const processedPosts = newPosts.map(post => ({
        ...post,
        likes: post.likes || 0,
        liked: post.liked || false,
        comments: post.comments || []
      }))
      posts.value = reset ? processedPosts : [...posts.value, ...processedPosts]
      hasMore.value = newPosts.length === perPage
      page.value++
    }
  } catch (err) {
    console.error('获取帖子失败', err)
  } finally {
    loading.value = false
  }
}

const submitPost = async () => {
  if (!newContent.value.trim()) return
  try {
    const allPosts = getPostsFromLocalStorage()
    const newPost = {
      id: Date.now(),
      nickname: nickname.value || '匿名',
      content: newContent.value,
      time: new Date().toISOString(),
      likes: 0,
      liked: false,
      comments: []
    }
    allPosts.unshift(newPost)
    savePostsToLocalStorage(allPosts)
    newContent.value = ''
    nickname.value = ''
    await fetchPosts(true)
  } catch (err) {
    alert('发布失败，请稍后再试')
  }
}

const loadMore = () => {
  fetchPosts(false)
}

const likePost = (postId) => {
  const post = posts.value.find(p => p.id === postId)
  if (post) {
    if (!post.liked) {
      post.likes++
      post.liked = true
    } else {
      post.likes--
      post.liked = false
    }
    
    // 更新localStorage中的数据
    const allPosts = getPostsFromLocalStorage()
    const updatedPosts = allPosts.map(p => {
      if (p.id === postId) {
        return { ...p, likes: post.likes, liked: post.liked }
      }
      return p
    })
    savePostsToLocalStorage(updatedPosts)
  }
}

const deletePost = (postId) => {
  if (confirm('确定要删除这篇帖子吗？')) {
    try {
      // 从localStorage中删除帖子
      const allPosts = getPostsFromLocalStorage()
      const updatedPosts = allPosts.filter(p => p.id !== postId)
      savePostsToLocalStorage(updatedPosts)
      
      // 更新当前显示的帖子列表
      posts.value = posts.value.filter(p => p.id !== postId)
    } catch (err) {
      console.error('删除帖子失败', err)
      alert('删除失败，请稍后再试')
    }
  }
}

const toggleCommentForm = (postId) => {
  if (openCommentForm.value === postId) {
    openCommentForm.value = null
  } else {
    openCommentForm.value = postId
    commentNickname.value = ''
    commentContent.value = ''
  }
}

const submitComment = (postId) => {
  if (!commentContent.value.trim()) return
  try {
    const allPosts = getPostsFromLocalStorage()
    const postIndex = allPosts.findIndex(p => p.id === postId)
    if (postIndex !== -1) {
      const newComment = {
        id: Date.now(),
        nickname: commentNickname.value || '匿名',
        content: commentContent.value,
        time: new Date().toISOString(),
        likes: 0,
        liked: false
      }
      allPosts[postIndex].comments = allPosts[postIndex].comments || []
      allPosts[postIndex].comments.unshift(newComment)
      savePostsToLocalStorage(allPosts)
      
      // 更新当前显示的帖子
      const post = posts.value.find(p => p.id === postId)
      if (post) {
        post.comments = allPosts[postIndex].comments
      }
      
      commentNickname.value = ''
      commentContent.value = ''
      openCommentForm.value = null
    }
  } catch (err) {
    console.error('发布评论失败', err)
    alert('发布评论失败，请稍后再试')
  }
}

const likeComment = (postId, commentId) => {
  const post = posts.value.find(p => p.id === postId)
  if (post) {
    const comment = post.comments.find(c => c.id === commentId)
    if (comment) {
      if (!comment.liked) {
        comment.likes++
        comment.liked = true
      } else {
        comment.likes--
        comment.liked = false
      }
      
      // 更新localStorage中的数据
      const allPosts = getPostsFromLocalStorage()
      const postIndex = allPosts.findIndex(p => p.id === postId)
      if (postIndex !== -1) {
        const commentIndex = allPosts[postIndex].comments.findIndex(c => c.id === commentId)
        if (commentIndex !== -1) {
          allPosts[postIndex].comments[commentIndex] = comment
          savePostsToLocalStorage(allPosts)
        }
      }
    }
  }
}

const deleteComment = (postId, commentId) => {
  if (confirm('确定要删除这条评论吗？')) {
    try {
      // 从localStorage中删除评论
      const allPosts = getPostsFromLocalStorage()
      const postIndex = allPosts.findIndex(p => p.id === postId)
      if (postIndex !== -1) {
        allPosts[postIndex].comments = allPosts[postIndex].comments.filter(c => c.id !== commentId)
        savePostsToLocalStorage(allPosts)
        
        // 更新当前显示的帖子
        const post = posts.value.find(p => p.id === postId)
        if (post) {
          post.comments = post.comments.filter(c => c.id !== commentId)
        }
      }
    } catch (err) {
      console.error('删除评论失败', err)
      alert('删除评论失败，请稍后再试')
    }
  }
}

onMounted(() => {
  fetchPosts()
})
</script>

<style scoped>
.forum-container {
  padding: 20px;
}
.back-button {
  margin-bottom: 20px;
  cursor: pointer;
  display: inline-block;
  background: #b5654b;
  color: white;
  padding: 6px 15px;
  border-radius: 30px;
  font-size: 0.9rem;
}
.forum-panel {
  max-width: 800px;
  margin: 0 auto;
  background: rgba(255,250,240,0.95);
  border-radius: 28px;
  padding: 24px;
  box-shadow: 0 8px 20px rgba(0,0,0,0.08);
}
h2 {
  color: #b5654b;
  text-align: center;
  margin-bottom: 20px;
}
.post-list {
  max-height: 500px;
  overflow-y: auto;
  margin-bottom: 20px;
}
.post-card {
  background: #fef6ef;
  border-radius: 20px;
  padding: 12px 16px;
  margin-bottom: 12px;
  border-left: 5px solid #b5654b;
}
.post-header {
  display: flex;
  justify-content: space-between;
  font-size: 0.8rem;
  color: #8b694c;
  margin-bottom: 8px;
}
.nickname {
  font-weight: bold;
}
.post-content {
  line-height: 1.4;
  margin-bottom: 10px;
}
.post-actions {
  display: flex;
  justify-content: flex-end;
  align-items: center;
}
.like-btn, .delete-btn, .comment-btn {
  background: none;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 0.9rem;
  margin-left: 15px;
}
.like-btn {
  color: #b5654b;
}
.delete-btn {
  color: #e74c3c;
}
.comment-btn {
  color: #b5654b;
}

/* 评论相关样式 */
.comment-list {
  margin-top: 15px;
  padding-top: 15px;
  border-top: 1px solid #e2cfbc;
}
.comment-item {
  background: #faf5f0;
  border-radius: 15px;
  padding: 10px 12px;
  margin-bottom: 10px;
  border-left: 3px solid #b5654b;
}
.comment-header {
  display: flex;
  justify-content: space-between;
  font-size: 0.75rem;
  color: #8b694c;
  margin-bottom: 5px;
}
.comment-nickname {
  font-weight: bold;
}
.comment-content {
  line-height: 1.3;
  margin-bottom: 8px;
  font-size: 0.9rem;
}
.comment-actions {
  display: flex;
  justify-content: flex-end;
  align-items: center;
}
.comment-like-btn, .comment-delete-btn {
  background: none;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 3px;
  font-size: 0.8rem;
  margin-left: 10px;
}
.comment-like-btn {
  color: #b5654b;
}
.comment-delete-btn {
  color: #e74c3c;
}
.comment-like-btn i.liked {
  color: #e74c3c;
  animation: likeAnimation 0.3s ease;
}

.comment-form {
  margin-top: 15px;
  padding: 15px;
  background: #faf5f0;
  border-radius: 15px;
  border: 1px solid #e2cfbc;
}
.comment-form input, .comment-form textarea {
  width: 100%;
  padding: 8px;
  margin-bottom: 8px;
  border: 1px solid #e2cfbc;
  border-radius: 15px;
  background: white;
  font-size: 0.85rem;
}
.comment-form button {
  background: #b5654b;
  color: white;
  border: none;
  padding: 6px 15px;
  border-radius: 30px;
  cursor: pointer;
  font-size: 0.85rem;
  float: right;
}
.like-btn i.liked {
  color: #e74c3c;
  animation: likeAnimation 0.3s ease;
}
@keyframes likeAnimation {
  0% { transform: scale(1); }
  50% { transform: scale(1.2); }
  100% { transform: scale(1); }
}
.load-more {
  text-align: center;
  color: #b5654b;
  cursor: pointer;
  padding: 8px;
  background: #f0e3d8;
  border-radius: 30px;
  margin-top: 10px;
}
.post-form {
  border-top: 1px solid #e2cfbc;
  padding-top: 20px;
}
.post-form input, .post-form textarea {
  width: 100%;
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #e2cfbc;
  border-radius: 20px;
  background: white;
  font-size: 0.9rem;
}
.post-form button {
  background: #b5654b;
  color: white;
  border: none;
  padding: 8px 20px;
  border-radius: 30px;
  cursor: pointer;
}
.loading, .empty {
  text-align: center;
  padding: 40px;
  color: #b5654b;
}
</style>