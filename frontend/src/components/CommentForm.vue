<script setup>
import { ref, defineProps, onMounted, nextTick } from 'vue'
import axios from 'axios'

const props = defineProps({
  parentId: {
    type: Number,
    default: null
  }
})

const userName = ref('')
const email = ref('')
const homePage = ref('')
const text = ref('')
const imageFile = ref(null)
const txtFile = ref(null)

const captchaKey = ref('')
const captchaImageUrl = ref('')
const captchaValue = ref('')

const message = ref('')
const isPreview = ref(false)

const loadCaptcha = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/comments/get-captcha/')
    captchaKey.value = response.data.captcha_key
    captchaImageUrl.value = response.data.captcha_image
  } catch (error) {
    console.error('Помилка завантаження капчі')
  }
}

onMounted(() => {
  loadCaptcha()
})

const handleImageUpload = (event) => {
  imageFile.value = event.target.files[0]
}

const handleTxtUpload = (event) => {
  txtFile.value = event.target.files[0]
}

const insertTag = (tagOpen, tagClose) => {
  text.value += `${tagOpen}${tagClose}`
}

const togglePreview = async () => {
  if (text.value || userName.value) {
    isPreview.value = !isPreview.value

    if (isPreview.value) {
      await nextTick()
      const previewElement = document.querySelector('.preview-box')

      if (previewElement) {
        previewElement.scrollIntoView({ behavior: 'smooth', block: 'start' })
      }
    }
  }
}

const submitComment = async () => {
  try {
    const formData = new FormData()
    formData.append('user_name', userName.value)
    formData.append('email', email.value)
    if (homePage.value) formData.append('home_page', homePage.value)
    formData.append('text', text.value)
    formData.append('captcha_key', captchaKey.value)
    formData.append('captcha_value', captchaValue.value)

    if (imageFile.value) formData.append('image', imageFile.value)
    if (txtFile.value) formData.append('txt_file', txtFile.value)
    if (props.parentId) formData.append('parent', props.parentId)

    await axios.post('http://localhost:8000/api/comments/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })

    message.value = 'Успішно! Оновіть сторінку, щоб побачити зміни.'

    // clear
    userName.value = ''
    email.value = ''
    homePage.value = ''
    text.value = ''
    captchaValue.value = ''
    imageFile.value = null
    txtFile.value = null
    isPreview.value = false
    loadCaptcha() // reload captcha

    const imgInput = document.getElementById(`image-input-${props.parentId || 'main'}`)
    if (imgInput) imgInput.value = ''
    const txtInput = document.getElementById(`txt-input-${props.parentId || 'main'}`)
    if (txtInput) txtInput.value = ''

  } catch (error) {
    message.value = 'Помилка: ' + JSON.stringify(error.response?.data || error.message)
    loadCaptcha() // error - new captcha
  }
}
</script>

<template>
  <div class="form-container">
    <h3 v-if="parentId">Відповісти на коментар</h3>
    <h2 v-else>Додати коментар</h2>

    <div v-if="isPreview" class="preview-box">
      <h4>Попередній перегляд:</h4>
      <div class="preview-header">
        <strong>{{ userName || 'Анонім' }}</strong>
        <span v-if="homePage"> ({{ homePage }})</span>
      </div>
      <div class="preview-body" v-html="text"></div>
      <button @click="togglePreview" class="btn-secondary">Повернутися до редагування</button>
    </div>

    <form v-show="!isPreview" @submit.prevent="submitComment">
      <div class="form-group">
        <label>Ім'я (тільки латиниця та цифри): *</label>
        <input v-model="userName" type="text" required pattern="[A-Za-z0-9]+" title="Тільки латинські літери та цифри">
      </div>

      <div class="form-group">
        <label>Email: *</label>
        <input v-model="email" type="email" required>
      </div>

      <div class="form-group">
        <label>Home page (URL):</label>
        <input v-model="homePage" type="url" placeholder="https://...">
      </div>

      <div class="form-group">
        <label>Теги:</label>
        <div class="tag-buttons">
          <button type="button" @click="insertTag('<a>', '</a>')">&lt;a&gt;</button>
          <button type="button" @click="insertTag('<code>', '</code>')">&lt;code&gt;</button>
          <button type="button" @click="insertTag('<i>', '</i>')">&lt;i&gt;</button>
          <button type="button" @click="insertTag('<strong>', '</strong>')">&lt;strong&gt;</button>
        </div>
      </div>

      <div class="form-group">
        <label>Текст повідомлення: *</label>
        <textarea v-model="text" required rows="5"></textarea>
      </div>

      <div class="form-group files-group">
        <div>
          <label>Зображення (JPG, PNG, GIF):</label>
          <input :id="`image-input-${parentId || 'main'}`" type="file" accept=".jpg,.jpeg,.png,.gif" @change="handleImageUpload">
        </div>
        <div>
          <label>Текстовий файл (TXT до 100КБ):</label>
          <input :id="`txt-input-${parentId || 'main'}`" type="file" accept=".txt" @change="handleTxtUpload">
        </div>
      </div>

      <div class="form-group captcha-group">
        <label>CAPTCHA: *</label>
        <div class="captcha-box">
          <img v-if="captchaImageUrl" :src="captchaImageUrl" alt="captcha" class="captcha-img" @click="loadCaptcha" title="Натисніть, щоб оновити">
          <input v-model="captchaValue" type="text" required placeholder="Введіть код">
        </div>
      </div>

      <div class="actions">
        <button type="button" @click="togglePreview" class="btn-secondary">Попередній перегляд</button>
        <button type="submit" class="submit-btn">Відправити</button>
      </div>
    </form>

    <p v-if="message" class="message">{{ message }}</p>
  </div>
</template>

<style scoped>
.form-container { margin-bottom: 30px; padding: 20px; border: 1px solid #ccc; border-radius: 5px; background-color: #f9f9f9; }
.form-group { margin-bottom: 15px; }
.files-group { display: flex; gap: 20px; margin-bottom: 20px; }
.captcha-group { margin-bottom: 20px; }
.captcha-box { display: flex; align-items: center; gap: 10px; }
.captcha-img { cursor: pointer; border: 1px solid #ddd; border-radius: 4px; }
.tag-buttons { display: flex; gap: 10px; margin-bottom: 5px; }
.tag-buttons button { padding: 5px 10px; background-color: #e0e0e0; border: 1px solid #ccc; border-radius: 3px; cursor: pointer; }
.tag-buttons button:hover { background-color: #d0d0d0; }
label { display: block; margin-bottom: 5px; font-weight: 500; }
input[type="text"], input[type="email"], input[type="url"], textarea { width: 100%; padding: 8px; box-sizing: border-box; }
.actions { display: flex; gap: 10px; }
.submit-btn { padding: 10px 15px; cursor: pointer; background-color: #4CAF50; color: white; border: none; border-radius: 4px; }
.submit-btn:hover { background-color: #45a049; }
.btn-secondary { padding: 10px 15px; cursor: pointer; background-color: #2196F3; color: white; border: none; border-radius: 4px; }
.btn-secondary:hover { background-color: #0b7dda; }
.preview-box { padding: 15px; background: #fff; border: 1px dashed #2196F3; border-radius: 5px; margin-bottom: 15px; }
.preview-header { margin-bottom: 10px; font-size: 0.9em; color: #555; }
.preview-body { line-height: 1.5; margin-bottom: 15px; }
.message { margin-top: 15px; color: #d32f2f; font-weight: bold; }
</style>