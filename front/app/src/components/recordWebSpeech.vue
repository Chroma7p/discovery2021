<template>
  <v-card>
    <v-container>
      <v-row>
        <v-col>
          <v-card-title>Suicovery</v-card-title>
        </v-col>
      </v-row>

      <v-row>
        <v-col>
          {{getTime}}
        </v-col>
      </v-row>

      <v-row>
        <v-col class="text-center">
          <v-btn icon elevation="3" @click="recordStart">
            <v-icon large>{{isRecording ? "mdi-microphone" : "mdi-microphone-outline"}}</v-icon>
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
import axios from "axios";

const bocabRegex = /右|左|前|まえ|みぎ|ひだり|ふれ|ちょっと|すごく/g;

const apiPrefix = "http://localhost:8000"

export default {
  name: "RecordWebSpeech",
  data(){
    return {
      // eslint-disable-next-line no-undef
      recog: new webkitSpeechRecognition(),
      isRecording: false,
      availableWords: [],
      displayTexts: "",
      timeCount: 0
    };
  },
  computed: {
    getTime(){
      return (this.timeCount <= 0) ? "Press microphone!": this.timeCount.toFixed(1);
    }
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
    recordStart(){
      if(this.isRecording)
        return;

      this.recog.start();
      this.timeCount = 3.0;

      const timer = setInterval(() => {
        this.timeCount -= 0.1;
        if(this.timeCount <= 0){
          this.recordEnd();
          clearInterval(timer);
        }
      }, 100);
    },
    recordEnd(){
      this.recog.stop();
    },
    textCallback(text){
      this.availableWords = text.match(bocabRegex);
      this.displayTexts  = "";
      for(const i in this.availableWords){
        this.displayTexts += this.availableWords[i];
      }
      axios.post(apiPrefix + "/records", {words: this.availableWords});
    }
  }
}
</script>

<style scoped>

</style>