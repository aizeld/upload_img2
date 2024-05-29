<template>
    <section>
      <form @submit.prevent="submit">
        <div class="mb-3">
          <label for="username" class="form-label">Username:</label>
          <input type="text" name="username" v-model.trim="form.username" class="form-control" />
        </div>
        <div class="mb-3">
          <label for="password" class="form-label">Password:</label>
          <input type="password" name="password" v-model.trim="form.password" class="form-control" />
        </div>
        <div class="mb-3 form-check">
          <input type="checkbox" name="remember" v-model="form.remember" class="form-check-input" id="rememberMe" />
          <label for="rememberMe" class="form-check-label">Remember Me</label>
        </div>
        <button :disabled="isSubmitting" type="submit" class="btn btn-primary">
          <span v-if="isSubmitting" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
          <span v-else>Submit</span>
        </button>
        <p v-if="errorMessage" class="text-danger">{{ errorMessage }}</p>
      </form>
    </section>
  </template>
  
  <script>
  import { defineComponent, ref } from 'vue';
  import { useRouter } from 'vue-router';
  import { useStore } from 'vuex';
  
  export default defineComponent({
    name: 'LoginView',
    setup() {
      const store = useStore();
      const router = useRouter();
      const form = ref({
        username: '',
        password: '',
        remember : false
      });
      const errorMessage = ref('');
      const isSubmitting = ref(false);
      
      const submit = async () => {
        isSubmitting.value = true;
        try {
          await store.dispatch('login', { username: form.value.username, password: form.value.password, remember: form.value.remember
 });
          router.push('/upload');
        } catch (error) {
          console.error('Login failed:', error);
          errorMessage.value = error.response?.data?.message || 'An error occurred during login';
        } finally {
          isSubmitting.value = false;
        }
      };
  
      return {
        form,
        errorMessage,
        isSubmitting,
        submit
      };
    }
  });
  </script>
  
  <style scoped>
  /* Add your styles here */
  </style>
  