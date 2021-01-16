<template>
  <v-container>
    <v-row align="center">
      <v-col>
        <canvas id="before_image" width="400" height="400" style="background-color: gray;" />
      </v-col>
      <v-col>
        <canvas width="400" height="400" style="background-color: gray;" />
      </v-col>
      <v-col style="text-align: center;">
        <v-btn
          @click="pushLoadButton()">
          ファイル選択
        </v-btn>
      </v-col>
    </v-row>
    <!-- 非表示のinputタグを格納 -->
    <input
      style="display: none"
      ref="input"
      type="file"
      accept="image/jpeg, image/jpg, image/png"
      @change="selectedFile()"
    >
  </v-container>
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator';

@Component({})
export default class MainFrame extends Vue {

  private pushLoadButton() {
    const { input }: any = this.$refs;
    input.click();
  }

  private async selectedFile() {
    const { input }: any = this.$refs;
    const file = input.files[0];
    if (!file) {
      return;
    }
    // 以下ファイルの操作
    let canvas = <HTMLCanvasElement> document.getElementById('before_image');
    let ctx = canvas.getContext('2d');
    const reader = new FileReader();
    reader.onload = function(e) {
      // canvas上に画像を重ねて表示
      let img = new Image();
      img.src = e.target!.result as string;
      img.onload = function() {
        ctx!.drawImage(img, 0, 0, 400, 400);
      }
    }
    reader.readAsDataURL(file);

    // TODO API連携
  }
}
</script>

<style scoped>

</style>
