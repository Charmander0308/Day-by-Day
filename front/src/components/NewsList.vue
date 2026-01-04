<template>
  <div>
    <div class="row">
      <div class="col-md-12 mb-4" v-for="(news, index) in paginatedNews" :key="news.id || index">
        <div class="card h-100 shadow-sm border-0">
          <div class="row g-0 align-items-center">
            
            <div class="col-md-3 text-center bg-light d-flex align-items-center justify-content-center" 
                 style="min-height: 160px;" v-if="news.image_url">
              <img 
                :src="news.image_url" 
                class="img-fluid rounded shadow-sm" 
                alt="news thumbnail"
                style="max-height: 150px; object-fit: cover;"
              >
            </div>
            <div class="col-md-3 text-center bg-light d-flex align-items-center justify-content-center" 
                 style="min-height: 160px;" v-else>
               <span class="text-muted small">No Image</span>
            </div>

            <div :class="news.image_url ? 'col-md-9' : 'col-md-12'">
              <div class="card-body p-4">
                <div class="mb-2">
                  <span class="badge bg-light text-secondary fw-normal border">
                    수집일: {{ formatDate(news.created_at) }}
                  </span>
                </div>

                <h5 class="card-title fw-bold mb-3">
                  <a :href="news.link" target="_blank" class="text-decoration-none text-dark hover-blue">
                    {{ news.title }}
                  </a>
                </h5>

                <p class="card-text text-muted mb-3 text-truncate-2" style="font-size: 0.95rem; line-height: 1.6;">
                  {{ news.description }}
                </p>

                <div class="text-end">
                  <a :href="news.link" target="_blank" class="btn btn-secondary btn-sm px-3">
                    원문 보기 <i class="bi bi-arrow-right-short"></i>
                  </a>
                </div>
              </div>
            </div>

          </div>
        </div>
      </div>
    </div>

    <nav v-if="newsList.length > 0" class="mt-4">
      <ul class="pagination justify-content-center">
        <li class="page-item" :class="{ disabled: currentPage === 1 }">
          <a class="page-link" href="#" @click.prevent="changePage(currentPage - 1)">이전</a>
        </li>
        <li v-for="page in visiblePages" :key="page" class="page-item" :class="{ active: currentPage === page }">
          <a class="page-link" href="#" @click.prevent="changePage(page)">{{ page }}</a>
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
  newsList: { type: Array, default: () => [] }
});

const currentPage = ref(1);
const itemsPerPage = 10;
const maxVisibleButtons = 5;

const totalPages = computed(() => Math.ceil(props.newsList.length / itemsPerPage));
const paginatedNews = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  return props.newsList.slice(start, start + itemsPerPage);
});

// 페이지 버튼 5개 계산해서 화면에 출력하는 로직
const visiblePages = computed(() => {
  const total = totalPages.value;
  
  // 전체 페이지가 5개 이하라면 그냥 다 보여줌
  if (total <= maxVisibleButtons) {
    return Array.from({ length: total }, (_, i) => i + 1);
  }

  // 현재 페이지를 가운데 두고 앞뒤로 계산 (ex: 현재가 10이면 8,9,10,11,12)
  let start = currentPage.value - Math.floor(maxVisibleButtons / 2);
  let end = start + maxVisibleButtons - 1;

  // 시작이 1보다 작으면 강제로 1~5로 맞춤
  if (start < 1) {
    start = 1;
    end = maxVisibleButtons;
  }

  // 끝이 전체 페이지보다 크면 뒤에서부터 5개로 맞춤 (예: 16~20)
  if (end > total) {
    end = total;
    start = total - maxVisibleButtons + 1;
  }

  // 계산된 start부터 end까지 배열 생성
  const pages = [];
  for (let i = start; i <= end; i++) {
    pages.push(i);
  }
  return pages;
});

const changePage = (page) => {
  if (page >= 1 && page <= totalPages.value) currentPage.value = page;
};

// 날짜 포맷팅 함수 (선택사항)
const formatDate = (dateStr) => {
  if (!dateStr) return '';
  const date = new Date(dateStr);
  return date.toLocaleDateString();
};

watch(() => props.newsList, () => { currentPage.value = 1; });
</script>

<style scoped>
.card { transition: transform 0.2s; }
.card:hover { transform: scale(1.01); }
.hover-blue:hover { color: #0d6efd !important; }
.text-truncate-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>