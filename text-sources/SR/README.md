# Legacy Speech Recognition Experiments

ReazonSpeechやESPnetを使って音声認識を試した、現在より前の実験です。

- `espnet/`: ESPnet本体のGit clone
- `SRvenv/`: 当時のPython仮想環境。2026-10-10に利用者の指示で削除済み。
- `eval_data/`: 評価データ
- `unseen_data/`: 未見データ
- `download_*.py`: データ取得スクリプト
- `transcribe_*.py`: 文字起こしスクリプト
- `test_*.py`: モデル評価スクリプト

現在のpause・attention・反復エラー研究とは直接接続していませんが、ASRの過去実験として保管しています。`SRvenv`は現在の研究からの依存がないことを確認し、削除しました。コードと評価データは保持しています。

削除した実行環境は約7.7GBでした。Python設定・道具とその版・PyTorch/CUDAの版を 整理記録 の environment_records/SRvenv/ に保存しました。
