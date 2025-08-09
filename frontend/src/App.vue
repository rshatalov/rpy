
<script setup>
import { ref } from 'vue';
import axios from 'axios';

const count = ref(0);
var message = ref("no message")

function call() {
    axios.get('http://localhost:8001/')
      .then(response => {
        console.log(response.data);
        message.value = response.data.message;
      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });
}

</script>

<template>
  <h1>RPY app</h1>
  <div>
    description of the app
    <br/>
    {{ count }}
    <br/>
    {{  message }}
    <br/>
    <div @click="call">click</div>
  </div>
</template>

<style scoped></style>
