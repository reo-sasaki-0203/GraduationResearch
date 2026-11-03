# 発話内部pause長操作実験レポート

PDF: `ASR/whisper_pause_attention/reports/internal_pause_experiment_report.pdf`

生成日時: 2026-06-25 09:56


## 要約

発話内部 pause 長操作による Encoder 表現・Cross-attention・認識変化の解析

対象モデル: kotoba-tech/kotoba-whisper-v2.0
データ: JSUT basic5000 100サンプル
条件: 0 / 200 / 500 / 1000 / 2000 ms の発話内部pause挿入、zero silence と room-tone silence
生成日時: 2026-06-25 09:56

このPDFの目的は、「何のための実験か」「どのような処理をしたか」「どの図表をどう読むか」「得られた結果から何が言えるか」を、初学者でも追える形で一つにまとめることである。

重要な結論を先に述べる。
- 転写結果そのものは大きくは崩れなかった。0ms baselineの平均CERは 0.0862、pause挿入条件を含めた平均CER範囲は 0.0830〜0.0910 だった。
- しかし decoder cross-attention のpeakはpause長にほぼ比例して後ろへずれた。つまり、文字起こしが安定していても、内部の時間アライメントはpauseを反映して動いている。
- encoder hidden statesからpause/speechやpause境界は高精度に線形分類できた。pause/speech分類の最高macro F1はlayer 22で0.9991、boundary分類の最高macro F1はlayer 30で0.9838だった。
- pause長そのものもhidden statesからかなり読めた。pause duration回帰の最高R2はlayer 25で0.9650だった。
- occlusionでは発話中の語をmaskすると大きく認識が変わる一方、inserted_pauseそのもののmaskは平均delta CERが小さかった。pauseは転写文字列を直接壊すというより、境界表現やアライメントに残る情報として効いている可能性がある。


## 実験概要

## 研究上の問い
ASRモデルは、発話中に挿入された無音pauseを単なる「何もない区間」として無視しているのか、それとも内部表現やattentionの中に保持しているのかを調べた。

この問いは、フィラー、長い間、文中pause、話者の迷いなどを扱ううえで重要である。文字起こしだけを見ると同じ文に見えても、内部では「どこで間があったか」「pause後の語がどれだけ後ろへずれたか」が表現されている可能性がある。

## 実験デザイン
JSUT basic5000の短い読み上げ音声100件を使い、各音声の指定時刻にpauseを挿入した。pause長は0, 200, 500, 1000, 2000 msで、200ms以上ではzero silenceとroom-tone silenceの2種類を作った。0msはbaselineとして1条件のみである。

無音種別の意味は以下である。
- zero silence: 波形値が完全に0の無音。
- room-tone silence: 同じ音声の低エネルギー区間をコピーして作った、背景音に近い無音風区間。

結果として、100件 x (0ms + 4 pause長 x 2無音種別) = 900条件を評価した。


## 解析手法

## 解析A: 認識結果
各条件でkotoba-whisper-v2.0に音声を入力し、転写結果を得た。参照文との比較にはCERを使った。CERは文字単位の誤り率で、低いほど参照文に近い。

併せてexact match、挿入誤り、削除誤り、置換誤りを数えた。また、pause後の文字列が特に悪化するかを見るため、発話時刻と文字位置を比例対応させた近似的なpost_pause_tail_cer_approxも計算した。

## 解析B: Encoder hidden statesのLinear Probe
各encoder frameに speech / inserted_pause / pre_pause_boundary / post_pause_boundary / padding のラベルを付け、各層のhidden statesから線形モデルで読み出せるか調べた。

分類では、pause/speech分類accuracy・macro F1と、boundary分類macro F1を見た。さらにinserted_pauseフレームだけを使い、pause durationを回帰してR2を測った。この解析の狙いは、pause情報がどの層に、どれくらい線形に残っているかを調べることである。

## 解析C: Encoder self-attention MAD
Encoder self-attentionについて、各query frameがどれくらい離れたkey frameへ注意を向けているかをmean attention distance、MADとして計算した。MADが大きいほど、より広い時間範囲を見ていると解釈できる。

領域は inserted_pause、pre_pause_boundary、post_pause_boundary、speech_no_inserted_pause などに分けた。pause周辺でattention距離が変わるかを見るためである。

## 解析D: Decoder cross-attention peak shift
Decoder cross-attentionは、各出力tokenがencoder側のどの時間フレームを強く見ているかを示す。0ms条件を基準にし、pause後tokenのpeakがpause長の分だけ後ろへずれるかを測った。

理想的には、500ms pauseならpause後tokenのpeakは約0.5秒後ろへ、1000ms pauseなら約1.0秒後ろへずれる。この追従性が高ければ、cross-attention peakは時間アライメントの手がかりとして使える。

## 解析E: Occlusion
音声の一部をmaskし、転写やCERが変わるかを見た。mask対象は inserted_pause、pause直前語、pause直後語、発話中央語、padding領域である。

狙いは、「モデルが実際にその時間領域を認識に使っているか」を確認すること。語の領域をmaskしてCERが上がるなら妥当であり、pauseそのものをmaskして大きく変わるなら、無音が単なる空白ではなく文脈境界や終了判断に使われている可能性が出てくる。


## 認識結果
| silence_kind | pause_duration_ms | n | mean_cer | median_cer | exact_match_rate |
| --- | --- | --- | --- | --- | --- |
| none | 0 | 100 | 0.0862 | 0.0607 | 0.3400 |
| room_tone | 200 | 100 | 0.0865 | 0.0580 | 0.3400 |
| room_tone | 500 | 100 | 0.0833 | 0.0563 | 0.3500 |
| room_tone | 1000 | 100 | 0.0897 | 0.0563 | 0.3300 |
| room_tone | 2000 | 100 | 0.0901 | 0.0563 | 0.3300 |
| zero | 200 | 100 | 0.0852 | 0.0563 | 0.3600 |
| zero | 500 | 100 | 0.0830 | 0.0563 | 0.3600 |
| zero | 1000 | 100 | 0.0888 | 0.0563 | 0.3400 |
| zero | 2000 | 100 | 0.0910 | 0.0563 | 0.3400 |

| silence_kind | pause_duration_ms | mean_insertions | mean_deletions | mean_substitutions | mean_post_pause_tail_cer_approx |
| --- | --- | --- | --- | --- | --- |
| none | 0 | 0.2900 | 0.3100 | 1.4400 | 0.1008 |
| room_tone | 200 | 0.3000 | 0.3100 | 1.4200 | 0.1024 |
| room_tone | 500 | 0.2800 | 0.3100 | 1.3900 | 0.0979 |
| room_tone | 1000 | 0.3300 | 0.3000 | 1.4600 | 0.1044 |
| room_tone | 2000 | 0.3400 | 0.3000 | 1.4600 | 0.1051 |
| zero | 200 | 0.3000 | 0.3000 | 1.4200 | 0.1002 |
| zero | 500 | 0.3000 | 0.2900 | 1.4000 | 0.0966 |
| zero | 1000 | 0.3400 | 0.2900 | 1.4400 | 0.1032 |
| zero | 2000 | 0.3500 | 0.3100 | 1.4500 | 0.1078 |


## Linear Probe
| probe | layer | n | accuracy | macro_f1 |
| --- | --- | --- | --- | --- |
| pause_vs_speech | 0 | 13600 | 0.9585 | 0.9584 |
| boundary_multiclass | 0 | 21478 | 0.8188 | 0.8173 |
| pause_vs_speech | 1 | 13600 | 0.9859 | 0.9858 |
| boundary_multiclass | 1 | 21478 | 0.9438 | 0.9435 |
| pause_vs_speech | 2 | 13600 | 0.9897 | 0.9897 |
| boundary_multiclass | 2 | 21478 | 0.9493 | 0.9491 |
| pause_vs_speech | 3 | 13600 | 0.9918 | 0.9917 |
| boundary_multiclass | 3 | 21478 | 0.9596 | 0.9595 |
| pause_vs_speech | 4 | 13600 | 0.9918 | 0.9917 |
| boundary_multiclass | 4 | 21478 | 0.9607 | 0.9606 |
| pause_vs_speech | 5 | 13600 | 0.9941 | 0.9941 |
| boundary_multiclass | 5 | 21478 | 0.9648 | 0.9647 |
| pause_vs_speech | 6 | 13600 | 0.9950 | 0.9950 |
| boundary_multiclass | 6 | 21478 | 0.9659 | 0.9658 |
| pause_vs_speech | 7 | 13600 | 0.9956 | 0.9956 |
| boundary_multiclass | 7 | 21478 | 0.9693 | 0.9692 |
| pause_vs_speech | 8 | 13600 | 0.9956 | 0.9956 |
| boundary_multiclass | 8 | 21478 | 0.9706 | 0.9705 |
| pause_vs_speech | 9 | 13600 | 0.9962 | 0.9962 |
| boundary_multiclass | 9 | 21478 | 0.9713 | 0.9712 |
| pause_vs_speech | 10 | 13600 | 0.9965 | 0.9965 |
| boundary_multiclass | 10 | 21478 | 0.9708 | 0.9707 |
| pause_vs_speech | 11 | 13600 | 0.9971 | 0.9970 |
| boundary_multiclass | 11 | 21478 | 0.9719 | 0.9718 |
| pause_vs_speech | 12 | 13600 | 0.9965 | 0.9965 |
| boundary_multiclass | 12 | 21478 | 0.9749 | 0.9748 |
| pause_vs_speech | 13 | 13600 | 0.9965 | 0.9965 |
| boundary_multiclass | 13 | 21478 | 0.9734 | 0.9733 |
| pause_vs_speech | 14 | 13600 | 0.9965 | 0.9965 |
| boundary_multiclass | 14 | 21478 | 0.9737 | 0.9737 |
| pause_vs_speech | 15 | 13600 | 0.9965 | 0.9965 |
| boundary_multiclass | 15 | 21478 | 0.9741 | 0.9741 |
| pause_vs_speech | 16 | 13600 | 0.9974 | 0.9973 |
| boundary_multiclass | 16 | 21478 | 0.9726 | 0.9726 |
| pause_vs_speech | 17 | 13600 | 0.9971 | 0.9970 |
| boundary_multiclass | 17 | 21478 | 0.9745 | 0.9745 |
| pause_vs_speech | 18 | 13600 | 0.9974 | 0.9973 |
| boundary_multiclass | 18 | 21478 | 0.9745 | 0.9745 |
| pause_vs_speech | 19 | 13600 | 0.9982 | 0.9982 |
| boundary_multiclass | 19 | 21478 | 0.9771 | 0.9771 |
| pause_vs_speech | 20 | 13600 | 0.9982 | 0.9982 |
| boundary_multiclass | 20 | 21478 | 0.9795 | 0.9795 |
| pause_vs_speech | 21 | 13600 | 0.9988 | 0.9988 |
| boundary_multiclass | 21 | 21478 | 0.9777 | 0.9776 |
| pause_vs_speech | 22 | 13600 | 0.9991 | 0.9991 |
| boundary_multiclass | 22 | 21478 | 0.9780 | 0.9780 |
| pause_vs_speech | 23 | 13600 | 0.9985 | 0.9985 |
| boundary_multiclass | 23 | 21478 | 0.9799 | 0.9799 |
| pause_vs_speech | 24 | 13600 | 0.9982 | 0.9982 |
| boundary_multiclass | 24 | 21478 | 0.9806 | 0.9806 |
| pause_vs_speech | 25 | 13600 | 0.9985 | 0.9985 |
| boundary_multiclass | 25 | 21478 | 0.9808 | 0.9808 |
| pause_vs_speech | 26 | 13600 | 0.9985 | 0.9985 |
| boundary_multiclass | 26 | 21478 | 0.9806 | 0.9806 |
| pause_vs_speech | 27 | 13600 | 0.9982 | 0.9982 |
| boundary_multiclass | 27 | 21478 | 0.9812 | 0.9812 |
| pause_vs_speech | 28 | 13600 | 0.9976 | 0.9976 |
| boundary_multiclass | 28 | 21478 | 0.9799 | 0.9799 |
| pause_vs_speech | 29 | 13600 | 0.9976 | 0.9976 |
| boundary_multiclass | 29 | 21478 | 0.9829 | 0.9829 |
| pause_vs_speech | 30 | 13600 | 0.9976 | 0.9976 |
| boundary_multiclass | 30 | 21478 | 0.9838 | 0.9838 |
| pause_vs_speech | 31 | 13600 | 0.9985 | 0.9985 |
| boundary_multiclass | 31 | 21478 | 0.9825 | 0.9825 |
| pause_vs_speech | 32 | 13600 | 0.9988 | 0.9988 |
| boundary_multiclass | 32 | 21478 | 0.9829 | 0.9829 |

| probe | layer | n | r2 |
| --- | --- | --- | --- |
| pause_duration_regression | 0 | 6400 | 0.1316 |
| pause_duration_regression | 1 | 6400 | 0.8504 |
| pause_duration_regression | 2 | 6400 | 0.9230 |
| pause_duration_regression | 3 | 6400 | 0.9386 |
| pause_duration_regression | 4 | 6400 | 0.9438 |
| pause_duration_regression | 5 | 6400 | 0.9483 |
| pause_duration_regression | 6 | 6400 | 0.9561 |
| pause_duration_regression | 7 | 6400 | 0.9571 |
| pause_duration_regression | 8 | 6400 | 0.9588 |
| pause_duration_regression | 9 | 6400 | 0.9578 |
| pause_duration_regression | 10 | 6400 | 0.9604 |
| pause_duration_regression | 11 | 6400 | 0.9605 |
| pause_duration_regression | 12 | 6400 | 0.9607 |
| pause_duration_regression | 13 | 6400 | 0.9574 |
| pause_duration_regression | 14 | 6400 | 0.9573 |
| pause_duration_regression | 15 | 6400 | 0.9545 |
| pause_duration_regression | 16 | 6400 | 0.9512 |
| pause_duration_regression | 17 | 6400 | 0.9559 |
| pause_duration_regression | 18 | 6400 | 0.9551 |
| pause_duration_regression | 19 | 6400 | 0.9585 |
| pause_duration_regression | 20 | 6400 | 0.9552 |
| pause_duration_regression | 21 | 6400 | 0.9541 |
| pause_duration_regression | 22 | 6400 | 0.9603 |
| pause_duration_regression | 23 | 6400 | 0.9619 |
| pause_duration_regression | 24 | 6400 | 0.9620 |
| pause_duration_regression | 25 | 6400 | 0.9650 |
| pause_duration_regression | 26 | 6400 | 0.9608 |
| pause_duration_regression | 27 | 6400 | 0.9610 |
| pause_duration_regression | 28 | 6400 | 0.9564 |
| pause_duration_regression | 29 | 6400 | 0.9606 |
| pause_duration_regression | 30 | 6400 | 0.9571 |
| pause_duration_regression | 31 | 6400 | 0.9551 |
| pause_duration_regression | 32 | 6400 | 0.9502 |


## Encoder MAD
| pause_duration_sec | region | mad_sec |
| --- | --- | --- |
| 0.2000 | inserted_pause | 1.1106 |
| 0.2000 | post_pause_boundary | 1.0802 |
| 0.2000 | pre_pause_boundary | 1.0999 |
| 0.2000 | speech_no_inserted_pause | 1.3003 |
| 0.5000 | inserted_pause | 1.1719 |
| 0.5000 | post_pause_boundary | 1.1658 |
| 0.5000 | pre_pause_boundary | 1.1938 |
| 0.5000 | speech_no_inserted_pause | 1.3995 |
| 1.0000 | inserted_pause | 1.3073 |
| 1.0000 | post_pause_boundary | 1.3310 |
| 1.0000 | pre_pause_boundary | 1.3693 |
| 1.0000 | speech_no_inserted_pause | 1.5696 |
| 2.0000 | inserted_pause | 1.6198 |
| 2.0000 | post_pause_boundary | 1.6838 |
| 2.0000 | pre_pause_boundary | 1.7363 |
| 2.0000 | speech_no_inserted_pause | 1.9136 |

| layer | region | mad_sec |
| --- | --- | --- |
| 0 | inserted_pause | 1.3227 |
| 0 | post_pause_boundary | 1.3350 |
| 0 | pre_pause_boundary | 1.2544 |
| 0 | speech_no_inserted_pause | 1.5091 |
| 1 | inserted_pause | 1.2533 |
| 1 | post_pause_boundary | 1.3295 |
| 1 | pre_pause_boundary | 1.3273 |
| 1 | speech_no_inserted_pause | 1.5727 |
| 2 | inserted_pause | 1.2375 |
| 2 | post_pause_boundary | 1.2421 |
| 2 | pre_pause_boundary | 1.2650 |
| 2 | speech_no_inserted_pause | 1.4807 |
| 3 | inserted_pause | 1.3947 |
| 3 | post_pause_boundary | 1.4088 |
| 3 | pre_pause_boundary | 1.4520 |
| 3 | speech_no_inserted_pause | 1.6959 |
| 4 | inserted_pause | 1.4571 |
| 4 | post_pause_boundary | 1.4183 |
| 4 | pre_pause_boundary | 1.4810 |
| 4 | speech_no_inserted_pause | 1.7225 |
| 5 | inserted_pause | 1.4021 |
| 5 | post_pause_boundary | 1.3800 |
| 5 | pre_pause_boundary | 1.4152 |
| 5 | speech_no_inserted_pause | 1.6277 |
| 6 | inserted_pause | 1.3933 |
| 6 | post_pause_boundary | 1.3763 |
| 6 | pre_pause_boundary | 1.4163 |
| 6 | speech_no_inserted_pause | 1.6596 |
| 7 | inserted_pause | 1.4339 |
| 7 | post_pause_boundary | 1.4163 |
| 7 | pre_pause_boundary | 1.4813 |
| 7 | speech_no_inserted_pause | 1.7102 |
| 8 | inserted_pause | 1.3939 |
| 8 | post_pause_boundary | 1.3906 |
| 8 | pre_pause_boundary | 1.4187 |
| 8 | speech_no_inserted_pause | 1.6432 |
| 9 | inserted_pause | 1.4473 |
| 9 | post_pause_boundary | 1.4382 |
| 9 | pre_pause_boundary | 1.4771 |
| 9 | speech_no_inserted_pause | 1.7144 |
| 10 | inserted_pause | 1.1975 |
| 10 | post_pause_boundary | 1.1793 |
| 10 | pre_pause_boundary | 1.1939 |
| 10 | speech_no_inserted_pause | 1.3948 |
| 11 | inserted_pause | 1.4906 |
| 11 | post_pause_boundary | 1.5096 |
| 11 | pre_pause_boundary | 1.4703 |
| 11 | speech_no_inserted_pause | 1.6827 |
| 12 | inserted_pause | 1.4676 |
| 12 | post_pause_boundary | 1.4558 |
| 12 | pre_pause_boundary | 1.4942 |
| 12 | speech_no_inserted_pause | 1.7106 |
| 13 | inserted_pause | 1.3427 |
| 13 | post_pause_boundary | 1.3542 |
| 13 | pre_pause_boundary | 1.3610 |
| 13 | speech_no_inserted_pause | 1.6039 |
| 14 | inserted_pause | 1.4067 |
| 14 | post_pause_boundary | 1.4278 |
| 14 | pre_pause_boundary | 1.4727 |
| 14 | speech_no_inserted_pause | 1.7101 |
| 15 | inserted_pause | 1.1319 |
| 15 | post_pause_boundary | 1.1487 |
| 15 | pre_pause_boundary | 1.1633 |
| 15 | speech_no_inserted_pause | 1.3568 |
| 16 | inserted_pause | 1.4170 |
| 16 | post_pause_boundary | 1.4016 |
| 16 | pre_pause_boundary | 1.4278 |
| 16 | speech_no_inserted_pause | 1.6345 |
| 17 | inserted_pause | 1.4508 |
| 17 | post_pause_boundary | 1.4115 |
| 17 | pre_pause_boundary | 1.4614 |
| 17 | speech_no_inserted_pause | 1.6948 |
| 18 | inserted_pause | 1.3399 |
| 18 | post_pause_boundary | 1.3587 |
| 18 | pre_pause_boundary | 1.4041 |
| 18 | speech_no_inserted_pause | 1.6548 |
| 19 | inserted_pause | 1.3980 |
| 19 | post_pause_boundary | 1.3827 |
| 19 | pre_pause_boundary | 1.4279 |
| 19 | speech_no_inserted_pause | 1.6519 |
| 20 | inserted_pause | 1.1723 |
| 20 | post_pause_boundary | 1.1629 |
| 20 | pre_pause_boundary | 1.2090 |
| 20 | speech_no_inserted_pause | 1.4169 |
| 21 | inserted_pause | 1.4058 |
| 21 | post_pause_boundary | 1.4034 |
| 21 | pre_pause_boundary | 1.4367 |
| 21 | speech_no_inserted_pause | 1.6796 |
| 22 | inserted_pause | 1.0676 |
| 22 | post_pause_boundary | 1.0673 |
| 22 | pre_pause_boundary | 1.1002 |
| 22 | speech_no_inserted_pause | 1.3037 |
| 23 | inserted_pause | 1.1731 |
| 23 | post_pause_boundary | 1.1212 |
| 23 | pre_pause_boundary | 1.1707 |
| 23 | speech_no_inserted_pause | 1.3021 |
| 24 | inserted_pause | 1.2714 |
| 24 | post_pause_boundary | 1.2175 |
| 24 | pre_pause_boundary | 1.2966 |
| 24 | speech_no_inserted_pause | 1.4311 |
| 25 | inserted_pause | 1.1622 |
| 25 | post_pause_boundary | 1.1440 |
| 25 | pre_pause_boundary | 1.1729 |
| 25 | speech_no_inserted_pause | 1.3584 |
| 26 | inserted_pause | 1.2015 |
| 26 | post_pause_boundary | 1.1109 |
| 26 | pre_pause_boundary | 1.1711 |
| 26 | speech_no_inserted_pause | 1.3146 |
| 27 | inserted_pause | 1.3887 |
| 27 | post_pause_boundary | 1.3559 |
| 27 | pre_pause_boundary | 1.3812 |
| 27 | speech_no_inserted_pause | 1.5826 |
| 28 | inserted_pause | 1.1673 |
| 28 | post_pause_boundary | 1.1329 |
| 28 | pre_pause_boundary | 1.1473 |
| 28 | speech_no_inserted_pause | 1.2974 |
| 29 | inserted_pause | 1.1948 |
| 29 | post_pause_boundary | 1.1354 |
| 29 | pre_pause_boundary | 1.1621 |
| 29 | speech_no_inserted_pause | 1.2358 |
| 30 | inserted_pause | 1.1319 |
| 30 | post_pause_boundary | 1.0691 |
| 30 | pre_pause_boundary | 1.0713 |
| 30 | speech_no_inserted_pause | 1.1527 |
| 31 | inserted_pause | 0.9608 |
| 31 | post_pause_boundary | 0.8218 |
| 31 | pre_pause_boundary | 0.9561 |
| 31 | speech_no_inserted_pause | 0.8666 |


## Cross-attention
| silence_kind | pause_duration_ms | mean_peak_shift_sec | median_peak_shift_sec | mean_abs_shift_error_sec | n |
| --- | --- | --- | --- | --- | --- |
| room_tone | 200 | 0.1922 | 0.2000 | 0.0145 | 1400 |
| room_tone | 500 | 0.4893 | 0.5000 | 0.0195 | 1400 |
| room_tone | 1000 | 0.9805 | 1.0000 | 0.0310 | 1400 |
| room_tone | 2000 | 1.9673 | 2.0000 | 0.0427 | 1400 |
| zero | 200 | 0.1889 | 0.2000 | 0.0172 | 1400 |
| zero | 500 | 0.4859 | 0.5000 | 0.0215 | 1400 |
| zero | 1000 | 0.9736 | 1.0000 | 0.0331 | 1400 |
| zero | 2000 | 1.9669 | 2.0000 | 0.0395 | 1400 |


## Occlusion
| window_region | n | changed_rate | mean_delta_cer | median_delta_cer |
| --- | --- | --- | --- | --- |
| inserted_pause | 899 | 0.1557 | 0.0138 | 0.0000 |
| padding | 900 | 0.0000 | 0.0000 | 0.0000 |
| post_pause_word | 891 | 0.9877 | 0.1683 | 0.1250 |
| pre_pause_word | 900 | 0.9789 | 0.1835 | 0.1304 |
| speech_middle | 900 | 0.6167 | 0.0824 | 0.0465 |


## 考察

## 主要結果の読み取り
認識結果では、pauseを入れても平均CERは大きくは変わらなかった。これは「pauseを入れたら必ず認識が壊れる」という仮説を支持しない。一方で、これは失敗ではない。JSUTは読み上げ音声で発話が明瞭なため、文字起こしだけなら頑健に保たれることが自然だからである。

Linear probeでは、pause/speech分類もboundary分類も非常に高いF1を示した。特に中〜高層で値が高く、pause情報が低層だけの音響特徴として消えるのではなく、上位表現にも読み出せる形で残っていることを示唆する。

Cross-attention peak shiftは非常にきれいで、pause後tokenのpeak shift中央値は200/500/1000/2000ms条件でそれぞれ理想値にほぼ一致した。これは、kotoba-whisper-v2.0のcross-attentionが今回の人工pause条件では時間アライメントとしてかなり信用できることを意味する。

Occlusionでは、pause直前・直後の語をmaskすると転写がほぼ変わった。一方、inserted_pause自体のmaskは変化率が約0.156、平均delta CERは約0.014に留まった。paddingは当然ながら変化なしだった。したがって、認識文字列への直接寄与は語領域が大きく、pauseは転写よりも内部表現・アライメント・境界情報として効いていると考えるのが自然である。


## 考察
今回の結果から、「文字起こしが変わらないからpauseを見ていない」とは言えないことが分かる。認識結果は安定していても、encoder hidden statesにはpause/speechやboundaryが高精度に線形分離可能な形で残り、cross-attention peakもpause長に応じて時間的に移動していた。

これは、ASRモデルが発話内部pauseを入力時間構造の一部として保持している可能性を示す。特に、pause duration回帰のR2が高いことは、単に「pauseかどうか」だけでなく「どれくらい長いpauseか」まで内部表現に含まれていることを示唆する。

zero silenceとroom-tone silenceの差は、少なくとも今回の集計では認識性能やcross-attention shiftに大きな違いとしては出なかった。人工的な完全ゼロ無音と、低エネルギー背景音を含む無音風区間のどちらでも、モデルはpause後tokenの時間ずれを概ね正しく反映していた。

ただし、cross-attentionだけでモデルの挙動を説明しきることはできない。cross-attention peakはアライメントの手がかりとして有用だが、認識結果の変化や内部表現の保持とは別軸である。そのため、本実験のように認識・hidden states・self-attention・cross-attention・occlusionを組み合わせて見ることが重要である。

## 限界
- JSUTは読み上げ音声であり、自然会話に比べて発話が明瞭で、pause挿入に対して認識が壊れにくい。
- post_pause_tail_cer_approxは、発話時刻と文字位置を比例対応させた近似であり、厳密な単語境界評価ではない。
- Linear probeでは一部で収束警告が出た。結果は生成されているが、標準化やmax_iter増加でより厳密にできる。
- 今回は人工的にpauseを挿入しており、実際の言い淀み、息継ぎ、フィラー、文中の意味的境界とは異なる可能性がある。

## 今後の展望
- 文中pauseだけでなく、フィラー（えー、えっと等）を挿入した条件を追加する。
- pause位置を音素・単語・文節境界に合わせ、post-pause語の誤り率をより厳密に測る。
- 強制アライメントを導入し、cross-attention peakと実際の単語境界の対応を定量評価する。
- JSUTだけでなく、自然会話や講義音声など、pauseやフィラーが自然に出るデータでも同じ解析を行う。
- Linear probeに標準化・正則化探索を導入し、層ごとの比較をより厳密にする。


## 生成CSV一覧
| file | rows | cols | size_MB | purpose |
| --- | --- | --- | --- | --- |
| README.md | - | - | 0.0041 | 実験条件・主要結果の短いREADME |
| cross_attention_pause_shift.csv | 19096 | 13 | 2.3855 | 0ms条件を基準にしたtoken別cross-attentio… |
| cross_attention_peaks_teacher_forcing.cs… | 21483 | 21 | 4.3560 | teacher forcing時のdecoder cross-attenti… |
| encoder_mad_pause_regions.csv | 3456000 | 17 | 613.52 | encoder self-attentionのmean attention d… |
| linear_probe_classification.csv | 66 | 5 | 0.0041 | encoder hidden statesからpause/speech・b… |
| linear_probe_duration_regression.csv | 33 | 4 | 0.0017 | encoder hidden statesからpause長を回帰し… |
| manifest_augmented.csv | 900 | 12 | 0.3227 | 900条件の拡張音声マニフェスト |
| manifest_source.csv | 100 | 4 | 0.0174 | 元音声100件とpause挿入時刻の対応表 |
| occlusion.csv | 4490 | 16 | 1.3301 | 各領域をmaskしたときの転写変化・CER変化… |
| occlusion_correlation.csv | 900 | 5 | 0.0740 | 各条件内のattention massとdelta CERのSpe… |
| summary_cross_attention_post_pause_shift… | 8 | 6 | 0.0006 | pause後tokenのcross-attention peak shift… |
| summary_encoder_mad_by_duration_region.c… | 16 | 3 | 0.0007 | encoder MADをpause長/領域で平均した集計… |
| summary_encoder_mad_by_layer_region.csv | 128 | 3 | 0.0051 | encoder MADを層/領域で平均した集計表 |
| summary_occlusion_by_region.csv | 5 | 5 | 0.0003 | occlusion領域ごとの変化率・delta CER集計 |
| summary_recognition_by_condition.csv | 9 | 6 | 0.0006 | pause長/無音種別ごとのCERとexact match集… |
| summary_recognition_edits_by_condition.c… | 9 | 6 | 0.0005 | pause長/無音種別ごとの挿入・削除・置換・… |
| transcriptions.csv | 900 | 17 | 0.2456 | 条件ごとの転写・CER・編集距離系指標 |


## 生成図一覧
| figure | size_px | caption |
| --- | --- | --- |
| cross_peak_shift_kotoba_tech_kotoba_whis… | 1280x720 | cross-attention peak shiftの既存集計図。… |
| examples/cross_attention_example_001_kot… | 1600x640 | 例: BASIC5000_0054の0ms条件におけるcross… |
| examples/cross_attention_example_002_kot… | 1600x640 | 例: BASIC5000_0054の200ms zero silence条… |
| examples/cross_attention_example_003_kot… | 1600x640 | 例: BASIC5000_0054の200ms room-tone sile… |
| internal_pause_cross_attention_post_paus… | 1440x810 | pause後tokenのdecoder cross-attention pe… |
| internal_pause_cross_attention_shift_err… | 1440x810 | pause後tokenのpeak shift誤差。小さいほど… |
| internal_pause_duration_regression_r2_by… | 1440x810 | inserted_pauseフレームのhidden statesか… |
| internal_pause_encoder_mad_by_duration_r… | 1620x900 | pause長ごとのencoder MAD。pauseが長くな… |
| internal_pause_encoder_mad_by_layer_regi… | 1620x900 | encoder self-attentionのmean attention d… |
| internal_pause_linear_probe_f1_by_layer.… | 1440x810 | encoder hidden statesからpause/speechお… |
| internal_pause_occlusion_changed_rate_by… | 1530x810 | 各領域をmaskしたとき転写文字列が変わった… |
| internal_pause_occlusion_delta_cer_by_re… | 1530x810 | 各領域をmaskしたときの平均delta CER。ど… |
| internal_pause_recognition_cer.png | 1440x810 | pause長と無音種別ごとの平均CER。読み上げ… |
| occlusion_attention_vs_delta_cer_kotoba_… | 960x800 | occlusion窓へのcross-attention massとdel… |
