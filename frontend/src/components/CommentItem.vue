<script setup>
import { ref, defineProps } from 'vue'
import CommentForm from './CommentForm.vue'

const props = defineProps({
  comment: {
    type: Object,
    required: true
  }
})

const showReplyForm = ref(false)
</script>

<template>
  <div class="comment-item">
    <div class="comment-header">
      <span class="user">{{ comment.user_name }}</span>
      <span class="date">{{ new Date(comment.created_at).toLocaleString() }}</span>
    </div>

    <div class="comment-body" v-html="comment.text"></div>

    <div v-if="comment.image" class="comment-file">
      <a :href="comment.image" target="_blank" rel="noopener noreferrer">
        <img :src="comment.image" alt="Прикріплене зображення" class="comment-image" />
      </a>
    </div>

    <div v-if="comment.txt_file" class="comment-file">
      <a :href="comment.txt_file" target="_blank" class="txt-link">
        Відкрити TXT файл
      </a>
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
      />
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
.comment-header {
  margin-bottom: 10px;
  font-size: 0.9em;
  color: #555;
}
.user {
  font-weight: 600;
  margin-right: 10px;
  color: #333;
}
.date {
  color: #888;
}
.comment-body {
  line-height: 1.5;
  margin-bottom: 10px;
}
.comment-file {
  margin-top: 10px;
}
.comment-image {
  max-width: 100%;
  border-radius: 4px;
  border: 1px solid #ccc;
  display: block;
}
.txt-link {
  display: inline-block;
  padding: 5px 10px;
  background-color: #f0f0f0;
  text-decoration: none;
  color: #333;
  border-radius: 4px;
  border: 1px solid #ccc;
}
.txt-link:hover {
  background-color: #e0e0e0;
}
.comment-actions {
  margin-top: 15px;
  margin-bottom: 5px;
}
.reply-btn {
  padding: 5px 10px;
  background-color: #2196F3;
  color: white;
  border: none;
  border-radius: 3px;
  cursor: pointer;
}
.reply-btn:hover {
  background-color: #0b7dda;
}
.reply-form-wrapper {
  margin-top: 10px;
  margin-bottom: 20px;
}
.replies {
  margin-left: 30px;
  border-left: 2px solid #eee;
  padding-left: 15px;
}
</style>