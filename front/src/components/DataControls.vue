<template>
  <div class="d-flex justify-content-end align-items-center mt-3 gap-2">
    
    <button @click="resetNews" class="btn btn-outline-danger shadow-sm">
      전체 초기화
    </button>

    <div class="vr mx-2"></div> <div class="input-group shadow-sm" style="width: auto;">
      <span class="input-group-text bg-white">표본</span>
      <select class="form-select" v-model="exportCount" style="max-width: 120px;">
        <option :value="null">전체</option>
        <option :value="10">최신 10개</option>
        <option :value="30">최신 30개</option>
        <option :value="50">최신 50개</option>
        <option :value="100">최신 100개</option>
      </select>
      <button @click="downloadExcel" class="btn btn-success">
        📊 엑셀 저장
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';

// 부모에게 신호를 보낼 수 있는 이벤트 정의
const emit = defineEmits(['refresh']);

const exportCount = ref(null);

// 뉴스 데이터 초기화
const resetNews = async () => {
  if(!confirm("정말 모든 뉴스를 삭제하시겠습니까?")) return;

  try {
    await axios.delete('http://127.0.0.1:8081/news/reset');
    alert("초기화되었습니다.");
    
    // 부모 컴포넌트에게 목록 갱신하라고 신호 보냄
    emit('refresh'); 
  } catch (error) {
    console.error("초기화 실패", error);
    alert("초기화 중 오류가 발생했습니다.");
  }
};

// 엑셀 다운로드
const downloadExcel = () => {
  let url = 'http://127.0.0.1:8081/news/export';
  if (exportCount.value) {
    url += `?limit=${exportCount.value}`;
  }
  window.location.href = url;
};
</script>

<style scoped>
</style>