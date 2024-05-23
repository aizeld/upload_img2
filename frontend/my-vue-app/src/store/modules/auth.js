
import axios from 'axios';
import VueCookies from 'vue-cookies';
const api = axios.create({
  baseURL: 'http://localhost:8000',
  withCredentials: true
});

const state = {
 user : !!VueCookies.get('token'),
};

const getters = {
  isAuthenticated: state => !!state.user,
  stateUser: state => state.user
};
const actions = {
  // Логин
  async login({ dispatch }, credentials) {
    try {
      await api.post('/login', credentials);
      await dispatch('viewMe');
    } catch (error) {
      console.error('Error during login:', error);
      throw error;
    }
  },

  // Получение информации о текущем пользователе
  async viewMe({ commit }) {
    try {
      const { data } = await api.get('/users/whoami');
      commit('setUser', data);
    } catch (error) {
      console.error('Error fetching user info:', error);
      throw error;
    }
  },

  // Логаут 
  async logOut({ commit }) {
    try {
      await api.post('/logout');
      commit('logout');
    } catch (error) {
      console.error('Error during logout:', error);
    }
  },
};

const mutations = {
  setUser(state, username) {
    state.user = username;
  },
  logout(state, user){
    state.user = user;
  },
};



export default {
  state,
  getters,
  actions,
  mutations
};