<script setup>
import { ref, onMounted, watch } from 'vue'
import ReactiveTable from '../components/ReactiveTable.vue'
import nobelService from '../services/nobelService'

const isLoading = ref(false)
const prizesData = ref([])
const totalItems = ref(0)

const currentPage = ref(1)
const itemsPerPage = 10

const filters = ref({
  search: '',
  awardYear: ''
})

const columns = [
  { key: 'category', label: 'Категория' },
  { key: 'awardYear', label: 'Год вручения' },
  { key: 'dateAwarded', label: 'Дата вручения' },
  { key: 'prizeAmount', label: 'Размер премии' },
  { key: 'laureateCount', label: 'Количество лауреатов' }
]

async function loadPrizes() {
  isLoading.value = true

  try {
    const apiFilters = {}
    if (filters.value.search) {
      apiFilters.category = filters.value.search
    }
    if (filters.value.awardYear) {
      apiFilters.nobelPrizeYear = filters.value.awardYear
    }

    const response = await nobelService.getNobelPrizes(
      currentPage.value - 1,
      itemsPerPage,
      apiFilters
    )

    prizesData.value = response.nobelPrizes.map(prize => {
      const category = prize.category?.en || prize.categoryFullName?.en || 'Неизвестно'
      const awardYear = prize.awardYear || 'Неизвестно'
      const dateAwarded = prize.dateAwarded || 'Не указано'
      const prizeAmount = prize.prizeAmount ? `${prize.prizeAmount} ${prize.currency || ''}`.trim() : 'Не указано'
      const laureateCount = prize.laureates?.length || 0

      return {
        category,
        awardYear,
        dateAwarded,
        prizeAmount,
        laureateCount
      }
    })

    totalItems.value = response.meta?.count || 0

  } catch (error) {
    console.error('Ошибка при загрузке премий:', error)
    prizesData.value = []
    totalItems.value = 0
  } finally {
    isLoading.value = false
  }
}

function handlePageChange(page) {
  currentPage.value = page
}

function handleFilterChange(newFilters) {
  filters.value = newFilters
  currentPage.value = 1
}

watch([currentPage, filters], () => {
  loadPrizes()
}, { deep: true })

onMounted(() => {
  loadPrizes()
})
</script>

<template>
  <ReactiveTable :columns="columns" :data="prizesData" :total-items="totalItems" :current-page="currentPage"
    :items-per-page="itemsPerPage" :filters="filters" :is-loading="isLoading" title="Нобелевские премии"
    @page-change="handlePageChange" @filter-change="handleFilterChange" />
</template>