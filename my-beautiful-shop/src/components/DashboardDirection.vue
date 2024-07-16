<!-- src/components/DashboardDirection.vue -->
<template>
  <div class="app">

  </div>


</template>

<script>
export default {
  data() {

  },



};
</script>
<style>
html, body, #app {
  margin: 0;
  padding: 0;
  width: 100%;
  max-width: 100%;
}

.app {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  height: 100vh;
  margin-top: 0;
  background-image: url('../assets/BeautyShop.png');
  background-size: cover;
  background-attachment: fixed;
  background-position: center;
  overflow-x: hidden;
}
.loading-spinner {
flex-direction: column;
justify-content: center;
align-items: center;
height: 200px;
}

.loader {
border: 4px solid rgba(255, 0, 0, 0.3);
border-radius: 50%;
border-top: 4px solid #fefefe;
width: 50px;
height: 50px;
left:50%;
right:50%;
animation: spin 1s linear infinite;
margin-top: 100px;
justify-content: center;
position: absolute;
margin-left:25px;
}



</style>