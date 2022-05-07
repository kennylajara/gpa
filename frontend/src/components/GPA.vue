<template>
    <div class="left-menu">
        <LeftSidebar
            :username="username"
            :menuSelected="menuSelected"
            @select-tab="selectTab"
            @logout="$emit('logout')"
        />
    </div>
    <div class="right-content">
        <AccountsList
            v-if="menuSelected === 'accounts'"
            :accessToken="accessToken"
        />
        <TransactionsList
            v-else-if="menuSelected === 'transactions'"
            :accessToken="accessToken"
        />
    </div>
</template>

<script>
import AccountsList from './AccountsList.vue';
import LeftSidebar from './LeftSidebar.vue';
import TransactionsList from './TransactionsList.vue';

export default {
    name: 'GPA',
    components: {
        AccountsList,
        LeftSidebar,
        TransactionsList,
    },
    data() {
        return {
            menuSelected: 'accounts',
        }
    },
    methods: {
        selectTab(tab) {
            this.menuSelected = tab;
        },
    },
    props: {
        accessToken: {
            type: String,
            default: '',
        },
        refreshToken: {
            type: String,
            default: '',
        },
        username: {
            type: String,
            default: '',
        },
    }
}
</script>

<style>
    .left-menu, .right-content {
        height: 100%;
    }

    .left-menu {
        width: 250px;
        float: left;
        border-right: 1px solid #333;
    }
    .right-content {
        width: calc(100% - 251px);
        float: left;
    }
</style>
