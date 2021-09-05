<template>
  <v-card>
    <v-container>
      <v-row>
        <v-col>
          <v-img :src="logo" />
        </v-col>
      </v-row>
      <v-divider />
      <v-row>
        <v-col cols="6">
          <v-img :src="howTo1" />
        </v-col>
        <v-col cols="6">
          <v-img :src="howTo2" />
        </v-col>
      </v-row>

      <v-row>
        <v-col class="text-center">
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

const isProduct = true;

const bocabRegex = /右|左|前|まえ|みぎ|ひだり|ふれ|ちょっと|すごく|少し|すこし|かなり|そこそこ/g;
const bocabComment = /右|左|前|まえ|みぎ|ひだり|ふれ|いいね|いいよ|いけ|違う|ちがう|だめ|ダメ/g

const apiPrefix = (isProduct) ? "http://163.43.106.67:8000" : "http://localhost:8000"
const commentApiPrefix = (isProduct) ? "http://163.43.106.67:4000" : "http://localhost:4000"

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
    },
    howTo1(){
      return require("@/assets/img/HowTo_1.png");
    },
    howTo2(){
      return require("@/assets/img/HowTo_2.png");
    },
    logo(){
      return require("@/assets/img/Logo.png");
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
      console.log(this.availableWords);
      axios.post(apiPrefix + "/records", {words: this.availableWords});
      const comments = text.match(bocabComment);
      axios.post(commentApiPrefix + "/addWord", {words: comments});
    }
  }
}
</script>

<style scoped>

</style>
