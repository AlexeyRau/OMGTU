<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import ReactiveTable from '../components/ReactiveTable.vue'
import NobelService from '../services/nobelService'

const prizesData = ref([])
const loading = ref(true)
const error = ref(null)

const pagination = ref({
  currentPage: 1,
  totalPages: 1,
  totalItems: 0,
  itemsPerPage: 20
})

const filters = ref({
  year: '',
  category: '',
  yearTo: ''
})

const columns = [
  { key: 'awardYear', label: 'Год' },
  { key: 'category', label: 'Категория' },
  { key: 'laureates', label: 'Лауреаты' },
  { key: 'prizeAmount', label: 'Сумма' },
  { key: 'prizeAmountAdjusted', label: 'Сумма (скорр.)' }
]

async function loadPrizes() {
  try {
    loading.value = true
    error.value = null

    const offset = (pagination.value.currentPage - 1) * pagination.value.itemsPerPage

    const options = {
      offset,
      limit: pagination.value.itemsPerPage,
      sort: 'desc'
    }

    if (filters.value.year) options.nobelPrizeYear = parseInt(filters.value.year)
    if (filters.value.yearTo) options.yearTo = parseInt(filters.value.yearTo)
    if (filters.value.category) options.nobelPrizeCategory = filters.value.category

    const response = await NobelService.getNobelPrizes(options)

    prizesData.value = response.nobelPrizes.map(prize => ({
      awardYear: prize.awardYear,
      category: prize.category?.en || prize.categoryFullName?.en || 'Неизвестно',
      laureates: prize.laureates?.map(l => l.knownName?.en || l.fullName?.en || 'Неизвестно').join(', ') || 'Нет лауреатов',
      prizeAmount: prize.prizeAmount ? `${prize.prizeAmount.toLocaleString()} SEK` : 'Н/Д',
      prizeAmountAdjusted: prize.prizeAmountAdjusted ? `${prize.prizeAmountAdjusted.toLocaleString()} SEK` : 'Н/Д'
    }))

    if (response.meta) {
      pagination.value.totalItems = response.meta.count || 0
      pagination.value.totalPages = Math.ceil(pagination.value.totalItems / pagination.value.itemsPerPage)
    }

  } catch (err) {
    error.value = 'Ошибка при загрузке данных. Пожалуйста, попробуйте позже.'
    console.error(err)
  } finally {
    loading.value = false
  }
}

function handlePageChange(newPage) {
  pagination.value.currentPage = newPage
  loadPrizes()
}

function handleFilterChange(filter) {
  if (filter.type === 'year') {
    filters.value.year = filter.value
  } else if (filter.type === 'category') {
    filters.value.category = filter.value
  } else if (filter.type === 'yearTo') {
    filters.value.yearTo = filter.value
  }

  pagination.value.currentPage = 1
  loadPrizes()
}

function applyFilters() {
  pagination.value.currentPage = 1
  loadPrizes()
}

function resetFilters() {
  filters.value = { year: '', category: '', yearTo: '' }
  pagination.value.currentPage = 1
  loadPrizes()
}

onMounted(() => {
  loadPrizes()
})

const categoryOptions = [
  { value: '', label: 'Все категории' },
  { value: 'phy', label: 'Физика' },
  { value: 'che', label: 'Химия' },
  { value: 'med', label: 'Медицина' },
  { value: 'lit', label: 'Литература' },
  { value: 'pea', label: 'Мир' },
  { value: 'eco', label: 'Экономика' }
]
</script>

<template>
  <div>
    <ReactiveTable :columns="columns" :data="prizesData" :pagination="pagination" :loading="loading"
      title="Нобелевские премии" @page-change="handlePageChange" @filter-change="handleFilterChange">
      <template #filters="{ applyFilter }">
        <div class="filters-container">
          <h3>Фильтры</h3>
          <div class="filter-group">
            <div class="filter-item">
              <label>Год с:</label>
              <input type="number" v-model="filters.year" placeholder="Например: 2000" min="1901"
                @change="applyFilters" />
            </div>

            <div class="filter-item">
              <label>Год по:</label>
              <input type="number" v-model="filters.yearTo" placeholder="Например: 2020" min="1901"
                @change="applyFilters" />
            </div>

            <div class="filter-item">
              <label>Категория:</label>
              <select v-model="filters.category" @change="applyFilters">
                <option v-for="option in categoryOptions" :key="option.value" :value="option.value">
                  {{ option.label }}
                </option>
              </select>
            </div>

            <button @click="resetFilters" class="reset-btn">
              Сбросить фильтры
            </button>
          </div>

          <div v-if="error" class="error-message">
            {{ error }}
          </div>
        </div>
      </template>
    </ReactiveTable>
  </div>
</template>

<style scoped>
.filters-container {
  padding: 15px;
}

.filters-container h3 {
  margin-bottom: 15px;
  color: #2c3e50;
}

.filter-group {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  align-items: flex-end;
}

.filter-item {
  display: flex;
  flex-direction: column;
  min-width: 200px;
}

.filter-item label {
  margin-bottom: 5px;
  font-weight: bold;
  color: #34495e;
}

.filter-item input,
.filter-item select {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.filter-item input:focus,
.filter-item select:focus {
  outline: none;
  border-color: #1abc9c;
  box-shadow: 0 0 0 2px rgba(26, 188, 156, 0.2);
}

.reset-btn {
  padding: 8px 16px;
  background-color: #e74c3c;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
  height: fit-content;
}

.reset-btn:hover {
  background-color: #c0392b;
}

.error-message {
  margin-top: 15px;
  padding: 10px;
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
  border-radius: 4px;
}

@media (max-width: 768px) {
  .filter-group {
    flex-direction: column;
    align-items: stretch;
  }

  .filter-item {
    min-width: auto;
  }
}
</style>