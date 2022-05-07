<template>
  <div id="login-container" v-if="!isLogged" >
    <LoginForm
      :username="username"
      :password="password"
      @update-username="updateUsername"
      @update-password="updatePassword"
      @login="login"
      @logout="logout"
    />
  </div>
  <div id="gpa-container" v-else>
    <GPA
      :username="username"
      :accessToken="accessToken"
      @logout="logout"
    />
  </div>
</template>

<script>
import GPA from './components/GPA.vue';
import LoginForm from './components/LoginForm.vue'

export default {
  name: 'App',
  components: {
    GPA,
    LoginForm,
  },
  data() {
    return {
      isLogged: false,
      refreshToken: null,
      accessToken: null,
      username: '',
      password: '',
    }
  },
  methods: {
    login() {
      let myHeaders = new Headers();
      myHeaders.append("Content-Type", "application/json");

      const raw = JSON.stringify({
        "username": this.username,
        "password": this.password,
      });

      var requestOptions = {
        method: 'POST',
        headers: myHeaders,
        body: raw,
        redirect: 'follow'
      };

      fetch("http://localhost:8000/api/token/", requestOptions)
        .then(response => response.json())
        .then(result => this.handleLoginResponse(result));

      this.password = '';
    },
    handleLoginResponse(result) {
      if (result.access) {
        this.isLogged = true;
        this.refreshToken = result.refresh;
        this.accessToken = result.access;
        // Refresh token every 2 minutes
        setInterval(() => {
          if (this.refreshToken != null) {
            this.refreshAccessToken();
          }
        }, 120000);
      } else {
        this.isLogged = false;
        alert("Login failed");
      }
    },
    updateUsername(value) {
      this.username = value;
    },
    updatePassword(value) {
      this.password = value;
    },
    refreshAccessToken() {
      let myHeaders = new Headers();
      myHeaders.append("Content-Type", "application/json");

      const raw = JSON.stringify({
        "refresh": this.refreshToken,
      });

      var requestOptions = {
        method: 'POST',
        headers: myHeaders,
        body: raw,
        redirect: 'follow'
      };

      fetch("http://localhost:8000/api/token/refresh/", requestOptions)
        .then(response => response.json())
        .then(result => this.handleRefreshResponse(result));
    },
    handleRefreshResponse(result) {
      if (result.access) {
        this.accessToken = result.access;
      } else {
        alert("Failed to refresh token. Please login again.");
        this.isLogged = false;
      }
    },
    logout() {
      this.isLogged = false;
      this.accessToken = null;
      this.refreshToken = null;
    },
  }
}
</script>

<style>
  html, body, #app, #gpa-container {
    height: 100%;
    margin: 0;
    padding: 0;
  }

  #login-container {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin-top: 60px;
  }
</style>
