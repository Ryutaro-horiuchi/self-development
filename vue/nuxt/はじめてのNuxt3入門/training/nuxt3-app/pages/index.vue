<template>
  <div>
    <h1>Top Page</h1>
    <hr>
    <p>{{ users[0] }}</p>
  </div>
</template>

<script setup>
  const { data: users } = await useFetch("https://jsonplaceholder.typicode.com/users")
</script>