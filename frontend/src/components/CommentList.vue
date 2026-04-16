<script setup>
import { ref, onMounted, onUnmounted, nextTick} from 'vue'
import axios from 'axios'
import CommentItem from './CommentItem.vue'

const comments = ref([])
const loading = ref(true)
const error = ref(null)

const currentPage = ref(1)
const totalPages = ref(1)
const ordering = ref('-created_at')

const highlightedCommentId = ref(null)
let socket = null

// Background loading
const fetchComments = async (isBackground = false) => {
  if (!isBackground) loading.value = true

  try {
    const response = await axios.get('http://localhost:8000/api/comments/', {
      params: {
        page: currentPage.value,
        ordering: ordering.value,
        timestamp: new Date().getTime() // skip cache
      }
    })

    comments.value = response.data.results || response.data

    if (response.data.count) {
      totalPages.value = Math.ceil(response.data.count / 25)
    } else {
      totalPages.value = 1
    }
  } catch (e) {
    error.value = 'Помилка завантаження: ' + e.message
  } finally {
    loading.value = false
  }
}

const changePage = (pageNumber) => {
  if (pageNumber >= 1 && pageNumber <= totalPages.value) {
    currentPage.value = pageNumber
    fetchComments()
  }
}

const changeSort = () => {
  currentPage.value = 1
  fetchComments()
}

onMounted(() => {
  fetchComments()

  socket = new WebSocket('ws://localhost:8000/ws/comments/')

socket.onmessage = (event) => {
    const data = JSON.parse(event.data)
    if (data.type === 'new_comment') {

      currentPage.value = 1

      fetchComments(true).then(async () => {
        if (data.comment_id) {
          const newId = Number(data.comment_id)

          // wait for new comment
          await nextTick()

          // highlight on
          highlightedCommentId.value = newId

          // scroll to new comment
          const newCommentEl = document.getElementById(`comment-${newId}`)
          if (newCommentEl) {
            newCommentEl.scrollIntoView({ behavior: 'smooth', block: 'center' })
          }

          // highlight off in 3 sec
          setTimeout(() => {
            highlightedCommentId.value = null
          }, 3000)
        }
      })
    }
  }

  socket.onclose = () => {
    console.log('WebSocket з\'єднання закрито')
  }
})

onUnmounted(() => {
  if (socket) socket.close()
})
</script>

<template>
  <div class="comments-section">
    <div class="controls">
      <h2>Список коментарів</h2>

      <div class="sort-control">
        <label>Сортувати за: </label>
        <select v-model="ordering" @change="changeSort">
          <option value="-created_at">Нові спочатку (Дата)</option>
          <option value="created_at">Старі спочатку (Дата)</option>
          <option value="user_name">Ім'я (А-Я)</option>
          <option value="-user_name">Ім'я (Я-А)</option>
          <option value="email">Email (А-Я)</option>
          <option value="-email">Email (Я-А)</option>
        </select>
      </div>
    </div>

    <div v-if="loading">Завантаження...</div>
    <div v-else-if="error">{{ error }}</div>
    <div v-else-if="comments.length === 0">Коментарів ще немає. Будьте першим!</div>
    <div v-else class="comment-list">
      <CommentItem
        v-for="comment in comments"
        :key="comment.id"
        :comment="comment"
        :highlighted-id="highlightedCommentId"
      />
    </div>

    <div v-if="totalPages > 1" class="pagination">
      <button
        :disabled="currentPage === 1"
        @click="changePage(currentPage - 1)"
      >
        Попередня
      </button>

      <span class="page-info">Сторінка {{ currentPage }} з {{ totalPages }}</span>

      <button
        :disabled="currentPage === totalPages"
        @click="changePage(currentPage + 1)"
      >
        Наступна
      </button>
    </div>
  </div>
</template>

<style scoped>
.comments-section { margin-top: 20px; }
.controls { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.sort-control select { padding: 5px; border-radius: 4px; }
.pagination { margin-top: 30px; display: flex; justify-content: center; align-items: center; gap: 15px; }
.pagination button { padding: 8px 15px; background-color: #f0f0f0; border: 1px solid #ccc; border-radius: 4px; cursor: pointer; }
.pagination button:disabled { background-color: #f9f9f9; color: #aaa; cursor: not-allowed; }
.pagination button:not(:disabled):hover { background-color: #e0e0e0; }
.page-info { font-weight: 600; }
</style>