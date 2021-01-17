// Load HTTP module
const onnx = require('onnxjs');
// import { Tensor, InferenceSession } from 
const Tensor = onnx.Tensor

const InferenceSession = onnx.InferenceSession
// ------------

const http = require('http');
const express = require('express');

const app = express();
const port = process.env.PORT || 3000;
app.listen(port, () => console.log(`Listening on port ${port}...`));

app.post('/', (req:any, res:any) => {
  res.send('Simple REST API');
});


// ------------
// function hello(name: string): string {
//   return `Hello, ${name}!`;
// }

// console.log(hello("World"));



async function runModel(input_array_:any) {
    debugger;
    // 推論に用いるセッションの初期化
    // Backendには cpu や webgl, wasm を利用することができます
    const session = new InferenceSession({ backendHint: 'webgl' })

    // ONNX形式のモデルファイル
    const modelFile = './sample.onnx' // ここで詰まる................................................................                                   

    // モデルの読み込み
    await session.loadModel(modelFile)

    // Inputデータの準備（必要であれば事前に前処理をしておく必要があります）
    // とりあえず、すべて0とするダミーデータを用意します
    const inputTensor = new Tensor(input_array_, 'float32', [1, 3, 450, 450])

    // 推論の実行
    const outputData = await session.run([inputTensor])
    return outputData;
  };
