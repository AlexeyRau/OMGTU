<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div id="app">
    <header>
      <div class="container">
        <h1>Лауреаты Нобелевских премий</h1>
        <p>Информация о лауреатах и их достижениях</p>
      </div>
    </header>

    <nav>
      <div class="container">
        <ul>
          <li>
            <RouterLink to="/" active-class="active">Премии</RouterLink>
          </li>
          <li>
            <RouterLink to="/laureates" active-class="active">Лауреаты</RouterLink>
          </li>
        </ul>
      </div>
    </nav>

    <main class="container">
      <RouterView />
    </main>

    <footer>
      <div class="container">
        <p>2025 Нобелевские премии. Лабораторная работа №2</p>
      </div>
    </footer>
  </div>
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: Arial, sans-serif;
  line-height: 1.6;
  color: black;
  background-color: white;
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.container {
  width: 90%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

header {
  background-color: #2c3e50;
  color: white;
  padding: 20px 0;
  text-align: center;
}

header h1 {
  margin-bottom: 10px;
  font-size: 2rem;
}

nav {
  background-color: #34495e;
  padding: 15px 0;
}

nav ul {
  list-style: none;
  display: flex;
  justify-content: center;
  gap: 30px;
  margin: 0;
  padding: 0;
}

nav a {
  color: white;
  text-decoration: none;
  padding: 8px 16px;
  border-radius: 4px;
  transition: background-color 0.3s;
}

nav a:hover {
  background-color: #1abc9c;
}

nav a.active {
  background-color: #16a085;
}

main {
  flex: 1;
  padding: 40px 0;
}

footer {
  background-color: #2c3e50;
  color: white;
  text-align: center;
  padding: 20px 0;
  margin-top: auto;
}
</style>