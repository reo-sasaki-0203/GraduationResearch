# 実験結果一覧

[元音声ごとの音声・メル比較を開く](../../../../../ASR/whisper_ig_reconstruction/notes/research_hub/utterances.html)

新しい結果から、実験・検証ごとに並べています。完了した比較、品質基準未達、事前確認、保管済み記録を、それぞれの状態を添えて掲載します。
## 同一発話・同一雑音で混合比を操作する追試（完了）

[5組×4段階の結果](../../../../../ASR/whisper_ig_reconstruction/notes/research_hub/controlled-snr.html)。Whisper large-v3で20/20条件を新規に計算・検算。絶対IG95と正IG95の両方で再構成した。混合比ごとの相関、同じ領域の優勢が入れ替わったときの追従、再構成音の指標と試聴例を掲載した。

<!-- covers: results/analyses/source_dominance/controlled_20261125_v1 -->
<!-- covers: results/analyses/source_dominance/controlled_largev3_20261125_v1 -->
<!-- covers: results/analyses/source_dominance/controlled_largev3_20261125_v1_positive -->
<!-- covers: results/analyses/source_dominance/controlled_largev3_20261125_v1_precision/128 -->

## 声と雑音の局所的な優勢度とIG（2026-11-25）

[保存済み1000発話の対応解析](../../../../../ASR/whisper_ig_reconstruction/notes/research_hub/source-dominance.html)。1000/1000完了。声の優勢度と絶対IGの発話内順位相関は平均0.308。IGの成分保持差は同面積のenergy・randomを上回った。実際の再構成波形の減衰、SI-SDR、2モデルのCERとの関連、旧IG品質別・雑音別の限界を併記した。

<!-- covers: results/analyses/source_dominance/main1000_20261125_v1 -->


## クリーン単語IGと別ASRによる追加評価（2026-11-17）

1. **[クリーン入力の単語別IG：10発話・29語](../../../../../ASR/whisper_ig_reconstruction/notes/research_hub/clean-word-ig.html)**。新規計算・積分精度診断・全保持対照・4段階の再構成。計算の処理状態、IG数値品質、手動区間確認、本人による抽出成功判定を詳細ページで別々に示します。自動区間案は正解としません。
2. **[別ASRによる保存済み1000発話・5条件のCER評価](../../../../../ASR/whisper_ig_reconstruction/notes/research_hub/cross-asr.html)**。Reazon CTCの事前検証と、clean／mixture／従来絶対IG95／正IG95／DeepFilterNet3の対応比較。既存WAVを使い、IG再計算・音声再生成をせず評価します。Whisperは保存値を参照します。

<!-- covers: results/comparisons/clean_word_ig/clean10_20261117_v1 -->
<!-- covers: results/comparisons/cross_asr/main1000_20261117_reazon_v1 -->

## トークン別・単語別IG：同じ10音声

**[トークン毎のIG計算の結果：10音声](../../../../../ASR/whisper_ig_reconstruction/notes/research_hub/token-word-ig.html)**（2026-11-10、処理完了・失敗0件、数値品質未達あり）。本文226トークンと日本語148短単位を正IG95・90・80・60で比較、計1,496条件のWAV・実メルを検査。追加IG再計算0件。単語の厳密対応124・近似24、IG品質はトークン180件・単語130件未達。既存の10音声runからの派生結果で、元データと元の全文比較を保持しています。

## 正IGの保持率を変えた10音声の試行

1. **[正IG90・85・80：同じ10音声の比較](../../../../../ASR/whisper_ig_reconstruction/notes/research_hub/positive-fractions-pilot.html)**（2026-11-10、30件完了・失敗0件）
   5雑音から各2件。同じ10音声×3条件の音声・実音声由来メルを保存し、各元音声の比較枠に正IG95・従来reconstructed・mixture・clear・DeepFilterNet3と並べています。処理結果と各音声へのリンクは詳細ページで確認できます。

<!-- token-ig-pilot-summary -->
[トークン毎のIG計算の結果：10音声](../../../../../ASR/whisper_ig_reconstruction/notes/research_hub/token-word-ig.html)を独立掲載。本文226トークンと日本語単語の正IG95・90・80・60、対応近似・品質未達・全件検査を明記。

<!-- covers: results/comparisons/positive_ig_fractions/main1000_20261110_pos908580_pilot10_v1 -->

## 1000件の比較

<span id="ig9510002026-11-09"></span>

1. **[正のIG累積95%・1000件の追加比較](../../../../../ASR/whisper_ig_reconstruction/notes/research_hub/positive-ig95.html)**（2026-11-09、完了）  
   mixture・従来IG95・正のIG95を比較。CER、2種類の固定文F、メルMAE、SI-SDR、保持数・面積率の全体・雑音別結果と検査記録。平均CERは7.716 / 8.755 / 12.063%、保持面積は100 / 62.516 / 29.492%。IGは再計算していません。面積差があるため、負の寄与除去だけの効果とは断定しません。
2. **[1000件・IG再構成とDeepFilterNet3の統合比較](../../../../../ASR/whisper_ig_reconstruction/notes/research_hub/main1000-results.html)**（2026-10-10〜14、完了・補助失敗1件を保存）  
   clear・mixture・IG再構成・DeepFilterNet3の4条件。全1000件の音声・図・各発話の比較へ進めます。従来のIGのみのA/B/C分析は同じ実験の追加分析・原記録として、このページにまとめています。

<!-- covers: results/comparisons/positive_ig95/main1000_20261109_pos95_v1 -->
<!-- covers: results/comparisons/deepfilternet3/main1000_20261010_dfn3_v1 -->
<!-- covers: results/experiments/whisper-large-v3/ig64_cum95_hard/main1000_20261010 -->
<!-- covers: results/analyses/whisper-large-v3/ig64_cum95_hard/main1000_20261010/abc_v1 -->

## 旧100件・事前の実験と検証

[旧100件の整理状態・評価記録の保全（2026-11-10監査）](../../../../../ASR/whisper_ig_reconstruction/notes/research_hub/old100-cleanup.html)：過去の削除7対象の不在を確認。今回新規削除0件・0 byte。現行参照のある事前試行・共有データは保持。

1. **旧100件・IG64累積95%の結果**（保管済み）  
   設定・集計・品質診断・失敗記録を保持。旧音声・配列・図は、新1000件の検査後に整理済みです。トークン確率・差分音声分析の保管記録も同じ旧100件の追加分析です。
2. **IG64・3件の事前試行**（指定3件を完了）  
   準備済み100件のうち3件を評価した記録。残り97件まで完了した実験ではありません。
3. **IG64・品質ゲートの事前試験**（品質基準未達で停止）  
   混合入力100件の準備後、IG品質判定で停止。保存済みの評価失敗1件・未処理99件をそのまま示します。
4. **IG64・1音声の処理手順検証**（診断完了）  
   実音声1件で認識・IG・マスク・再構成・評価の接続を確認した記録。本実験100件の完了とは区別します。
5. **Whisper large-v3・float32積分診断**（品質基準未達）  
   1音声のIG32/64/128/256等の診断と参考出力。診断結果・実行状態・設定。3条件pilotや本番100件の成功として数えません。
6. **Whisper large-v3・32/64点の積分診断**（品質基準未達）  
   1音声のcompleteness・マスク安定性が不足した記録。診断結果・実行状態。参考出力を保持しています。
7. **Whisper large-v3・初期モデル診断**（失敗・保留）  
   decoderの開始トークン配置で停止。実行状態・モデル情報。完成した再構成実験として扱いません。

<!-- covers: results/main64_ig95 -->
<!-- covers: results/analyses/whisper-large-v3/ig64_cum95_hard/main64_ig95/token_scores_v1 -->
<!-- covers: results/pilot64_run -->
<!-- covers: results/pilot64_ig95 -->
<!-- covers: results/pipeline64_diagnostic -->
<!-- covers: results/largev3_fp32_diagnostic -->
<!-- covers: results/largev3_diagnostic_v2 -->
<!-- covers: results/largev3_diagnostic -->

## データ準備・基盤の確認記録

1. **本番前のデータ確認**（音声100件を準備、混合は未作成）  
   雑音区間の試聴記録待ちで停止した当時の状態です。後続の実験結果と区別します。
2. **入力準備の確認**（選定のみ）  
   100件の選定記録。混合・モデル評価の完了件数は0です。
3. **最初のデータ選定**（選定のみ）  
   100件の選定と、元音声・雑音候補の確認記録です。
4. **合成音声・環境の基盤検査**  
   合成音声による検査結果・検査ログ・環境診断。研究データでの性能比較とは区別します。

<!-- covers: results/final_data_review -->
<!-- covers: results/prepared_review -->
<!-- covers: results/data_review -->
<!-- covers: results/validation -->

数値の良し悪し、処理完了、IGの数値品質を分けて記録しています。失敗・未処理を0の性能値や成功へ置き換えていません。2026-11-10までの一覧整備では保存済み記録を参照し、過去の実験を再実行していません。2026-11-17の新規実行2件は上段に別runとして掲載しています。
