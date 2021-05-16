<template>
  <v-container>
    <v-row align="center" justify="center">
      <v-col cols="auto">
        <canvas id="before_image" width="400" height="400" style="background-color: gray;" />
      </v-col>
      <v-col cols="auto">
        <v-btn
          @click="onClickLoadButton">
          ファイル選択
        </v-btn>
      </v-col>
    </v-row>
    <v-row align="center" justify="center">
      <v-col cols="auto">
        <v-tabs centered>
          <v-tab @click="onClickTab">Hayao</v-tab>
          <v-tab @click="onClickTab">Shinkai</v-tab>
          <v-tab @click="onClickTab">Hosoda</v-tab>
        </v-tabs>
        <canvas id="after_image" width="400" height="400" style="background-color: gray;" />
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
  private static readonly BEFORE_IMAGE_CANVAS_ID = 'before_image'
  private static readonly AFTER_IMAGE_CANVAS_ID = 'after_image'

  private file: File | undefined

  private onClickLoadButton() {
    const { input }: any = this.$refs;
    input.click();
  }

  private onChangeFile(event: HTMLInputEvent) {
    let files = event.target.files;
    if (!files) {
      return;
    }
    let file = files[0];
    if (!file) {
      return;
    }

    // 同じファイルを選んでもイベントが発火するように
    event.target.value = '';

    this.readImageFile(file, MainFrame.BEFORE_IMAGE_CANVAS_ID);
    this.clearImage(MainFrame.AFTER_IMAGE_CANVAS_ID);
    this.file = file;
  }

  private readImageFile(file: File, canvasId: string) {
    const reader = new FileReader();
    reader.onload = e => this.drawImage(e.target!.result!, canvasId);
    reader.readAsDataURL(file);
  }

  private drawImage(file: string | ArrayBuffer, canvasId: string) {
    let canvas = <HTMLCanvasElement> document.getElementById(canvasId);
    let ctx = canvas.getContext('2d');
    // canvas上に画像を重ねて表示
    let img = new Image();
    img.src = file as string;
    img.onload = this.onloadImage(ctx!, img);
  }

  private onloadImage(ctx: CanvasRenderingContext2D, img: HTMLImageElement) {
    return () => {
      let canvasAspect = ctx.canvas.width / ctx.canvas.height; // canvasのアスペクト比
      let imgAspect = img.width / img.height // 画像のアスペクト比

      ctx.fillStyle = "black";
      ctx.fillRect(0, 0, ctx.canvas.width, ctx.canvas.height);

      let left;
      let top;
      let width;
      let height;
      if(imgAspect >= canvasAspect) {
        // 画像が横長
        left = 0;
        width = ctx.canvas.width;
        height = ctx.canvas.width / imgAspect;
        top = (ctx.canvas.height - height) / 2;
      } else {
        // 画像が縦長
        top = 0;
        height = ctx.canvas.height;
        width = ctx.canvas.height * imgAspect;
        left = (ctx.canvas.width - width) / 2;
      }
      ctx.drawImage(img, 0, 0, img.width, img.height, left, top, width, height);
    }
  }

  private clearImage(canvasId: string) {
    let canvas = <HTMLCanvasElement> document.getElementById(canvasId);
    let ctx = canvas.getContext('2d');
    ctx!.clearRect(0, 0, canvas.width, canvas.height);
  }

  private async onClickTab(event: HTMLClickEvent) {
    let target = event.target;

    if (!this.file) {
      return;
    }

    this.clearImage(MainFrame.AFTER_IMAGE_CANVAS_ID);

    let formData = new FormData();
    formData.append('file', this.file);
    formData.append('style', target!.textContent!);

    let response;
    try {
      response = await Vue.$fetch.post_original('api', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
    } catch (error) {
      console.error(error);
      return;
    }

    this.drawImage(response.data as string, MainFrame.AFTER_IMAGE_CANVAS_ID);
  }
}

interface HTMLInputEvent extends Event {
  target: HTMLInputElement & EventTarget
}

interface HTMLClickEvent extends Event {
  target: HTMLDivElement & EventTarget
}
</script>

<style scoped>

</style>
