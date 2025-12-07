<template>
  <div>
    <h1>Top Page</h1>
    <hr>
    <p>{{ users[0] }}</p>
  </div>
</template>

<script setup>
  const { data: users, error } = await useFetch("https://jsonplaceholder.typicode.com/userss")
  if (error.value) {
    throw createError({ statusCode: 404, statusMessage: "Page not found!!" } )
  }
</script>