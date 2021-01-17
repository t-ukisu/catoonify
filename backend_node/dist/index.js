"use strict";
// Load HTTP module
const onnx = require('onnxjs');
// import { Tensor, InferenceSession } from 
const Tensor = onnx.Tensor;
const InferenceSession = onnx.InferenceSession;
const hostname = "127.0.0.1";
const port = 8000;
function hello(name) {
    return `Hello, ${name}!`;
}
console.log(hello("World"));
// async runModel(input_array_:any) {
//     debugger;
//     // 推論に用いるセッションの初期化
//     // Backendには cpu や webgl, wasm を利用することができます
//     const session = new InferenceSession({ backendHint: 'webgl' })
//     // ONNX形式のモデルファイル
//     const modelFile = './sample.onnx' // ここで詰まる................................................................                                   
//     // モデルの読み込み
//     await session.loadModel(modelFile)
//     // Inputデータの準備（必要であれば事前に前処理をしておく必要があります）
//     // とりあえず、すべて0とするダミーデータを用意します
//     const inputTensor = new Tensor(input_array_, 'float32', [1, 3, 450, 450])
//     // 推論の実行
//     const outputData = await session.run([inputTensor])
//     return outputData;
//   };
//# sourceMappingURL=index.js.map