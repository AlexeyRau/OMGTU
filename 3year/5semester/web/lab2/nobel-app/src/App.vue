<template>
  <div id="app">
    <header>
      <div class="container">
        <h1>{{ headerTitle }}</h1>
        <p>{{ headerSubtitle }}</p>
      </div>
    </header>

    <nav>
      <div class="container">
        <ul>
          <li>
            <router-link 
              to="/prizes" 
              :class="{ active: $route.path === '/prizes' }"
            >
              Премии
            </router-link>
          </li>
          <li>
            <router-link 
              to="/laureates" 
              :class="{ active: $route.path === '/laureates' }"
            >
              Лауреаты
            </router-link>
          </li>
        </ul>
      </div>
    </nav>

    <main class="container">
      <router-view></router-view>
    </main>

    <footer>
      <div class="container">
        <p>2025 Нобелевские премии. Лабораторная работа №2 - Реактивность</p>
      </div>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'App',
  computed: {
    headerTitle() {
      return this.$route.path === '/prizes' 
        ? 'Нобелевские премии' 
        : 'Лауреаты Нобелевских премий'
    },
    headerSubtitle() {
      return this.$route.path === '/prizes'
        ? 'Информация о категориях и наградах'
        : 'Информация о лауреатах и их достижениях'
    }
  }
}
</script>

<style>
* {
    margin: 0;
    padding: 0;
}

body {
    font-family: Arial;
    line-height: 1.6;
    color: black;
    background-color: white;
}

.container {
    width: 90%;
    margin: 0 auto;
    padding: 20px;
}

header {
    background-color: #2c3e50;
    color: white;
    padding: 16px 0;
    text-align: center;
}

header h1 {
    margin-bottom: 8px;
}

nav {
    background-color: #34495e;
    padding: 16px 0;
}

nav ul {
    list-style: none;
    display: flex;
    justify-content: center;
    gap: 32px;
}

nav a {
    color: white;
    text-decoration: none;
    padding: 8px 16px;
    border-radius: 4px;
}

nav a:hover {
    background-color: #1abc9c;
}

nav a.router-link-active,
nav a.active {
    background-color: #16a085;
}

main {
    padding: 32px 0;
    min-height: 60vh;
}

footer {
    background-color: #2c3e50;
    color: white;
    text-align: center;
    padding: 1rem 0;
    margin-top: 2rem;
}
</style>