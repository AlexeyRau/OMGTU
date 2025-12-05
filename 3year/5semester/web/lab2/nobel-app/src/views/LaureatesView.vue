<script setup>
import ReactiveTable from '../components/ReactiveTable.vue'

const columns = [
  { key: 'name', label: 'Имя' },
  { key: 'birthDate', label: 'Дата рождения' },
  { key: 'prizesCount', label: 'Число премий' }
]

const laureatesData = [
  { name: 'Альберт Эйнштейн', birthDate: '14.03.1879', prizesCount: 1 },
  { name: 'Мария Кюри', birthDate: '07.11.1867', prizesCount: 2 },
  { name: 'Лайнус Полинг', birthDate: '28.02.1901', prizesCount: 2 },
  { name: 'Нильс Бор', birthDate: '07.10.1885', prizesCount: 1 },
  { name: 'Эрнест Хемингуэй', birthDate: '21.07.1899', prizesCount: 1 }
]
</script>

<template>
  <ReactiveTable 
    :columns="columns" 
    :data="laureatesData" 
    title="Лауреаты Нобелевских премий"
  />
</template>