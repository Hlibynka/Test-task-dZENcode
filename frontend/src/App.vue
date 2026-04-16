<script setup>
import { ref } from 'vue'
import axios from 'axios'
import CommentForm from './components/CommentForm.vue'
import CommentList from './components/CommentList.vue'

const username = ref('')
const password = ref('')
const token = ref(localStorage.getItem('access_token') || '')

// if token in memory - add to task
if (token.value) {
  axios.defaults.headers.common['Authorization'] = `Bearer ${token.value}`
}

const logout = () => {
  token.value = ''
  localStorage.removeItem('access_token')
  delete axios.defaults.headers.common['Authorization']
}

const login = async () => {
  try {
    const response = await axios.post('http://localhost:8000/api/token/', {
      username: username.value,
      password: password.value
    })
    token.value = response.data.access
    localStorage.setItem('access_token', token.value)

    axios.defaults.headers.common['Authorization'] = `Bearer ${token.value}`
    alert('Успішний вхід!')
  } catch (error) {
    alert('Неправильний логін або пароль')
  }
}

// Interceptor for loging off
axios.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      logout() // Автоматичний вихід
      alert('Час дії вашої сесії (JWT) минув. Будь ласка, увійдіть знову.')
    }
    return Promise.reject(error)
  }
)
</script>

<template>
  <div class="app-container">
    <header class="auth-panel">
      <h1>Система коментарів</h1>

      <div v-if="!token" class="login-form">
        <input v-model="username" type="text" placeholder="Логін адміна">
        <input v-model="password" type="password" placeholder="Пароль">
        <button @click="login" class="login-btn">Увійти</button>
      </div>

      <div v-else class="logged-in">
        <span>✅ Авторизовано </span>
        <button @click="logout" class="logout-btn">Вийти</button>
      </div>
    </header>

    <main>
      <div v-if="!token" class="warning-msg">
        Щоб залишити коментар, необхідно авторизуватися.
      </div>

      <CommentForm v-if="token" />
      <hr>
      <CommentList />
    </main>
  </div>
</template>

<style scoped>
.app-container { max-width: 900px; margin: 0 auto; padding: 20px; font-family: Arial, sans-serif; }
.auth-panel { display: flex; justify-content: space-between; align-items: center; background: #333; color: white; padding: 15px 20px; border-radius: 8px; margin-bottom: 20px; }
.auth-panel h1 { margin: 0; font-size: 1.5em; }
.login-form { display: flex; gap: 10px; }
.login-form input { padding: 8px; border-radius: 4px; border: none; }
.login-btn { background: #4CAF50; color: white; border: none; padding: 8px 15px; border-radius: 4px; cursor: pointer; }
.logout-btn { background: #f44336; color: white; border: none; padding: 8px 15px; border-radius: 4px; cursor: pointer; margin-left: 15px; }
.warning-msg { background: #fff3cd; color: #856404; padding: 15px; border-radius: 4px; border: 1px solid #ffeeba; margin-bottom: 20px; text-align: center; }
hr { margin: 30px 0; border: 0; border-top: 1px solid #eee; }
</style>