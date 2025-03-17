<template>
  <div id="app">
    <NavBar />
    <div class="main container">
      <router-view/>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import NavBar from '@/components/NavBar.vue'
export default {
  components: {
    NavBar
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}
.main {
  padding-top: 5em;
}
</style>
<style>
body {
  background: linear-gradient(180deg, #61d591, #913ee4);
  font-family: 'Roboto', sans-serif;
  margin: 0;
  padding: 0;
  height: 100%;
  min-height: 100vh;  /* 确保页面高度至少填满视口 */
  background-size: cover;  /* 确保背景填满整个页面 */
  background-attachment: fixed; /* 背景固定，滚动时背景不会跟随 */
}

</style>
