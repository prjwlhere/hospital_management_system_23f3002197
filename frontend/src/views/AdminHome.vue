<!-- src/views/AdminHome.vue -->
<template>
  <!-- AdminHome is shown inside App.vue's admin layout (router-view). -->
  <div>
    <!-- if you used AdminDashboard to include entire side+content,
         just render it here. Otherwise render a simple placeholder. -->
    <AdminDashboard />
  </div>
</template>

<script>
import AdminDashboard from "@/components/AdminDashboard.vue";

export default {
  name: "AdminHome",
  components: { AdminDashboard },
};
</script>

<style scoped>
/* optional */
</style>
