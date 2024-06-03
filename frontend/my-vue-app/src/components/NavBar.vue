<template>
    <header>
      <nav class="navbar navbar-expand-md navbar-dark bg-dark">
        <div class="container">
          <router-link class="navbar-brand" to="/">Загрузка файлов</router-link>
          <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarCollapse" aria-controls="navbarCollapse" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarCollapse">
            <ul class="navbar-nav me-auto mb-2 mb-md-0">
              <template v-if="isLoggedIn">
                <li class="nav-item">
                  <router-link class="nav-link" to="/">Home</router-link>
                </li>
                <li class="nav-item">
                  <router-link class="nav-link" to="/upload">Upload images</router-link>
                </li>
                <li class="nav-item">
                  <router-link class="nav-link" to="/profile">My Profile</router-link>
                </li>
                <li class="nav-item">
                  <a class="nav-link" @click="logout">Log Out</a>
                </li>
              </template>
              <template v-else>
                <li class="nav-item">
                  <router-link class="nav-link" to="/login">Log In</router-link>
                </li>
              </template>
            </ul>
          </div>
        </div>
      </nav>
    </header>
  </template>
  
  <script>

  import { defineComponent, computed } from 'vue';
  import { useStore } from 'vuex';
  import { useRouter } from 'vue-router';
  
  export default defineComponent({
    name: 'NavBar',
    setup() {
      const store = useStore();
      const router = useRouter();
  
      const isLoggedIn = computed(() => store.getters.isAuthenticated);
  
      const logout = async () => {
        await store.dispatch('logOut');
        router.push('/login');
      };
  
      return {
        isLoggedIn,
        logout
      };
    }
  });


  </script>
  
  <style scoped>
  a {
    cursor: pointer;
  }
  </style>
  