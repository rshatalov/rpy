<script setup>
import { ref } from 'vue';

const timer = ref(0);

function increment() {
    if (timer.value < 10) {
        timer.value++;
    }
}

</script>

<template>
    <div @click="increment">Increase</div>
    <div>{{ timer }}</div>
    <div @click="timer--">Decrease</div>

</template>

<style scoped></style>
