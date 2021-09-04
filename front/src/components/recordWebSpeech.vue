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
          {{displayTexts}}
        </v-col>
      </v-row>


    </v-container>
  </v-card>
</template>

<script>

import {
  apiPrefix,
  bocabRegex
} from "@/components/consts";
import axios from "axios";

export default {
  name: "RecordWebSpeech",
  data(){
    return {
      // eslint-disable-next-line no-undef
      recog: new webkitSpeechRecognition(),
      isRecording: false,
      availableWords: [],
      displayTexts: "",
      isEnding : false
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

    this.recog.onstart = () => {this.isRecording = true;};
    this.recog.onend = () => {this.isRecording = false;};
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
    },
    recordEnd(){
      if(this.isEnding)
        return;
      this.isEnding = true;
      setTimeout(()=> {
        this.recog.stop();
        this.isEnding = false;
        }, 500);
    },
    textCallback(text){
      this.availableWords = text.match(bocabRegex);
      this.displayTexts  = "";
      for(const i in this.availableWords){
        this.displayTexts += this.availableWords[i];
      }
      axios.post(apiPrefix + "/record", {data: this.availableWords});
    }
  }
}
</script>

<style scoped>

</style>