<template>
  <div>
    <DataTable :columns="columns" :data="prizesData" />
  </div>
</template>

<script>
import DataTable from '../components/DataTable.vue'

export default {
  name: 'Prizes',
  components: {
    DataTable
  },
  data() {
    return {
      columns: [
        { key: 'category', title: 'Категория', sortable: true },
        { key: 'awardDate', title: 'Дата вручения', sortable: true },
        { key: 'grantAmount', title: 'Стоимость гранта', sortable: true }
      ],
      prizesData: [
        { category: 'Физика', awardDate: '13.09.2025', grantAmount: '11 млн.' },
        { category: 'Химия', awardDate: '14.09.2025', grantAmount: '11 млн.' },
        { category: 'Медицина', awardDate: '15.09.2025', grantAmount: '11 млн.' },
        { category: 'Литература', awardDate: '16.09.2025', grantAmount: '11 млн.' },
        { category: 'Мир', awardDate: '17.09.2025', grantAmount: '11 млн.' }
      ]
    }
  }
}
</script>