<template>
  <v-container>
    <v-row align="center">
      <v-col>
        <canvas id="before_image" width="400" height="400" style="background-color: gray;" />
      </v-col>
      <v-col>
        <canvas id="after_image" width="400" height="400" style="background-color: gray;" />
      </v-col>
      <v-col style="text-align: center;">
        <v-btn
          @click="onClickLoadButton">
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
      @change="onChangeFile"
    >
  </v-container>
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator';

@Component({})
export default class MainFrame extends Vue {

  private onClickLoadButton() {
    const { input }: any = this.$refs;
    input.click();
  }

  private async onChangeFile(event: any) {
    let files = event.target.files || event.dataTransfer.files;
    let file = files[0];
    if (!file) {
      return;
    }

    // 同じファイルを選んでもイベントが発火するように
    event.target.value = '';

    this.drowImageBefore(file, 'before_image');

    let formData = new FormData();
    formData.append('file', file);
    formData.append('style', 'Hayao');

    let res;
    try {
      res = await Vue.$fetch.post_original('api/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
    } catch (error) {
      console.error(error);
      return;
    }

    this.drowImage(res.data, 'after_image');
  }

  private drowImageBefore(file: any, canvasId: string) {
    const reader = new FileReader();
    let self = this;
    reader.onload = function(e) {
      self.drowImage(e.target!.result, canvasId);
    }
    reader.readAsDataURL(file);
  }

  private drowImage(file: any, canvasId: string) {
    let canvas = <HTMLCanvasElement> document.getElementById(canvasId);
    let ctx = canvas.getContext('2d');
    // canvas上に画像を重ねて表示
    let img = new Image();
    img.src = file as string;
    img.onload = function() {
      ctx!.drawImage(img, 0, 0, 400, 400);
    }
  }
}
</script>

<style scoped>

</style>
