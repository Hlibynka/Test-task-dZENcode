<script setup>
import { ref, defineProps } from 'vue'
import CommentForm from './CommentForm.vue'

const props = defineProps({
  comment: {
    type: Object,
    required: true
  },
  highlightedId: {
    type: Number,
    default: null
  }
})

const showReplyForm = ref(false)
const isLightboxOpen = ref(false)

const toggleLightbox = () => {
  isLightboxOpen.value = !isLightboxOpen.value
}
</script>

<template>
  <div
    :id="`comment-${comment.id}`"
    class="comment-item"
    :class="{ 'highlight-anim': Number(comment.id) === Number(highlightedId) }"
  >
    <div class="comment-header">
      <span class="user">{{ comment.user_name }}</span>
      <span v-if="comment.home_page" class="homepage-link">
        <a :href="comment.home_page" target="_blank" rel="noopener noreferrer">🏠</a>
      </span>
      <span class="date">{{ new Date(comment.created_at).toLocaleString() }}</span>
    </div>

    <div class="comment-body" v-html="comment.text"></div>

    <div v-if="comment.image" class="comment-file">
      <img :src="comment.image" alt="Прикріплене зображення" class="comment-image thumbnail" @click="toggleLightbox" />
    </div>

    <div v-if="comment.txt_file" class="comment-file">
      <a :href="comment.txt_file" target="_blank" class="txt-link">📄 Відкрити TXT файл</a>
    </div>

    <div class="comment-actions">
      <button class="reply-btn" @click="showReplyForm = !showReplyForm">
        {{ showReplyForm ? 'Скасувати' : 'Відповісти' }}
      </button>
    </div>

    <div v-if="showReplyForm" class="reply-form-wrapper">
      <CommentForm :parentId="comment.id" />
    </div>

    <div v-if="comment.replies && comment.replies.length > 0" class="replies">
      <CommentItem
        v-for="reply in comment.replies"
        :key="reply.id"
        :comment="reply"
        :highlighted-id="highlightedId"
      />
    </div>

    <div v-if="isLightboxOpen" class="lightbox-overlay" @click="toggleLightbox">
      <div class="lightbox-content" @click.stop>
        <button class="close-btn" @click="toggleLightbox">×</button>
        <img :src="comment.image" class="lightbox-image" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.comment-item {
  border: 1px solid #ddd;
  padding: 15px;
  margin-top: 15px;
  border-radius: 5px;
  background-color: #fff;
}
.comment-header { margin-bottom: 10px; font-size: 0.9em; color: #555; }
.user { font-weight: 600; margin-right: 5px; color: #333; }
.homepage-link { margin-right: 10px; text-decoration: none; }
.date { color: #888; float: right; }
.comment-body { line-height: 1.5; margin-bottom: 10px; word-break: break-word; }
.comment-file { margin-top: 10px; }
.thumbnail { max-width: 150px; cursor: pointer; transition: transform 0.2s; }
.thumbnail:hover { transform: scale(1.05); }
.txt-link { display: inline-block; padding: 5px 10px; background-color: #f0f0f0; text-decoration: none; color: #333; border-radius: 4px; border: 1px solid #ccc; }
.comment-actions { margin-top: 10px; }
.reply-btn { padding: 5px 10px; background-color: #2196F3; color: white; border: none; border-radius: 3px; cursor: pointer; }
.reply-btn:hover { background-color: #0b7dda; }
.reply-form-wrapper { margin-top: 15px; }
.replies { margin-left: 30px; border-left: 2px solid #eee; padding-left: 15px; }

/* modal window style */
.lightbox-overlay { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(0, 0, 0, 0.8); display: flex; justify-content: center; align-items: center; z-index: 1000; }
.lightbox-content { position: relative; max-width: 90%; max-height: 90%; }
.lightbox-image { max-width: 100%; max-height: 90vh; border: 3px solid #fff; border-radius: 5px; box-shadow: 0 5px 15px rgba(0,0,0,0.5); }
.close-btn { position: absolute; top: -15px; right: -15px; background: #f44336; color: white; border: none; border-radius: 50%; width: 30px; height: 30px; font-size: 20px; line-height: 28px; cursor: pointer; box-shadow: 0 2px 5px rgba(0,0,0,0.3); }
.close-btn:hover { background: #d32f2f; }

/* highlight animation */
.highlight-anim { animation: highlightFade 3s ease-out; }
@keyframes highlightFade {
  0% { background-color: #e8f5e9; border-color: #4CAF50; box-shadow: 0 0 10px rgba(76, 175, 80, 0.5); }
  100% { background-color: #fff; border-color: #ddd; box-shadow: none; }
}
</style>