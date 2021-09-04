<template>
  <v-app>
    <v-container>
      <v-row>
        <v-col>
          <RecordWebSpeech />
        </v-col>
      </v-row>
    </v-container>
  </v-app>
</template>

<script>

import RecordWebSpeech from "@/components/recordWebSpeech";
export default {
  name: 'App',

  components: {
    RecordWebSpeech,
  }
};
</script>
