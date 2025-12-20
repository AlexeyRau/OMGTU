<script setup>
import { defineProps, defineEmits } from 'vue'

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
  pagination: {
    type: Object,
    default: () => ({
      currentPage: 1,
      totalPages: 1,
      totalItems: 0,
      itemsPerPage: 20
    })
  },
  loading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['page-change', 'filter-change'])

function changePage(newPage) {
  if (newPage >= 1 && newPage <= props.pagination.totalPages) {
    emit('page-change', newPage)
  }
}

function applyFilter(filterType, value) {
  emit('filter-change', { type: filterType, value })
}
</script>

<template>
  <div class="table-page">
    <h2>{{ title }}</h2>

    <div class="filters" v-if="$slots.filters">
      <slot name="filters" :apply-filter="applyFilter"></slot>
    </div>

    <div v-if="loading" class="loading">
      Загрузка данных...
    </div>

    <div class="table-container" v-else>
      <table>
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
          <tr v-if="data.length === 0">
            <td :colspan="columns.length" class="no-data">
              Нет данных для отображения
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="pagination" v-if="pagination.totalPages > 1 && !loading">
      <button @click="changePage(pagination.currentPage - 1)" :disabled="pagination.currentPage === 1" class="page-btn">
        Назад
      </button>

      <span class="page-info">
        Страница {{ pagination.currentPage }} из {{ pagination.totalPages }}
      </span>

      <button @click="changePage(pagination.currentPage + 1)"
        :disabled="pagination.currentPage === pagination.totalPages" class="page-btn">
        Вперёд
      </button>

      <span class="total-info">
        Всего записей: {{ pagination.totalItems }}
      </span>
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

.filters {
  margin-bottom: 20px;
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #ddd;
}

.loading {
  text-align: center;
  padding: 40px;
  font-size: 18px;
  color: #666;
}

.table-container {
  overflow-x: auto;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
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
  padding: 40px !important;
  color: #666;
  font-style: italic;
}

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
  background-color: #34495e;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.page-btn:hover:not(:disabled) {
  background-color: #1abc9c;
}

.page-btn:disabled {
  background-color: #95a5a6;
  cursor: not-allowed;
}

.page-info {
  font-weight: bold;
  color: #2c3e50;
}

.total-info {
  color: #666;
  font-size: 14px;
}

@media (max-width: 768px) {
  .pagination {
    flex-direction: column;
    gap: 10px;
  }

  th,
  td {
    padding: 12px 15px;
    font-size: 14px;
  }
}
</style>