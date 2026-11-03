> 2026-10-12：1000件の整合性検査・旧100件の整理は完了しました。補助認識1件はユーザー指定で失敗結果として保存し、主結果とIG品質判定は維持しています。完了記録。以下の途中状態は過去の記録です。

# ASR Research

日本語Whisper系モデルの内部表現と認識挙動を解析する現行研究です。

## asr_prosody_probe

初期の共通基盤です。

- 音声の文字起こし
- log-Mel spectrogramの可視化
- Encoder hidden statesの抽出
- 層別Linear Probe
- PCA/UMAP可視化

専用の`.venv`は、現在のデータ処理スクリプトからも利用しています。

## whisper_pause_attention

JSUT basic5000へ人工的なpauseを挿入した中心実験です。

- 100音声、900条件
- 認識結果とCER
- Encoder hidden statesのLinear Probe
- Encoder self-attentionのMAD
- Decoder cross-attention peak shift
- Occlusion

現在有効な結果は`results_internal_pause/`と`figures_internal_pause/`、詳細レポートは`reports/`にあります。`archived_experiments/`は旧条件やsmoke testを隔離したものです。

## whisper_ig_reconstruction

[研究の入口HTML](../../ASR/whisper_ig_reconstruction/index.html)から、100件のトークン予測確率・差分音声・本番結果・発表資料へ移動できます。

Whisperが文字起こしに使う音の部分を推定し、重要度の低い部分を弱めて音声を作り直す実験です。初回の音声100件の準備・1件の動作確認に加え、ユーザー指示により64回で100件の本番を開始しました。最新の本番結果に保存します。

初めて見る場合は、フォルダ案内（ブラウザー用） または 文章版 を開いてください。
