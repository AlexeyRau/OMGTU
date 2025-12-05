<script setup>
import { ref, onMounted, watch } from 'vue'
import ReactiveTable from '../components/ReactiveTable.vue'
import nobelService from '../services/nobelService'

const isLoading = ref(false)
const laureatesData = ref([])
const totalItems = ref(0)

const currentPage = ref(1)
const itemsPerPage = 10

const filters = ref({
  search: '',
  awardYear: ''
})

const columns = [
  { key: 'fullName', label: 'Полное имя' },
  { key: 'birthDate', label: 'Дата рождения' },
  { key: 'deathDate', label: 'Дата смерти' },
  { key: 'gender', label: 'Пол' },
  { key: 'prizeCount', label: 'Количество премий' }
]

async function loadLaureates() {
  isLoading.value = true

  try {
    const apiFilters = {}
    if (filters.value.search) {
      apiFilters.name = filters.value.search
    }
    if (filters.value.awardYear) {
      apiFilters.nobelPrizeYear = filters.value.awardYear
    }

    const response = await nobelService.getLaureates(
      currentPage.value - 1,
      itemsPerPage,
      apiFilters
    )

    laureatesData.value = response.laureates.map(laureate => {
      const fullName = laureate.fullName?.en ||
        `${laureate.givenName?.en || ''} ${laureate.familyName?.en || ''}`.trim()

      const birthDate = laureate.birth?.date || 'Неизвестно'
      const deathDate = laureate.death?.date || 'Жив'
      const gender = laureate.gender === 'male' ? 'Мужской' :
        laureate.gender === 'female' ? 'Женский' : 'Организация'

      const prizeCount = laureate.nobelPrizes?.length || 0

      return {
        fullName,
        birthDate,
        deathDate,
        gender,
        prizeCount
      }
    })

    totalItems.value = response.meta?.count || 0

  } catch (error) {
    console.error('Ошибка при загрузке лауреатов:', error)
    laureatesData.value = []
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
  loadLaureates()
}, { deep: true })

onMounted(() => {
  loadLaureates()
})
</script>

<template>
  <ReactiveTable :columns="columns" :data="laureatesData" :total-items="totalItems" :current-page="currentPage"
    :items-per-page="itemsPerPage" :filters="filters" :is-loading="isLoading" title="Лауреаты Нобелевских премий"
    @page-change="handlePageChange" @filter-change="handleFilterChange" />
</template>