<template>
  <div>
    <div v-if="isLoggedIn" id="upload">
      <p>Click <router-link to="/upload">here</router-link> to upload files.</p>
    </div>
    <p v-else>
      <span><router-link to="/register">Register</router-link></span>
      <span> or </span>
      <span><router-link to="/login">Log In</router-link></span>
    </p>
  </div>
</template>

<script>
import { defineComponent, computed } from 'vue';
import { useStore } from 'vuex';

export default defineComponent({
  name: 'HomeView',
  setup() {
    const store = useStore();

    const isLoggedIn = computed(() => {
      return store.getters.isAuthenticated;
    });

    return {
      isLoggedIn
    };
  }
});
</script>