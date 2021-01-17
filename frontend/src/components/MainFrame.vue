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
import { Tensor, InferenceSession } from 'onnxjs'

@Component({})
export default class MainFrame extends Vue {

  private pushLoadButton() {
    const { input }: any = this.$refs;
    input.click();
    }

  async runModel(input_array_:any) {
    debugger;
    // 推論に用いるセッションの初期化
    // Backendには cpu や webgl, wasm を利用することができます
    const session = new InferenceSession({ backendHint: 'webgl' })

    // ONNX形式のモデルファイル
    const modelFile = './models/sample.onnx' // ここで詰まる................................................................                                   

    // モデルの読み込み
    await session.loadModel(modelFile)

    // Inputデータの準備（必要であれば事前に前処理をしておく必要があります）
    // とりあえず、すべて0とするダミーデータを用意します
    const inputTensor = new Tensor(input_array_, 'float32', [1, 3, 450, 450])

    // 推論の実行
    const outputData = await session.run([inputTensor])
    return outputData;
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
        ctx!.drawImage(img, 0, 0, 450, 450);
      }
    }
    reader.readAsDataURL(file);
    
    const imageDataScaled = ctx!.getImageData(0, 0, 450, 450);
    {/* imgData is now an array where every 4 places are each pixel. So [0][1][2][3] are the [r][g][b][a] of the first pixel. */}
    const input_array = new Float32Array(3*450*450);
    for (let i = 0, len = imageDataScaled.data.length; i < len; i += 4) {
      for (let j = 0; j < 3; j++) {
        input_array[i+j] = imageDataScaled.data[i+j] / 255;
      }
    }
    
    const tensor = new Tensor(input_array, 'float32', [1, 3, 450, 450]);
    

    // TODO API連携
    let output_array = this.runModel(tensor);
    // 色素が[0,1]に正規化されているので、[0,255]の範囲に復元する後処理を実施
    
  }
}
</script>

<style scoped>

</style>
