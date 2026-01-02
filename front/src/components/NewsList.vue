<template>
  <div>
    <div class="row">
      <div class="col-md-12 mb-3" v-for="(news, index) in paginatedNews" :key="news.id || index">
        <div class="card shadow-sm">
          <div class="card-body">
            <h5 class="card-title">
              <a :href="news.link" target="_blank" class="text-decoration-none text-dark">
                {{ news.title }}
              </a>
            </h5>
            <p class="card-text text-muted small">링크: {{ news.link }}</p>
          </div>
        </div>
      </div>
      
      <div v-if="newsList.length === 0" class="text-center text-muted mt-5">
        데이터가 없습니다.
      </div>
    </div>

    <nav v-if="newsList.length > 0" aria-label="Page navigation" class="mt-4">
      <ul class="pagination justify-content-center">
        
        <li class="page-item" :class="{ disabled: currentPage === 1 }">
          <a class="page-link" href="#" @click.prevent="changePage(currentPage - 1)">이전</a>
        </li>

        <li 
          v-for="page in totalPages" 
          :key="page" 
          class="page-item" 
          :class="{ active: currentPage === page }"
        >
          <a class="page-link" href="#" @click.prevent="changePage(page)">
            {{ page }}
          </a>
        </li>

        <li class="page-item" :class="{ disabled: currentPage === totalPages }">
          <a class="page-link" href="#" @click.prevent="changePage(currentPage + 1)">다음</a>
        </li>

      </ul>
    </nav>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';

const props = defineProps({
  newsList: {
    type: Array,
    default: () => []
  }
});

const currentPage = ref(1);    // 현재 보고 있는 페이지
const itemsPerPage = 10;       // 한 페이지당 보여줄 개수

// 전체 페이지 수 계산 
const totalPages = computed(() => {
  return Math.ceil(props.newsList.length / itemsPerPage);
});

// 현재 페이지에 보여줄 뉴스들만 자르기 
const paginatedNews = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  const end = start + itemsPerPage;
  return props.newsList.slice(start, end);
});

// 페이지 변경 함수
const changePage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page;
  }
};

// 뉴스 데이터를 새로 불러오면 1페이지로 리셋
watch(() => props.newsList, () => {
  currentPage.value = 1;
});
</script>

<style scoped>
.card:hover { transform: translateY(-3px); transition: 0.2s; }
.page-link { cursor: pointer; } 
</style>