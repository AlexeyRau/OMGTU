<script setup>
import { defineProps } from 'vue'

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
  }
})
</script>

<template>
  <div class="table-page">
    <h2>{{ title }}</h2>
    <div class="table-container">
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
        </tbody>
      </table>
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

.table-container {
  overflow-x: auto;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

table {
  width: 100%;
  border-collapse: collapse;
  background-color: white;
  min-width: 600px;
}

th, td {
  padding: 15px 20px;
  text-align: left;
  border: 1px solid #ddd;
  transition: background-color 0.2s;
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
  cursor: pointer;
}

td {
  color: #333;
}

/* Адаптивность */
@media (max-width: 768px) {
  th, td {
    padding: 12px 15px;
    font-size: 14px;
  }
  
  .container {
    width: 95%;
    padding: 0 10px;
  }
}
</style>