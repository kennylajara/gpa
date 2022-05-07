<template>
    <table>
        <thead>
            <tr>
                <th>ID</th>
                <th>Date</th>
                <th>Transaction Type</th>
                <th>Account Number</th>
                <th>Note</th>
                <th>Amount</th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="transaction in transactions" :key="transaction.ID">
                <td>{{ transaction.ID }}</td>
                <td>{{ transaction.date }}</td>
                <td>{{ transaction.transaction_type }}</td>
                <td>{{ this.getAccountNumber(transaction.account_id) }}</td>
                <td>{{ transaction.note }}</td>
                <td>{{ transaction.transaction_type == 'credit'? '+': '-' }}{{ transaction.amount }}</td>
            </tr>
        </tbody>
    </table>
</template>

<script>
export default {
    name: 'TransactionsList',
    props: {
        accessToken: {
            type: String,
            default: '',
        },
    },
    data() {
        return {
            transactions: [],
            accounts: [],
        }
    },
    methods: {
        fetchTransactions() {
            const url = `http://localhost:8000/transaction/`;
            fetch(url, {
                method: 'GET',
                headers: {
                    'Authorization': 'Bearer ' + this.accessToken,
                },
            })
            .then(response => response.json())
            .then(result => this.transactions = result);
        },
        fetchAccounts() {
            const url = `http://localhost:8000/account/`;
            fetch(url, {
                method: 'GET',
                headers: {
                    'Authorization': 'Bearer ' + this.accessToken,
                },
            })
            .then(response => response.json())
            .then(result => this.accounts = result);
        },
        getAccountNumber(transactionId) {
            const account = this.accounts.find(account => account.ID === transactionId);
            let acount_number = account.account_number;
            return '***' + acount_number.substr(acount_number.length - 4);
        },
    },
    created() {
        this.fetchTransactions();
        this.fetchAccounts();
    },
};
</script>

<style>
table {
    width: calc(100% - 60px);
    margin-top: 60px;
    text-align: center;
    margin-left: 30px;
    margin-right: 30px;
    border-collapse: collapse;
}

th {
    background-color: #ccc;
}

tr, td, th {
    border: solid;
    border-width: 1px;
    border-color: #aaa;
}
</style>
