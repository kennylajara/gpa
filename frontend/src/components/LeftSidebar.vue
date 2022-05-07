<template>
    <div>
        <h1>Hi, {{ username }}</h1>
        <hr>
        <div>
            <button
                @click="$emit('select-tab', 'accounts')"
                :class="{'active': menuSelected === 'accounts'}"
            >Accounts</button>
        </div>
        <div>
            <button
                @click="$emit('select-tab', 'transactions')"
                :class="{'active': menuSelected === 'transactions'}"
            >Transactions</button>
        </div>
        <a href="#" @click="$emit('logout')">Logout</a>
    </div>
</template>

<script>
export default {
    name: 'LeftSidebar',
    props: {
        menuSelected: {
            type: String,
            default: 'accounts',
        },
        username: {
            type: String,
            default: '',
        },
    },
}
</script>

<style scoped>
    div {
        text-align: center;
    }
    button {
        width: 200px;
        background-color: #ccc;
        border: none;
        margin-top: 10px;
        padding: 10px;
        cursor: pointer;
    }
    button.active {
        background-color: rgb(42, 31, 199);
        color: #fff;
    }
    h1 {
        font-size: 1.5em;
    }
</style>
