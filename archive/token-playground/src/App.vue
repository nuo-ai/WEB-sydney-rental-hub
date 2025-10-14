<template>
  <div id="app-layout">
    <header>
      <h1>Sydney Rental Hub - Token Playground</h1>
      <p>在这里实时测试和可视化我们的设计令牌。</p>
    </header>
    <main>
      <div class="controls-panel">
        <h2>令牌控制器</h2>
        <TokenControls />
      </div>
      <div class="preview-panel">
        <h2>组件预览</h2>
        <section>
          <h3>Property Card</h3>
          <!-- PropertyCardDemo component will go here -->
        </section>
        <section>
          <h3>Buttons</h3>
          <!-- ButtonStatesDemo component will go here -->
        </section>
      </div>
    </main>
  </div>
</template>

<script setup>
import TokenControls from './components/TokenControls.vue';
</script>

<style>
#app-layout {
  display: flex;
  flex-direction: column;
  height: 100vh;
  font-family: sans-serif;
}
header {
  padding: 1rem 2rem;
  border-bottom: 1px solid #eee;
}
main {
  display: flex;
  flex-grow: 1;
  overflow: hidden;
}
.controls-panel {
  width: 300px;
  padding: 1rem;
  border-right: 1px solid #eee;
  overflow-y: auto;
}
.preview-panel {
  flex-grow: 1;
  padding: 2rem;
  overflow-y: auto;
  background-color: #f9f9f9;
}
section {
  margin-bottom: 2rem;
  background: white;
  padding: 1rem;
  border-radius: 8px;
}
</style>
