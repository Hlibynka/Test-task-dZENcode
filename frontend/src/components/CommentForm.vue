<script setup>
import { ref, defineProps } from 'vue'
import axios from 'axios'

const props = defineProps({
  parentId: {
    type: Number,
    default: null
  }
})

const userName = ref('')
const email = ref('')
const text = ref('')
const imageFile = ref(null)
const txtFile = ref(null)
const message = ref('')

const handleImageUpload = (event) => {
  imageFile.value = event.target.files[0]
}

const handleTxtUpload = (event) => {
  txtFile.value = event.target.files[0]
}

const insertTag = (tagOpen, tagClose) => {
  text.value += `${tagOpen}${tagClose}`
}

const submitComment = async () => {
  try {
    const formData = new FormData()
    formData.append('user_name', userName.value)
    formData.append('email', email.value)
    formData.append('text', text.value)

    if (imageFile.value) {
      formData.append('image', imageFile.value)
    }
    if (txtFile.value) {
      formData.append('txt_file', txtFile.value)
    }
    if (props.parentId) {
      formData.append('parent', props.parentId)
    }

    const response = await axios.post('http://localhost:8000/api/comments/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })

    message.value = 'Успішно! Оновіть сторінку, щоб побачити зміни.'

    userName.value = ''
    email.value = ''
    text.value = ''
    imageFile.value = null
    txtFile.value = null

    const imgInput = document.getElementById(`image-input-${props.parentId || 'main'}`)
    if (imgInput) imgInput.value = ''

    const txtInput = document.getElementById(`txt-input-${props.parentId || 'main'}`)
    if (txtInput) txtInput.value = ''

  } catch (error) {
    message.value = 'Помилка: ' + JSON.stringify(error.response?.data || error.message)
  }
}
</script>

<template>
  <div class="form-container">
    <h3 v-if="parentId">Відповісти на коментар</h3>
    <h2 v-else>Додати коментар</h2>

    <form @submit.prevent="submitComment">
      <div class="form-group">
        <label>Ім'я (тільки латиниця та цифри):</label>
        <input v-model="userName" type="text" required pattern="[A-Za-z0-9]+" title="Тільки латинські літери та цифри">
      </div>

      <div class="form-group">
        <label>Email:</label>
        <input v-model="email" type="email" required>
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
        <label>Текст повідомлення:</label>
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

      <button type="submit" class="submit-btn">Відправити</button>
    </form>

    <p v-if="message" class="message">{{ message }}</p>
  </div>
</template>

<style scoped>
.form-container {
  margin-top: 15px;
  margin-bottom: 30px;
  padding: 15px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #f9f9f9;
}
.form-group {
  margin-bottom: 15px;
}
.files-group {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
}
.tag-buttons {
  display: flex;
  gap: 10px;
  margin-bottom: 5px;
}
.tag-buttons button {
  padding: 5px 10px;
  background-color: #e0e0e0;
  border: 1px solid #ccc;
  border-radius: 3px;
  cursor: pointer;
}
.tag-buttons button:hover {
  background-color: #d0d0d0;
}
label {
  display: block;
  margin-bottom: 5px;
}
input[type="text"], input[type="email"], textarea {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
}
.submit-btn {
  padding: 10px 15px;
  cursor: pointer;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
}
.submit-btn:hover {
  background-color: #45a049;
}
.message {
  margin-top: 15px;
  color: #d32f2f;
}
</style>