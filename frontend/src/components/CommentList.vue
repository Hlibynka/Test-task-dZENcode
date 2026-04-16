<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import CommentItem from './CommentItem.vue'

const comments = ref([])
const loading = ref(true)
const error = ref(null)

const currentPage = ref(1)
const totalPages = ref(1)
const ordering = ref('-created_at')

const fetchComments = async () => {
  loading.value = true
  try {
    const response = await axios.get('http://localhost:8000/api/comments/', {
      params: {
        page: currentPage.value,
        ordering: ordering.value
      }
    })

    comments.value = response.data.results || response.data

    if (response.data.count) {
      totalPages.value = Math.ceil(response.data.count / 5)
    } else {
      totalPages.value = 1
    }

    loading.value = false
  } catch (e) {
    error.value = 'Помилка завантаження: ' + e.message
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
.comments-section {
  margin-top: 20px;
}
.controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
.sort-control select {
  padding: 5px;
  border-radius: 4px;
}
.pagination {
  margin-top: 30px;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 15px;
}
.pagination button {
  padding: 8px 15px;
  background-color: #f0f0f0;
  border: 1px solid #ccc;
  border-radius: 4px;
  cursor: pointer;
}
.pagination button:disabled {
  background-color: #f9f9f9;
  color: #aaa;
  cursor: not-allowed;
}
.pagination button:not(:disabled):hover {
  background-color: #e0e0e0;
}
.page-info {
  font-weight: 600;
}
</style>