<script setup>
import { ref, onMounted } from 'vue'
import ReactiveTable from '../components/ReactiveTable.vue'
import NobelService from '../services/nobelService'

const laureatesData = ref([])
const loading = ref(true)
const error = ref(null)

const pagination = ref({
  currentPage: 1,
  totalPages: 1,
  totalItems: 0,
  itemsPerPage: 20
})

const filters = ref({
  name: '',
  gender: '',
  category: ''
})

const columns = [
  { key: 'name', label: 'Имя' },
  { key: 'gender', label: 'Пол' },
  { key: 'birth', label: 'Дата рождения' },
  { key: 'country', label: 'Страна' },
  { key: 'prizesCount', label: 'Количество премий' },
  { key: 'firstPrize', label: 'Первая премия' }
]

function getName(laureate) {
  if (laureate.knownName && laureate.knownName.en) {
    return laureate.knownName.en
  }
  if (laureate.fullName && laureate.fullName.en) {
    return laureate.fullName.en
  }
  if (laureate.orgName && laureate.orgName.en) {
    return laureate.orgName.en
  }
  if (laureate.givenName && laureate.familyName) {
    return `${laureate.givenName.en || ''} ${laureate.familyName.en || ''}`.trim()
  }
  return 'Неизвестно'
}

function getGender(laureate) {
  if (laureate.gender === 'male') return 'Мужской'
  if (laureate.gender === 'female') return 'Женский'
  return 'Организация'
}

function getBirthDate(laureate) {
  if (laureate.birth && laureate.birth.date) {
    return laureate.birth.date.replace('0000-00-00', 'Неизвестно')
  }
  if (laureate.founded && laureate.founded.date) {
    return laureate.founded.date.replace('0000-00-00', 'Неизвестно')
  }
  return 'Н/Д'
}

function getCountry(laureate) {
  if (laureate.birth && laureate.birth.place) {
    return laureate.birth.place.countryNow?.en ||
      laureate.birth.place.country?.en || 'Н/Д'
  }
  if (laureate.founded && laureate.founded.place) {
    return laureate.founded.place.countryNow?.en ||
      laureate.founded.place.country?.en || 'Н/Д'
  }
  return 'Н/Д'
}

async function loadLaureates() {
  try {
    loading.value = true
    error.value = null

    const offset = (pagination.value.currentPage - 1) * pagination.value.itemsPerPage

    const options = {
      offset,
      limit: pagination.value.itemsPerPage,
      sort: 'asc'
    }

    if (filters.value.name) options.name = filters.value.name
    if (filters.value.gender) options.gender = filters.value.gender
    if (filters.value.category) options.nobelPrizeCategory = filters.value.category

    const response = await NobelService.getLaureates(options)
    console.log('API Response:', response)

    laureatesData.value = response.laureates.map(laureate => {
      console.log('Processing laureate:', laureate)

      return {
        name: getName(laureate),
        gender: getGender(laureate),
        birth: getBirthDate(laureate),
        country: getCountry(laureate),
        prizesCount: laureate.nobelPrizes?.length || 0,
        firstPrize: laureate.nobelPrizes?.[0]?.awardYear || 'Н/Д'
      }
    })

    if (response.meta) {
      pagination.value.totalItems = response.meta.count || 0
      pagination.value.totalPages = Math.ceil(pagination.value.totalItems / pagination.value.itemsPerPage)
    }

  } catch (err) {
    error.value = 'Ошибка при загрузке данных. Пожалуйста, попробуйте позже.'
    console.error('Load error:', err)
  } finally {
    loading.value = false
  }
}

function handlePageChange(newPage) {
  pagination.value.currentPage = newPage
  loadLaureates()
}

function handleFilterChange(filter) {
  if (filter.type === 'name') {
    filters.value.name = filter.value
  } else if (filter.type === 'gender') {
    filters.value.gender = filter.value
  } else if (filter.type === 'category') {
    filters.value.category = filter.value
  }

  pagination.value.currentPage = 1
  loadLaureates()
}

function applyFilters() {
  pagination.value.currentPage = 1
  loadLaureates()
}

function resetFilters() {
  filters.value = { name: '', gender: '', category: '' }
  pagination.value.currentPage = 1
  loadLaureates()
}

onMounted(() => {
  loadLaureates()
})

const genderOptions = [
  { value: '', label: 'Все' },
  { value: 'male', label: 'Мужской' },
  { value: 'female', label: 'Женский' }
]

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
    <ReactiveTable :columns="columns" :data="laureatesData" :pagination="pagination" :loading="loading"
      title="Лауреаты Нобелевских премий" @page-change="handlePageChange" @filter-change="handleFilterChange">
      <template #filters="{ applyFilter }">
        <div class="filters-container">
          <h3>Фильтры лауреатов</h3>
          <div class="filter-group">
            <div class="filter-item">
              <label>Имя:</label>
              <input type="text" v-model="filters.name" placeholder="Поиск по имени..." @input="applyFilters" />
            </div>

            <div class="filter-item">
              <label>Пол:</label>
              <select v-model="filters.gender" @change="applyFilters">
                <option v-for="option in genderOptions" :key="option.value" :value="option.value">
                  {{ option.label }}
                </option>
              </select>
            </div>

            <div class="filter-item">
              <label>Категория премии:</label>
              <select v-model="filters.category" @change="applyFilters">
                <option v-for="option in categoryOptions" :key="option.value" :value="option.value">
                  {{ option.label }}
                </option>
              </select>
            </div>

            <button @click="resetFilters" class="reset-btn">
              Сбросить
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