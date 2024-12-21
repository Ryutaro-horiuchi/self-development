<script setup>
import { ref } from 'vue'

const emit = defineEmits(['submit'])
const email = ref('email')

function handlerSubmit() {
  emit('submit', email.value)
}
</script>

<template>
  <div>
    <input type="email" v-model="email" />

    <button @click="handlerSubmit">Submit</button>
  </div>
</template>