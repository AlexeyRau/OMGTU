<script setup>
import { defineProps, defineEmits, computed } from 'vue'

const props = defineProps({
  columns: {
    type: Array,
    required: true
  },
  data: {
    type: Array,
    required: true
  },
  title: {
    type: String,
    default: 'Таблица данных'
  },
  totalItems: {
    type: Number,
    default: 0
  },
  currentPage: {
    type: Number,
    default: 1
  },
  itemsPerPage: {
    type: Number,
    default: 10
  },
  filters: {
    type: Object,
    default: () => ({})
  },
  isLoading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits([
  'page-change',
  'filter-change'
])

const totalPages = computed(() => {
  return Math.ceil(props.totalItems / props.itemsPerPage)
})

function goToPage(page) {
  if (page >= 1 && page <= totalPages.value) {
    emit('page-change', page)
  }
}

function updateFilter(key, value) {
  emit('filter-change', { ...props.filters, [key]: value })
}
</script>

<template>
  <div class="table-page">
    <h2>{{ title }}</h2>

    <!-- Фильтры -->
    <div class="filters" v-if="Object.keys(filters).length > 0">
      <div class="filter-group">
        <label>Поиск:</label>
        <input type="text" :value="filters.search || ''" @input="updateFilter('search', $event.target.value)"
          placeholder="Введите для поиска..." />
      </div>

      <!-- Пример фильтра по году (можно добавить другие) -->
      <div class="filter-group">
        <label>Год:</label>
        <input type="number" :value="filters.year || ''" @input="updateFilter('awardYear', $event.target.value)"
          placeholder="Год" min="1901" :max="new Date().getFullYear()" />
      </div>
    </div>

    <!-- Таблица с загрузкой -->
    <div class="table-container">
      <!-- Индикатор загрузки -->
      <div v-if="isLoading" class="loading">
        Загрузка данных...
      </div>

      <table v-else>
        <thead>
          <tr>
            <th v-for="column in columns" :key="column.key">
              {{ column.label }}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, index) in data" :key="index">
            <td v-for="column in columns" :key="column.key">
              {{ row[column.key] }}
            </td>
          </tr>
          <!-- Если нет данных -->
          <tr v-if="data.length === 0">
            <td :colspan="columns.length" class="no-data">
              Нет данных для отображения
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Пагинация -->
    <div class="pagination" v-if="totalPages > 1">
      <button @click="goToPage(currentPage - 1)" :disabled="currentPage === 1" class="page-btn">
        Назад
      </button>

      <span class="page-info">
        Страница {{ currentPage }} из {{ totalPages }}
      </span>

      <button @click="goToPage(currentPage + 1)" :disabled="currentPage === totalPages" class="page-btn">
        Вперед
      </button>
    </div>

    <!-- Информация о количестве записей -->
    <div class="info" v-if="totalItems > 0">
      Показано {{ data.length }} из {{ totalItems }} записей
    </div>
  </div>
</template>

<style scoped>
.table-page {
  padding: 20px 0;
}

.table-page h2 {
  margin-bottom: 20px;
  color: #2c3e50;
  text-align: center;
}

/* Стили для фильтров */
.filters {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 8px;
  flex-wrap: wrap;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.filter-group label {
  font-weight: bold;
  color: #2c3e50;
  font-size: 14px;
}

.filter-group input {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  min-width: 200px;
}

.filter-group input:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
}

/* Стили для таблицы */
.table-container {
  overflow-x: auto;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  min-height: 200px;
  position: relative;
}

.loading {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 200px;
  color: #7f8c8d;
  font-size: 16px;
}

table {
  width: 100%;
  border-collapse: collapse;
  background-color: white;
  min-width: 600px;
}

th,
td {
  padding: 15px 20px;
  text-align: left;
  border: 1px solid #ddd;
}

th {
  background-color: #34495e;
  color: white;
  font-weight: bold;
  position: sticky;
  top: 0;
}

tbody tr:nth-child(even) {
  background-color: #f8f9fa;
}

tbody tr:nth-child(odd) {
  background-color: #ffffff;
}

tbody tr:hover {
  background-color: #e8f4fc;
}

.no-data {
  text-align: center;
  color: #7f8c8d;
  padding: 40px !important;
  font-style: italic;
}

/* Стили для пагинации */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  margin-top: 20px;
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 8px;
}

.page-btn {
  padding: 8px 16px;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s;
}

.page-btn:hover:not(:disabled) {
  background-color: #2980b9;
}

.page-btn:disabled {
  background-color: #bdc3c7;
  cursor: not-allowed;
}

.page-info {
  font-weight: bold;
  color: #2c3e50;
}

/* Информация о записях */
.info {
  text-align: center;
  margin-top: 10px;
  color: #7f8c8d;
  font-size: 14px;
}

/* Адаптивность */
@media (max-width: 768px) {
  .filters {
    flex-direction: column;
  }

  .filter-group input {
    min-width: 100%;
  }

  .pagination {
    flex-direction: column;
    gap: 10px;
  }

  th,
  td {
    padding: 10px;
    font-size: 14px;
  }
}
</style>