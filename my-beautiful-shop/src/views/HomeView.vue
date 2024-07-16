<template>
  <div id="app">
    <div class="video-background">
      <video autoplay loop muted playsinline class="fullscreen-video">
        <source src="@/assets/liquid.mp4" type="video/mp4">
      </video>
    </div>

    <nav class="navbar">
    </nav>

    <router-view />
  </div>
</template>

<style scoped>
.video-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%; 
  overflow: hidden;
  z-index: -1; 
}

.fullscreen-video {
  width: 100%;
  height: auto; 
  object-fit: cover; 
}

#app {
  position: relative;
}
</style>