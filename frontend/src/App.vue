<script setup>
import CommentList from './components/CommentList.vue'
import CommentForm from './components/CommentForm.vue'
</script>

<template>
  <main class="container">
    <h1>Система коментарів</h1>
    <CommentForm />
    <hr>
    <CommentList />
  </main>
</template>

<style>
.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  font-family: sans-serif;
}
hr {
  margin: 40px 0;
  border: 1px solid #ddd;
}
</style>