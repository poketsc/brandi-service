const serviceStore = {
  namespaced: true,
  state: {
    accessToken: localStorage.getItem('service_token')
  },
  getters: {
    getToken(state) {
      return state.accessToken
    }
  },
  mutations: {
    getStorageToken(state) {
      state.accessToken = localStorage.getItem('service_token')
    }
  }
}

export default serviceStore
