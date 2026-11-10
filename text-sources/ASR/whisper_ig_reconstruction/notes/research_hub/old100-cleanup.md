# 旧100件の整理状態と評価記録の保全

2026-11-10に依存関係と保存状態を再監査しました。**今回の新規削除は0件・削減容量0 byte**です。旧主100件の大容量データは既に整理されており、今回削除したものとして数えません。

[実験結果一覧](../../../../../ASR/whisper_ig_reconstruction/notes/research_hub/results.html) · 旧100件の保管ページ

## 過去の削除と今回の確認

既存の `backups/old100_cleanup.json` の削除7対象がすべて存在しないことを確認しました。過去の論理サイズ合計は6,553,588,409 byte（約6.10 GiB）。同記録の空き容量差は6,754,271,232 byteであり、共有ファイルシステムの空き容量変動と論理サイズを同一視しません。元の削除JSONに実施日時はありません。`completion_20261012` の保管記録はありますが、正確な削除時刻を推定して補っていません。

|過去に削除済みの対象|記録上の論理byte|
|---|---:|
|`results/main64_ig95/samples`|6,295,685,547|
|同runの`clean_pool`|33,794,284|
|同runの`clean_review`|738,800|
|同runの`noise_review`|11,520,240|
|同runの`figures`|220,436|
|同runの`supplement_all100`|228,987|
|旧100件`token_scores_v1/samples`|211,400,115|

今回の監査日時・対象サイズ・保持判断はサーバ内 `backups/old100_audit_20261110/audit.json`。残す小容量の記録一覧とSHA256は同フォルダの `preserved_records.json` に保存しました。元の削除記録も変更していません。

## 保持・保留の範囲と理由

旧主100件の設定・選定一覧は主1000件の由来にも必要です。`configs/main1000.yaml` の `include_selection` が旧 `selection.json` を参照しているため、run全体は削除しません。1000件の入力・出力、今回の10音声・保存トークンIG・再開チェックポイント、共有JSUT・雑音・モデルはすべて保持しました。

`results/pilot64_run`（486,151,233 byte）、`pilot64_ig95`（199,616,159 byte）、`pipeline64_diagnostic`（60,365,255 byte）、`largev3_diagnostic_v2`（38,278,431 byte）、`largev3_fp32_diagnostic`（41,358,948 byte）は独立した事前試行・診断であり、現行の結果ページと `comparison_tools/utterance_browser.py` が参照しています。**今回の削除対象から除外・保持**しました。これらを旧主100件の不要な重複とみなす根拠はなく、音声を削除すると現行の試聴に影響します。共有・由来が不明なファイルは推測で削除していません。

`backups/old100_record` は1,661ファイル・13,603,992 byteの設定・評価・失敗・個別トークンスコア等で、WAV/NPY/NPZは0件です。原記録を保持し、今回の容量削減のために消しません。監査で触れた `data/` も共有データのため保持。

旧主100件と旧トークン分析のHTMLには、過去の削除7対象への音声・図・sampleリンクが残っていないことを文字列検査しました。今回新たな削除に伴う参照変更はありません。旧試行と現行1000件の対応をsample番号だけで同一視していません。

## 残した既存評価値

以下は `results/main64_ig95/metrics/plain_summary.json` と `supplement_summary.json` の保存値の転記で、今回のCER再測定ではありません。100件・4雑音（white/washing/kitchen/traffic）×5 SNR（0/5/10/15/20 dB）各5件・Whisper large-v3・bfloat16・IG64・従来の絶対IG累積95%などの設定は同runの `config.yaml`、対象は `selection.json` / `selection_manifest.csv`、評価定義・条件は `report.md` と `metrics/aggregate_all100.csv` に保持。

|条件|音響比較件数|保存済み参照文CER（発話平均）|メルMAE dB|IG品質合格対象数|
|---|---:|---:|---:|---:|
|mixture|100|5.328616%|10.822775|19|
|reconstruction_only|100|5.473031%|10.741862|19|
|ig95_hard|100|6.399808%|9.399999|19|
|random_matched|100|6.652142%|10.515959|19|
|energy_matched|100|5.861650%|9.280366|19|

元runの評価段階は成功99件・失敗1件（sample_0079、EOSなし）のまま保存。後続の補足集計は100件の音響値と同設定ASR診断に由来し、元の失敗段階を成功に変更していません。品質は19合格・81未達。保存された補足表のASR成功数は各条件100であり、元runの「99成功・1失敗」とは処理段階が異なります。両者の記録を保持しています。

残した保存先は `results/main64_ig95/metrics/`、`backups/old100_record/experiment/` と `backups/old100_record/token_scores_v1/`。公開版はこの説明・集計のみで、個別音声・配列・個人メモ・会話ログは収録しません。
