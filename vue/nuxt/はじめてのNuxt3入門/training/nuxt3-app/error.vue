<template>
  <div v-if="error.statusCode === 404">
    <h1>Error!</h1>
    <p>{{ error.message }}</p>
  </div>
</template>

<script setup>
  const error = useError()
  console.error(error)
</script>