<template>
  <div class="table-container">
    <table>
      <thead>
        <tr>
          <th 
            v-for="column in columns" 
            :key="column.key"
            @click="sortTable(column.key)"
            :class="{ sortable: column.sortable }"
          >
            {{ column.title }}
            <span v-if="sortColumn === column.key" class="sort-indicator">
              {{ sortDirection === 'asc' ? '↑' : '↓' }}
            </span>
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(row, index) in sortedData" :key="index">
          <td v-for="column in columns" :key="column.key">
            {{ row[column.key] }}
          </td>
        </tr>
      </tbody>
    </table>
    
    <div v-if="data.length === 0" class="no-data">
      Нет данных для отображения
    </div>
  </div>
</template>

<script>
export default {
  name: 'DataTable',
  props: {
    columns: {
      type: Array,
      required: true
    },
    data: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      sortColumn: '',
      sortDirection: 'asc'
    }
  },
  computed: {
    sortedData() {
      if (!this.sortColumn) return this.data
      
      return [...this.data].sort((a, b) => {
        let aValue = a[this.sortColumn]
        let bValue = b[this.sortColumn]
        
        if (typeof aValue === 'string') {
          aValue = aValue.toLowerCase()
          bValue = bValue.toLowerCase()
        }
        
        if (aValue < bValue) return this.sortDirection === 'asc' ? -1 : 1
        if (aValue > bValue) return this.sortDirection === 'asc' ? 1 : -1
        return 0
      })
    }
  },
  methods: {
    sortTable(columnKey) {
      const column = this.columns.find(col => col.key === columnKey)
      if (!column || !column.sortable) return
      
      if (this.sortColumn === columnKey) {
        this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc'
      } else {
        this.sortColumn = columnKey
        this.sortDirection = 'asc'
      }
    }
  }
}
</script>

<style scoped>
.table-container {
  margin: 32px 0;
}

table {
  width: 100%;
  border-collapse: collapse;
  background-color: white;
}

th, td {
  padding: 12px 15px;
  text-align: left;
  border: 1px solid #ddd;
}

th {
  background-color: #34495e;
  color: white;
  font-weight: bold;
}

th.sortable {
  cursor: pointer;
  transition: background-color 0.3s;
}

th.sortable:hover {
  background-color: #2c3e50;
}

.sort-indicator {
  margin-left: 5px;
}

tbody tr:nth-child(even) {
  background-color: #f8f9fa;
}

tbody tr:nth-child(odd) {
  background-color: #ffffff;
}

tbody tr:hover {
  background-color: #e8f4fc;
  transition: background-color 0.2s;
}

.no-data {
  text-align: center;
  padding: 20px;
  color: #666;
  font-style: italic;
}
</style>