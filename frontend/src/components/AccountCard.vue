<template>
    <div class="account-card">
        <h2>Account Number</h2>
        <p>{{ account.account_number }}</p>
        <div class="account-card-balance">
            <h3 class="left">Current Balance</h3>
            <p class="right">${{ account.current_balance }}</p>
        </div>
        <div class="clear"></div>
        <a class="right" href="#" @click="$emit('see-transactions', account.ID)">View Transactions</a>
        <div class="clear"></div>
    </div>
</template>

<script>
export default {
    name: 'AccountCard',
    props: {
        account: {},
    },
}
</script>

<style scoped>
.account-card {
    width: clacl(100% - 20px);
    padding: 10px;
    margin-right: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
    margin-bottom: 10px;
}

h2 {
    margin-top: 0;
}

.right {
    float: right;
}

.left {
    float: left;
}
.clear {
    clear: both;
}
</style>
