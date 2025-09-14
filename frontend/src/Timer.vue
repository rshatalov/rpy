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
    <hr/>
    <div>Timer</div>
    <div @click="increment">Increase button</div>
    <div>{{ timer }}</div>
    <div @click="timer--">Decrease button</div>
    <hr/>
</template>

<style scoped></style>
