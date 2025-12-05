<script setup>
import ReactiveTable from '../components/ReactiveTable.vue'

const columns = [
  { key: 'category', label: 'Категория' },
  { key: 'awardDate', label: 'Дата вручения' },
  { key: 'grantAmount', label: 'Стоимость гранта' }
]

const prizesData = [
  { category: 'Физика', awardDate: '13.09.2025', grantAmount: '11 млн.' },
  { category: 'Химия', awardDate: '13.09.2024', grantAmount: '11 млн.' },
  { category: 'Медицина', awardDate: '13.09.2023', grantAmount: '10 млн.' },
  { category: 'Литература', awardDate: '13.09.2022', grantAmount: '10 млн.' },
  { category: 'Экономика', awardDate: '13.09.2020', grantAmount: '10 млн.' }
]
</script>

<template>
  <ReactiveTable :columns="columns" :data="prizesData" title="Нобелевские премии" />
</template>