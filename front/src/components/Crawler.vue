<template>
  <p class="mt-2 text-muted" v-if="lastUpdated">마지막 업데이트: {{ lastUpdated }}</p>

  <div class="card p-4 shadow-sm bg-light border-0">
    <div class="row g-2 align-items-center">
      
      <div class="col-md-5">
        <div class="input-group">
          <span class="input-group-text bg-white border-end-0">🔍</span>
          <input 
            type="text" 
            class="form-control border-start-0" 
            v-model="keyword" 
            placeholder="검색어 입력 (예: 에듀테크)"
            @keyup.enter="requestCrawl"
          >
        </div>
      </div>

      <div class="col-md-2">
        <select class="form-select" v-model="sort">
          <option value="recency">최신순</option>
          <option value="accuracy">정확도순</option>
        </select>
      </div>

      <div class="col-md-2">
        <select class="form-select" v-model="limit">
          <option :value="10">10개</option>
          <option :value="30">30개</option>
          <option :value="50">50개</option>
          <option :value="100">100개</option>
        </select>
      </div>

      <div class="col-md-3">
        <button 
          @click="requestCrawl" 
          class="btn btn-primary w-100 fw-bold" 
          :disabled="isLoading"
        >
          <span v-if="isLoading" class="spinner-border spinner-border-sm me-2"></span>
          {{ isLoading ? '수집 중...' : '최신 뉴스 가져오기' }}
        </button>
      </div>

    </div>
    
    <div class="text-end mt-2">
      <small class="text-muted">
        키워드: <span class="fw-bold text-dark">{{ keyword }}</span> | 
        목표 개수: <span class="fw-bold text-dark">{{ limit }}개</span>
      </small>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';

const emit = defineEmits(['refresh']); 

const keyword = ref("");
const limit = ref(10);
const sort = ref("recency");
const isLoading = ref(false);
const lastUpdated = ref('');

const requestCrawl = async () => {
  if (!keyword.value.trim()) {
    alert("검색어를 입력해주세요!");
    return;
  }

  isLoading.value = true;
  try {
    const response = await axios.post(
      'http://127.0.0.1:8081/news/crawl',
      null, 
      {
        params: {
          keyword: keyword.value,
          limit: limit.value,
          sort: sort.value
        }
      }
    );
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

<style scoped>
.form-control:focus, .form-select:focus {
  box-shadow: none;
  border-color: #0d6efd;
}
</style>