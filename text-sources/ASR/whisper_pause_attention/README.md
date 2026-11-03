# Whisper Pause Attention

Whisper 系 ASR モデルにおいて、発話前後に挿入した無音区間が encoder
self-attention、decoder cross-attention、文字起こし結果へどう影響するかを調べる
ための初手実験コードです。

添付指示では JSUT basic5000 を主対象にしていましたが、このワークスペースには
既に `../../../data_processing/data` に音声とテキストがあるため、`configs/smoke.yaml`
はその既存データを読む設定にしています。JSUT を使う場合は config の
`dataset.type` を `jsut` に変更し、`dataset.jsut_root` を実パスへ変えてください。

## セットアップ

CUDA 対応 PyTorch はサーバー環境に合わせて入れてください。既に使っている venv が
あるならそれを有効化して構いません。

```bash
cd ASR/whisper_pause_attention
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

large-v3 の attention 取得は重いので、最初は必ず `configs/smoke.yaml` の
`models` を 1 モデル、`n_samples` を 1 にしたまま確認してください。

## Smoke Test

```bash
bash scripts/run_smoke.sh
```

同等の Python コマンド:

```bash
python -m src.run_experiment --config configs/smoke.yaml
```

GPU メモリが足りない場合:

```bash
python -m src.run_experiment \
  --config configs/smoke.yaml \
  --models kotoba-tech/kotoba-whisper-v1.0 \
  --n_samples 1 \
  --skip_occlusion
```

## Full 実験

smoke test が通った後にだけ実行してください。

```bash
bash scripts/run_full.sh
```

`configs/full.yaml` は JSUT basic5000、`kotoba-tech/kotoba-whisper-v2.0`、
100サンプル、前方無音のみの条件を想定しています。
後方無音は Whisper の padding と区別しにくいため、現在は `post_silence_sec: [0.0]`
に固定しています。`jsut_root` は環境に合わせて書き換えてください。

## 出力 CSV

`results/` に以下を保存します。

- `manifest_source.csv`: 元サンプルの一覧
- `manifest_augmented.csv`: 前方無音を挿入した音声の一覧
- `transcriptions.csv`: generate mode の文字起こし、CER、exact match
- `encoder_mad.csv`: encoder self-attention の mean attention distance
- `cross_attention_peaks_teacher_forcing.csv`: teacher forcing cross-attention peak
- `occlusion.csv`: waveform occlusion と CER 変化
- `occlusion_correlation.csv`: attention mass と delta CER の Spearman 相関
- `summary_kotoba_v2_pre_silence.md`: v2.0 前方無音実験の要約
- `summary_pre_silence_cer.csv`: 前方無音条件ごとの CER と 0秒条件との差分
- `summary_pre_silence_tests.csv`: 前方無音条件の対応あり検定
- `summary_occlusion_by_region.csv`: occlusion 領域別要約

## 図

`figures/` に保存します。

- `encoder_mad_by_layer_<model>.png`
- `encoder_mad_heatmap_<model>_<condition>.png`
- `cross_peak_shift_<model>.png`
- `occlusion_attention_vs_delta_cer_<model>.png`
- `examples/cross_attention_example_*.png`

既存 CSV から図だけ再生成する場合:

```bash
python -m src.run_experiment --config configs/smoke.yaml --plots_only
```


## 実験結果の分離

後方無音ありで実行した旧結果は `archived_experiments/post_silence_full_20260623/`
に隔離しています。v1.0/large-v3 の前方無音小規模結果は
`archived_experiments/pre_silence_jsut5_v1_largev3_20260623/`、v2.0 の
1サンプル確認結果は `archived_experiments/kotoba_v2_pre_silence_smoke_n1_20260624/`
に隔離しています。通常の `results/`、`figures/`、`augmented_audio/` には、
現在実行している実験の結果だけを置く運用にします。

## 研究上の仮定と注意

- encoder index と時間は初期実装では `time_sec = encoder_index * 0.02` とみなします。
- Whisper processor は 30 秒へ padding します。後方無音は padding と解釈が混ざりやすいため、
  現在の実験では追加せず、`post_silence_sec: [0.0]` に固定しています。
  augmented audio の実時間を超える encoder frame は padding として扱います。
- attention は説明の十分条件ではありません。occlusion による文字起こし変化と
  合わせて解釈してください。
- attention weights を得るため、`attn_implementation: eager` を既定にしています。
  SDPA / Flash Attention では weights が返らない場合があります。
- attention tensor 全体は保存しません。集計値 CSV と代表例の compressed npz だけを
  保存します。

## まだ簡略化している点

- occlusion は smoke では selected windows のみです。full sliding window は
  `src/occlusion.py` を拡張すれば入れられる設計です。
- generate mode の cross-attention 取得は未実装です。現状は teacher forcing を主解析、
  generate は transcription と CER の保存に使います。
- GPU メモリ節約のための layer/head subset は config 項目としては未実装です。
  大きいモデルで落ちる場合は `n_samples`、条件数、occlusion を減らしてください。
