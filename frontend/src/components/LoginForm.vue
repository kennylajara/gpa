<template>
    <div id="login-form">
        <label for="username">Username
            <input type="text" id="username" v-model="usernameMutator" @keydown.enter="$emit('login')" />
        </label>
        <label for="password">Password
            <input type="password" id="password" v-model="passwordMutator" @keydown.enter="$emit('login')" />
        </label>
        <button @click="$emit('login')">Login</button>
    </div>
</template>

<script>
export default {
    name: 'LoginForm',
    props: {
        username: {
            type: String,
            default: '',
        },
        password: {
            type: String,
            default: '',
        },
    },
    computed: {
        usernameMutator: {
            get() {
                return this.username;
            },
            set(value) {
                this.$emit('update-username', value);
            }
        },
        passwordMutator: {
            get() {
                return this.password;
            },
            set(value) {
                this.$emit('update-password', value);
            }
        }
    }
};
</script>

<style scoped>
#login-form {
    border: 1px solid #333;
    padding: 20px;
    border-radius: 5px;
    margin: 0 auto;
    width: 300px;
    text-align: left;
    display: block;
}

#login-form label {
    box-sizing:border-box;
    margin-bottom: 5px;
}

#login-form input {
    width: 100%;
    padding: 0.2em; 
    box-sizing: border-box;
    margin-bottom: 15px;
}

#login-form button {
    margin: 0 auto;
}
</style>
