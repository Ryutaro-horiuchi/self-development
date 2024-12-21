<script setup>
import { ref } from 'vue'

const count = ref(0)
const emit = defineEmits(['increment'])

function handleClick() {
  count.value += 1
  emit('increment', count.value)
}
</script>

<template>
  <button @click="handleClick">Increment</button>
</template>