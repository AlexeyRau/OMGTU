<template>
  <div>
    <DataTable :columns="columns" :data="laureatesData" />
  </div>
</template>

<script>
import DataTable from '../components/DataTable.vue'

export default {
  name: 'Laureates',
  components: {
    DataTable
  },
  data() {
    return {
      columns: [
        { key: 'name', title: 'Имя/Название', sortable: true },
        { key: 'birthDate', title: 'Дата рождения/Основания', sortable: true },
        { key: 'prizesCount', title: 'Число премий', sortable: true }
      ],
      laureatesData: [
        { name: 'Альберт Эйнштейн', birthDate: '14.03.1879', prizesCount: 1 },
        { name: 'Мария Кюри', birthDate: '07.11.1867', prizesCount: 2 },
        { name: 'Лайнус Полинг', birthDate: '28.02.1901', prizesCount: 2 },
        { name: 'Международный комитет Красного Креста', birthDate: '17.02.1863', prizesCount: 3 },
        { name: 'Джон Бардин', birthDate: '23.05.1908', prizesCount: 2 }
      ]
    }
  }
}
</script>