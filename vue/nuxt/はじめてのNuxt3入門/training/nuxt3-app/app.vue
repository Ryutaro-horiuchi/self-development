<template>
  <div>
    <NuxtLayout :name="layout">
      <NuxtPage />
    </NuxtLayout>
  </div>
</template>

<script setup>
const layout = 'custom'
useHead(
  {
    title: "カスタムタイトル"
  }
)
</script>
