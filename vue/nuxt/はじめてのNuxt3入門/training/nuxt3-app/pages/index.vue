<template>
  <div>
    <p>{{ counter }}</p>
    <button @click="counterStore.countUp">+</button>
    <button @click="counterStore.countDown">-</button>
    <button @click="counterStore.reset">reset</button>
  </div>
</template>

<script setup>
  const counterStore = useCounterState()
  const { counter } = counterStore
</script>