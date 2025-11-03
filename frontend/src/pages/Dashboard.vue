<template>
    <div>
        <h1>Dashboard</h1>
        <div>
            Description of the app
            <br/>
            {{ count }}
            <br/>
            {{ message }}
            <br/>
            <div @click="call">click here</div>
        </div>
    </div>
    <TestItemForm />
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import TestItemForm from '@/components/TestItemForm.vue';
import ActForm from '@/components/ActForm.vue';

const count = ref(0);
var message = ref('no message');

function call() {
    axios.get('http://localhost:8000/')
    .then(response => {
        console.log(response.data);
        message.value = response.data.message;
    })
    .catch(error => {
        console.log('Error fetching data: ', error);
        message.value = error;
    })
}
</script>