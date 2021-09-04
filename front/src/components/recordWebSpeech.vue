<template>
  <v-card>
    <v-container>
      <v-row>
        <v-col>
          <v-card-title>ぼくのすいかわり</v-card-title>
        </v-col>
      </v-row>

      <v-row>
        <v-col class="text-center">
          <v-btn icon @click="routeClick">
            <v-icon>{{isRecording ? "mdi-microphone" : "mdi-microphone-outline"}}</v-icon>
          </v-btn>
        </v-col>
      </v-row>

      <v-row>
        <v-col>
          {{currText}}
        </v-col>
      </v-row>


    </v-container>
  </v-card>
</template>

<script>

import {bocabRegex} from "@/components/consts";

export default {
  name: "RecordWebSpeech",
  data(){
    return {
      // eslint-disable-next-line no-undef
      recog: new webkitSpeechRecognition(),
      currText: "",
      isRecording: false,
      availableWords: [],
    };
  },
  mounted() {
    this.recog.lang = "ja-JP"
    this.recog.interimResults = false;
    this.recog.continuous = false;
    this.recog.onresult = (event) => {
      for (let i = event.resultIndex; i < event.results.length; i++) {
        if (!event.results[i].isFinal)
          continue;

        const recogText = event.results[i][0].transcript;
        this.textCallback(recogText);
      }
    };

  },
  methods: {
    routeClick(){
      if(!this.isRecording){
        this.recordStart();
      }else{
        this.recordEnd();
      }
    },
    recordStart(){
      this.recog.start();
      this.isRecording = true;
    },
    recordEnd(){
      this.recog.stop();
      this.isRecording = false;
    },
    textCallback(text){
      this.currText += text;
      this.availableWords = this.currText.match(bocabRegex);
    }
  }
}
</script>

<style scoped>

</style>