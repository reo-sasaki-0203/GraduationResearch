# ASR Prosody Probe

日本語 ASR モデルの Encoder hidden states に、通常発話 (`speech`)、
無音区間 (`pause`)、フィラー (`filler`) の情報がどの程度線形に表現されて
いるかを調べるための初期実験コードです。Kotoba-Whisper を既定値とし、
Hugging Face Transformers で扱える Whisper 系モデルを切り替えて使えます。

## ディレクトリ構成

```text
asr_prosody_probe/
  README.md
  requirements.txt
  scripts/
    transcribe_audio.py
    visualize_log_mel_spectrograms.py
    extract_hidden_states.py
    run_probe.py
    visualize_embeddings.py
  src/
    audio_utils.py
    dataset_utils.py
    label_utils.py
    whisper_utils.py
    probe_utils.py
    plot_utils.py
  data/
    audio/
    labels/
  outputs/
    hidden_states/
    transcriptions/
    probe_results/
    figures/
```

## 環境構築

Python 3.10 以降を想定しています。この環境の NVIDIA driver に合わせ、
`requirements.txt` は CUDA 12.1 対応の `torch==2.5.1+cu121` と
`torchaudio==2.5.1+cu121` を固定しています。GPU がなくても CPU で動作します。
別環境では必要に応じてこの 2 行を変更してください。

```bash
cd asr_prosody_probe
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## データとラベル CSV

音声ファイルを `data/audio/` に置きます。短い WAV ファイルを推奨します。
入力は抽出時に mono、16 kHz に変換されます。

例: `data/audio/sample01.wav`

対応する CSV を `data/labels/` に置きます。

例: `data/labels/sample01_labels.csv`

```csv
start,end,label
0.00,1.25,speech
1.25,1.80,pause
1.80,2.35,filler
2.35,4.90,speech
```

時刻の単位は秒です。ラベルは `speech`、`pause`、`filler` のいずれかに
してください。ラベルがない時間帯の Encoder frame は実験対象から除外されます。

## 1. 文字起こし結果の確認

`kotoba-tech/kotoba-whisper-v2.0` で短い音声ファイルを文字起こしし、CSV と
Markdown に保存します。

```bash
python3 scripts/transcribe_audio.py \
  --audio_dir data/audio \
  --device cuda:0
```

主な出力:

```text
outputs/transcriptions/kotoba_whisper_v2_0_transcriptions.csv
outputs/transcriptions/kotoba_whisper_v2_0_transcriptions.md
```

## 2. Log-Mel Spectrogram 可視化

Whisper に近い設定 (`16 kHz`, `n_fft=400`, `hop_length=160`,
`win_length=400`, `n_mels=80`) で log-Mel spectrogram を描画します。
音声間を比較しやすいように、色の基準は入力音声全体で共通です。

```bash
python3 scripts/visualize_log_mel_spectrograms.py \
  --audio_dir data/audio \
  --output_dir outputs/figures/log_mel_spectrograms
```

個別の PNG と、全音声を縦に並べた比較用 PNG が保存されます。

```text
outputs/figures/log_mel_spectrograms/1_normal_log_mel.png
outputs/figures/log_mel_spectrograms/log_mel_spectrograms_overview.png
```

## 3. Hidden States 抽出

```bash
python3 scripts/extract_hidden_states.py \
  --model_name kotoba-tech/kotoba-whisper-v2.0 \
  --audio_dir data/audio \
  --output_dir outputs/hidden_states
```

別モデルを使う場合は、たとえば `--model_name openai/whisper-small` を指定します。
CUDA があれば自動的に CUDA、なければ CPU を使います。明示する場合は
`--device cpu` や `--device cuda:0` を指定します。

WhisperProcessor は短い入力も固定長に pad します。このコードは音声区間に
対応する Encoder frame のみを保存します。30 秒を超える音声は最初の 30 秒だけを
解析し、実際に解析した時間を `outputs/hidden_states/metadata.csv` に記録します。

保存例:

```text
outputs/hidden_states/sample01_layer00.npy
outputs/hidden_states/sample01_layer01.npy
outputs/hidden_states/metadata.csv
```

`layer00` は Transformers が返す Encoder 埋め込み出力です。それ以降に各
Encoder block の hidden states が続きます。各 `.npy` の shape は
`(num_frames, hidden_dim)` です。

## 4. 層別 Probing

```bash
python3 scripts/run_probe.py \
  --hidden_dir outputs/hidden_states \
  --label_dir data/labels \
  --audio_dir data/audio \
  --output_csv outputs/probe_results/layerwise_metrics.csv
```

各層について `LogisticRegression(max_iter=1000, class_weight="balanced")` を
学習し、accuracy、macro F1、ラベル別 frame 数を保存します。frame `i` の時刻は
`i / num_frames * analyzed_duration_sec` で近似します。

主な出力:

```text
outputs/probe_results/layerwise_metrics.csv
outputs/probe_results/confusion_matrix_layer00.csv
outputs/figures/layerwise_probe_accuracy.png
outputs/figures/layerwise_probe_macro_f1.png
```

壊れた入力は原因をログに表示してスキップします。1 件でも問題があれば停止したい
場合は `--strict` を追加してください。

## 5. PCA / UMAP 可視化

```bash
python3 scripts/visualize_embeddings.py \
  --hidden_dir outputs/hidden_states \
  --label_dir data/labels \
  --audio_dir data/audio \
  --layers 0 mid last \
  --output_dir outputs/figures
```

既定では layer 0、中間層、最終層を PCA で可視化します。`umap-learn` が import
できる場合は UMAP 版も保存します。PCA のみを作る場合は `--skip_umap` を追加します。
描画負荷を抑えるため、各層から最大 5000 frame を固定 seed で抽出します。

主な出力:

```text
outputs/figures/pca_layer00.png
outputs/figures/pca_layermid.png
outputs/figures/pca_layerlast.png
outputs/figures/umap_layer00.png
```

## 軽量テスト

モデルをダウンロードせず、ラベル対応と probe の共通処理だけを確認できます。

```bash
python3 -m unittest discover -s tests -v
```

## 今後の拡張案

- pause / non-pause の二値分類
- フィラー種別ごとの分類
- pause duration の回帰
- speech rate との相関分析
- hallucination が出た無音区間の表現解析
- decoder cross-attention heatmap の可視化
- CKA / CCA による層間表現比較

hidden states と frame label の対応付けは `src/dataset_utils.py` に分離しているため、
分類器や可視化方法を追加するときに再利用できます。
