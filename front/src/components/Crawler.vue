<template>
  <div class="text-center my-4">
    <button @click="requestCrawl" class="btn btn-primary btn-lg" :disabled="isLoading">
      <span v-if="isLoading">🔄 수집 중...</span>
      <span v-else>최신 뉴스 크롤링하기</span>
    </button>
    <p class="mt-2 text-muted" v-if="lastUpdated">마지막 업데이트: {{ lastUpdated }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';

const emit = defineEmits(['refresh']); 
const isLoading = ref(false);
const lastUpdated = ref('');

const requestCrawl = async () => {
  isLoading.value = true;
  try {
    const response = await axios.post('http://127.0.0.1:8081/news/crawl');
    alert(response.data.message);
    lastUpdated.value = new Date().toLocaleString();
    
    emit('refresh'); 
  } catch (error) {
    alert("크롤링 실패!");
    console.error(error);
  } finally {
    isLoading.value = false;
  }
};
</script>