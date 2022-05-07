<template>
    <div class="accounts-list">
        <div
            v-for="account in accounts"
            :key="account.ID"
            class="account"
        >
            <accountCard
                :account="account"
            />
        </div>
    </div>
</template>

<script>
import AccountCard from './AccountCard.vue';

export default {
    name: 'AccountsList',
    components: {
        AccountCard,
    },
    props: {
        accessToken: {
            type: String,
            default: '',
        },
    },
    data() {
        return {
            accounts: [],
        }
    },
    methods: {
        fetchAccounts() {
            fetch('http://localhost:8000/account/', {
                method: 'GET',
                headers: {
                    'Authorization': 'Bearer ' + this.accessToken,
                },
            })
            .then(response => response.json())
            .then(result => this.accounts = result);
        },
    },
    created() {
        this.fetchAccounts();
    },
}
</script>

<style scoped>
.accounts-list {
    padding-top: 50px;
}

.account {
    margin-bottom: 5px;
    width: 33.33%;
    float: left;
    padding: 10px;
}
</style>
