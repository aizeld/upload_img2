<template>
    <section>
      <div v-if="user">
        <p><strong>Email:</strong> <span>{{ user.email }}</span></p>
        <p><strong>Is Staff:</strong> <span>{{ user.is_staff }}</span></p>
        <p><strong>Username:</strong> <span>{{ user.name }}</span></p>
      </div>
      <div v-else>
        <p>Loading...</p>
      </div>
    </section>
  </template>
  
  <script>
  import { defineComponent, computed, onMounted } from 'vue';
  import { useStore } from 'vuex';
  
  export default defineComponent({
    name: 'ProfileView',
    setup() {
      const store = useStore();
  
      // Fetch user data when the component is mounted
      onMounted(() => {
        store.dispatch('viewMe');
      });
  
      // Computed property to get user from Vuex store
      const user = computed(() => store.getters.stateUser);
  
      return {
        user
      };
    }
  });
  </script>