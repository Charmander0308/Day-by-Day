<template>
  <div class="container py-5">
    <h1 class="text-center mb-5">📰 Day by Day</h1>
    
    <Crawler @refresh="fetchNews" />

    <hr />

    <NewsList :newsList="newsData" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import Crawler from './components/Crawler.vue';
import NewsList from './components/NewsList.vue';

const newsData = ref([]);

const fetchNews = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8081/news');
    newsData.value = response.data;
  } catch (error) {
    console.error("데이터 로드 실패", error);
  }
};

onMounted(() => {
  fetchNews(); // 앱 켜지자마자 실행
});
</script>