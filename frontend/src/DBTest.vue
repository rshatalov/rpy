<script setup>
import { ref } from 'vue';

const v = ref(0);

function change() {
    console.log('some change');
}

</script>

<template>
    <hr/>
    <div>BD Test</div>
    <div @click="change">change button</div>
    <hr/>
</template>

<style scoped></style>
