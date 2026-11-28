# XAIの再構成設定選定と追加①〜③

確認日 2026-11-28。10発話での設定選定を完了しました。採用設定で本実験を実行しています。

DeepLIFTとLRPは対象モデルのattention・LayerNorm等の伝播規則が未検証で、未実施です。Grad-CAMとRolloutは時間地図です。絶対IGとの比較は最適化済み設定同士の比較で、保持面積は手法ごとに異なります。

研究サーバ版の図・試聴・メル

## 設定選定のための10発話比較

開発用10発話に白色・交通雑音を各5発話、−5・0・+10 dBで1条件ずつ割り当てました。同じ混合音と生成ASRで候補を比較し、Reazonの発話平均CERを4生成ASRで等重みに集計しました。各手法の全候補でCER・MAEが揃った組を使い、同率のときは波形MAEが小さい方を採用しました。波形MAEはクリーン音声との共通ゲイン・同長波形の平均絶対差です。IGの設定値は有効メルセルの累積寄与率、その他は保持面積率、時間地図では時間区画数の保持率です。OcclusionとSHAPの区画は周波数4×時間8に固定し、乱数シード、特徴量の基準と推論予算も候補間で共通にしました。

採用設定　絶対IG 97%, 正IG 97%, Occlusion 90%, Permutation SHAP 90%, LIME 90%, Saliency 90%, Input × Gradient 90%, SmoothGrad 90%, Grad-CAM 90%, Attention Rollout 90%

| 手法 | 設定 | 選定 | 平均CER | 平均MAE | 有効組 | 順位集計組 | 欠測組 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 絶対IG | 97% | 採用 | 33.39% <meter aria-label="平均CER" min="0" max="1.0" value="0.3339169816504775">33.39%</meter> | 0.03837 <meter aria-label="平均MAE" min="0" max="0.04489191434282966" value="0.038368870173675046">0.03837</meter> | 37 / 40 <meter aria-label="有効組" min="0" max="40" value="37">37 / 40</meter> | 37 | 3 |
| 絶対IG | 95% | — | 36.85% <meter aria-label="平均CER" min="0" max="1.0" value="0.3685311411482687">36.85%</meter> | 0.03664 <meter aria-label="平均MAE" min="0" max="0.04489191434282966" value="0.03664411569622068">0.03664</meter> | 37 / 40 <meter aria-label="有効組" min="0" max="40" value="37">37 / 40</meter> | 37 | 3 |
| 絶対IG | 90% | — | 40.34% <meter aria-label="平均CER" min="0" max="1.0" value="0.4033899449794191">40.34%</meter> | 0.03369 <meter aria-label="平均MAE" min="0" max="0.04489191434282966" value="0.03368994228933146">0.03369</meter> | 37 / 40 <meter aria-label="有効組" min="0" max="40" value="37">37 / 40</meter> | 37 | 3 |
| 絶対IG | 85% | — | 42.79% <meter aria-label="平均CER" min="0" max="1.0" value="0.42787178100269535">42.79%</meter> | 0.03160 <meter aria-label="平均MAE" min="0" max="0.04489191434282966" value="0.03159621500151982">0.03160</meter> | 37 / 40 <meter aria-label="有効組" min="0" max="40" value="37">37 / 40</meter> | 37 | 3 |
| 絶対IG | 80% | — | 45.18% <meter aria-label="平均CER" min="0" max="1.0" value="0.4517590492252017">45.18%</meter> | 0.03004 <meter aria-label="平均MAE" min="0" max="0.04489191434282966" value="0.030040768067257823">0.03004</meter> | 37 / 40 <meter aria-label="有効組" min="0" max="40" value="37">37 / 40</meter> | 37 | 3 |
| 絶対IG | 75% | — | 47.86% <meter aria-label="平均CER" min="0" max="1.0" value="0.4786225467322414">47.86%</meter> | 0.02892 <meter aria-label="平均MAE" min="0" max="0.04489191434282966" value="0.02892361270561542">0.02892</meter> | 37 / 40 <meter aria-label="有効組" min="0" max="40" value="37">37 / 40</meter> | 37 | 3 |
| 絶対IG | 70% | — | 50.54% <meter aria-label="平均CER" min="0" max="1.0" value="0.5053857700872034">50.54%</meter> | 0.02811 <meter aria-label="平均MAE" min="0" max="0.04489191434282966" value="0.02810823897706682">0.02811</meter> | 37 / 40 <meter aria-label="有効組" min="0" max="40" value="37">37 / 40</meter> | 37 | 3 |
| 絶対IG | 60% | — | 57.14% <meter aria-label="平均CER" min="0" max="1.0" value="0.571416012165919">57.14%</meter> | 0.02694 <meter aria-label="平均MAE" min="0" max="0.04489191434282966" value="0.026942443344623347">0.02694</meter> | 37 / 40 <meter aria-label="有効組" min="0" max="40" value="37">37 / 40</meter> | 37 | 3 |
| 絶対IG | 50% | — | 65.05% <meter aria-label="平均CER" min="0" max="1.0" value="0.6505249140847233">65.05%</meter> | 0.02655 <meter aria-label="平均MAE" min="0" max="0.04489191434282966" value="0.026549720736380275">0.02655</meter> | 37 / 40 <meter aria-label="有効組" min="0" max="40" value="37">37 / 40</meter> | 37 | 3 |
| 正IG | 97% | 採用 | 44.06% <meter aria-label="平均CER" min="0" max="1.0" value="0.44057729845341737">44.06%</meter> | 0.02911 <meter aria-label="平均MAE" min="0" max="0.04489191434282966" value="0.02911102329950696">0.02911</meter> | 37 / 40 <meter aria-label="有効組" min="0" max="40" value="37">37 / 40</meter> | 37 | 3 |
| 正IG | 95% | — | 47.24% <meter aria-label="平均CER" min="0" max="1.0" value="0.47240643343781663">47.24%</meter> | 0.02848 <meter aria-label="平均MAE" min="0" max="0.04489191434282966" value="0.028478830099140297">0.02848</meter> | 37 / 40 <meter aria-label="有効組" min="0" max="40" value="37">37 / 40</meter> | 37 | 3 |
| 正IG | 90% | — | 47.02% <meter aria-label="平均CER" min="0" max="1.0" value="0.47024784861975827">47.02%</meter> | 0.02735 <meter aria-label="平均MAE" min="0" max="0.04489191434282966" value="0.027354319680275845">0.02735</meter> | 37 / 40 <meter aria-label="有効組" min="0" max="40" value="37">37 / 40</meter> | 37 | 3 |
| 正IG | 85% | — | 48.28% <meter aria-label="平均CER" min="0" max="1.0" value="0.48279307308306135">48.28%</meter> | 0.02652 <meter aria-label="平均MAE" min="0" max="0.04489191434282966" value="0.02652376586450716">0.02652</meter> | 37 / 40 <meter aria-label="有効組" min="0" max="40" value="37">37 / 40</meter> | 37 | 3 |
| 正IG | 80% | — | 50.08% <meter aria-label="平均CER" min="0" max="1.0" value="0.5008481927831885">50.08%</meter> | 0.02596 <meter aria-label="平均MAE" min="0" max="0.04489191434282966" value="0.02595856557288688">0.02596</meter> | 37 / 40 <meter aria-label="有効組" min="0" max="40" value="37">37 / 40</meter> | 37 | 3 |
| 正IG | 75% | — | 52.36% <meter aria-label="平均CER" min="0" max="1.0" value="0.5236440090464893">52.36%</meter> | 0.02568 <meter aria-label="平均MAE" min="0" max="0.04489191434282966" value="0.02568349475028576">0.02568</meter> | 37 / 40 <meter aria-label="有効組" min="0" max="40" value="37">37 / 40</meter> | 37 | 3 |
| 正IG | 70% | — | 53.96% <meter aria-label="平均CER" min="0" max="1.0" value="0.5396472528011717">53.96%</meter> | 0.02553 <meter aria-label="平均MAE" min="0" max="0.04489191434282966" value="0.025533907954285534">0.02553</meter> | 37 / 40 <meter aria-label="有効組" min="0" max="40" value="37">37 / 40</meter> | 37 | 3 |
| 正IG | 60% | — | 62.62% <meter aria-label="平均CER" min="0" max="1.0" value="0.6261812323917636">62.62%</meter> | 0.02558 <meter aria-label="平均MAE" min="0" max="0.04489191434282966" value="0.025582855807706223">0.02558</meter> | 37 / 40 <meter aria-label="有効組" min="0" max="40" value="37">37 / 40</meter> | 37 | 3 |
| 正IG | 50% | — | 70.48% <meter aria-label="平均CER" min="0" max="1.0" value="0.704838917332963">70.48%</meter> | 0.02603 <meter aria-label="平均MAE" min="0" max="0.04489191434282966" value="0.026027658458506388">0.02603</meter> | 37 / 40 <meter aria-label="有効組" min="0" max="40" value="37">37 / 40</meter> | 37 | 3 |
| Occlusion | 30% | — | 87.61% <meter aria-label="平均CER" min="0" max="1.0" value="0.876109808433511">87.61%</meter> | 0.03477 <meter aria-label="平均MAE" min="0" max="0.04489191434282966" value="0.034765388741515364">0.03477</meter> | 37 / 40 <meter aria-label="有効組" min="0" max="40" value="37">37 / 40</meter> | 37 | 3 |
| Occlusion | 45% | — | 81.22% <meter aria-label="平均CER" min="0" max="1.0" value="0.8121552353511673">81.22%</meter> | 0.03704 <meter aria-label="平均MAE" min="0" max="0.04489191434282966" value="0.03703823954247974">0.03704</meter> | 37 / 40 <meter aria-label="有効組" min="0" max="40" value="37">37 / 40</meter> | 37 | 3 |
| Occlusion | 60% | — | 75.20% <meter aria-label="平均CER" min="0" max="1.0" value="0.7519673431799524">75.20%</meter> | 0.03950 <meter aria-label="平均MAE" min="0" max="0.04489191434282966" value="0.039499644778811814">0.03950</meter> | 37 / 40 <meter aria-label="有効組" min="0" max="40" value="37">37 / 40</meter> | 37 | 3 |
| Occlusion | 75% | — | 57.26% <meter aria-label="平均CER" min="0" max="1.0" value="0.5725938407770516">57.26%</meter> | 0.04263 <meter aria-label="平均MAE" min="0" max="0.04489191434282966" value="0.0426294938754324">0.04263</meter> | 37 / 40 <meter aria-label="有効組" min="0" max="40" value="37">37 / 40</meter> | 37 | 3 |
| Occlusion | 90% | 採用 | 45.29% <meter aria-label="平均CER" min="0" max="1.0" value="0.4528601704653095">45.29%</meter> | 0.04465 <meter aria-label="平均MAE" min="0" max="0.04489191434282966" value="0.04464955477192119">0.04465</meter> | 37 / 40 <meter aria-label="有効組" min="0" max="40" value="37">37 / 40</meter> | 37 | 3 |
| Permutation SHAP | 30% | — | 81.45% <meter aria-label="平均CER" min="0" max="1.0" value="0.8145196237650015">81.45%</meter> | 0.03092 <meter aria-label="平均MAE" min="0" max="0.04489191434282966" value="0.030916109651804323">0.03092</meter> | 37 / 40 <meter aria-label="有効組" min="0" max="40" value="37">37 / 40</meter> | 37 | 3 |
| Permutation SHAP | 45% | — | 74.41% <meter aria-label="平均CER" min="0" max="1.0" value="0.7440582673405697">74.41%</meter> | 0.03393 <meter aria-label="平均MAE" min="0" max="0.04489191434282966" value="0.0339330775065323">0.03393</meter> | 37 / 40 <meter aria-label="有効組" min="0" max="40" value="37">37 / 40</meter> | 37 | 3 |
| Permutation SHAP | 60% | — | 63.62% <meter aria-label="平均CER" min="0" max="1.0" value="0.6361871120895657">63.62%</meter> | 0.03735 <meter aria-label="平均MAE" min="0" max="0.04489191434282966" value="0.03735124758188027">0.03735</meter> | 37 / 40 <meter aria-label="有効組" min="0" max="40" value="37">37 / 40</meter> | 37 | 3 |
| Permutation SHAP | 75% | — | 56.03% <meter aria-label="平均CER" min="0" max="1.0" value="0.5602652005814037">56.03%</meter> | 0.04083 <meter aria-label="平均MAE" min="0" max="0.04489191434282966" value="0.040833379074648485">0.04083</meter> | 37 / 40 <meter aria-label="有効組" min="0" max="40" value="37">37 / 40</meter> | 37 | 3 |
| Permutation SHAP | 90% | 採用 | 42.63% <meter aria-label="平均CER" min="0" max="1.0" value="0.4263284311034471">42.63%</meter> | 0.04427 <meter aria-label="平均MAE" min="0" max="0.04489191434282966" value="0.04427011272598825">0.04427</meter> | 37 / 40 <meter aria-label="有効組" min="0" max="40" value="37">37 / 40</meter> | 37 | 3 |
| LIME | 30% | — | 84.77% <meter aria-label="平均CER" min="0" max="1.0" value="0.8477456186169022">84.77%</meter> | 0.03252 <meter aria-label="平均MAE" min="0" max="0.04489191434282966" value="0.03252490279799056">0.03252</meter> | 37 / 40 <meter aria-label="有効組" min="0" max="40" value="37">37 / 40</meter> | 37 | 3 |
| LIME | 45% | — | 75.53% <meter aria-label="平均CER" min="0" max="1.0" value="0.7552571273889076">75.53%</meter> | 0.03561 <meter aria-label="平均MAE" min="0" max="0.04489191434282966" value="0.03560762037657173">0.03561</meter> | 37 / 40 <meter aria-label="有効組" min="0" max="40" value="37">37 / 40</meter> | 37 | 3 |
| LIME | 60% | — | 69.53% <meter aria-label="平均CER" min="0" max="1.0" value="0.6952763274529179">69.53%</meter> | 0.03760 <meter aria-label="平均MAE" min="0" max="0.04489191434282966" value="0.037596886830444466">0.03760</meter> | 37 / 40 <meter aria-label="有効組" min="0" max="40" value="37">37 / 40</meter> | 37 | 3 |
| LIME | 75% | — | 56.32% <meter aria-label="平均CER" min="0" max="1.0" value="0.5631841664998235">56.32%</meter> | 0.04116 <meter aria-label="平均MAE" min="0" max="0.04489191434282966" value="0.041158544774174466">0.04116</meter> | 37 / 40 <meter aria-label="有効組" min="0" max="40" value="37">37 / 40</meter> | 37 | 3 |
| LIME | 90% | 採用 | 43.52% <meter aria-label="平均CER" min="0" max="1.0" value="0.43523605110138036">43.52%</meter> | 0.04433 <meter aria-label="平均MAE" min="0" max="0.04489191434282966" value="0.04433458279814591">0.04433</meter> | 37 / 40 <meter aria-label="有効組" min="0" max="40" value="37">37 / 40</meter> | 37 | 3 |
| Saliency | 30% | — | 91.63% <meter aria-label="平均CER" min="0" max="1.0" value="0.9162634894967722">91.63%</meter> | 0.03570 <meter aria-label="平均MAE" min="0" max="0.04489191434282966" value="0.035704987501267424">0.03570</meter> | 37 / 40 <meter aria-label="有効組" min="0" max="40" value="37">37 / 40</meter> | 37 | 3 |
| Saliency | 45% | — | 84.03% <meter aria-label="平均CER" min="0" max="1.0" value="0.8403232338929936">84.03%</meter> | 0.03677 <meter aria-label="平均MAE" min="0" max="0.04489191434282966" value="0.036770327658464164">0.03677</meter> | 37 / 40 <meter aria-label="有効組" min="0" max="40" value="37">37 / 40</meter> | 37 | 3 |
| Saliency | 60% | — | 74.25% <meter aria-label="平均CER" min="0" max="1.0" value="0.742492222326275">74.25%</meter> | 0.03789 <meter aria-label="平均MAE" min="0" max="0.04489191434282966" value="0.037887098847666605">0.03789</meter> | 37 / 40 <meter aria-label="有効組" min="0" max="40" value="37">37 / 40</meter> | 37 | 3 |
| Saliency | 75% | — | 61.48% <meter aria-label="平均CER" min="0" max="1.0" value="0.6148087561642283">61.48%</meter> | 0.04072 <meter aria-label="平均MAE" min="0" max="0.04489191434282966" value="0.040717160493117">0.04072</meter> | 37 / 40 <meter aria-label="有効組" min="0" max="40" value="37">37 / 40</meter> | 37 | 3 |
| Saliency | 90% | 採用 | 43.42% <meter aria-label="平均CER" min="0" max="1.0" value="0.4342385271979528">43.42%</meter> | 0.04405 <meter aria-label="平均MAE" min="0" max="0.04489191434282966" value="0.04405449097946942">0.04405</meter> | 37 / 40 <meter aria-label="有効組" min="0" max="40" value="37">37 / 40</meter> | 37 | 3 |
| Input × Gradient | 30% | — | 92.80% <meter aria-label="平均CER" min="0" max="1.0" value="0.9280075227893456">92.80%</meter> | 0.03576 <meter aria-label="平均MAE" min="0" max="0.04489191434282966" value="0.03576327698070074">0.03576</meter> | 37 / 40 <meter aria-label="有効組" min="0" max="40" value="37">37 / 40</meter> | 37 | 3 |
| Input × Gradient | 45% | — | 89.70% <meter aria-label="平均CER" min="0" max="1.0" value="0.896969175764106">89.70%</meter> | 0.03700 <meter aria-label="平均MAE" min="0" max="0.04489191434282966" value="0.03699649638140074">0.03700</meter> | 37 / 40 <meter aria-label="有効組" min="0" max="40" value="37">37 / 40</meter> | 37 | 3 |
| Input × Gradient | 60% | — | 81.26% <meter aria-label="平均CER" min="0" max="1.0" value="0.8126381799847007">81.26%</meter> | 0.03889 <meter aria-label="平均MAE" min="0" max="0.04489191434282966" value="0.0388929582291466">0.03889</meter> | 37 / 40 <meter aria-label="有効組" min="0" max="40" value="37">37 / 40</meter> | 37 | 3 |
| Input × Gradient | 75% | — | 70.25% <meter aria-label="平均CER" min="0" max="1.0" value="0.702463133080234">70.25%</meter> | 0.04191 <meter aria-label="平均MAE" min="0" max="0.04489191434282966" value="0.0419059263258985">0.04191</meter> | 37 / 40 <meter aria-label="有効組" min="0" max="40" value="37">37 / 40</meter> | 37 | 3 |
| Input × Gradient | 90% | 採用 | 50.08% <meter aria-label="平均CER" min="0" max="1.0" value="0.5008207200773004">50.08%</meter> | 0.04489 <meter aria-label="平均MAE" min="0" max="0.04489191434282966" value="0.04489191434282966">0.04489</meter> | 37 / 40 <meter aria-label="有効組" min="0" max="40" value="37">37 / 40</meter> | 37 | 3 |
| SmoothGrad | 30% | — | 92.70% <meter aria-label="平均CER" min="0" max="1.0" value="0.9270237851572704">92.70%</meter> | 0.03497 <meter aria-label="平均MAE" min="0" max="0.04489191434282966" value="0.03497488333507226">0.03497</meter> | 37 / 40 <meter aria-label="有効組" min="0" max="40" value="37">37 / 40</meter> | 37 | 3 |
| SmoothGrad | 45% | — | 84.76% <meter aria-label="平均CER" min="0" max="1.0" value="0.8475907382560329">84.76%</meter> | 0.03702 <meter aria-label="平均MAE" min="0" max="0.04489191434282966" value="0.037017560494574595">0.03702</meter> | 37 / 40 <meter aria-label="有効組" min="0" max="40" value="37">37 / 40</meter> | 37 | 3 |
| SmoothGrad | 60% | — | 75.04% <meter aria-label="平均CER" min="0" max="1.0" value="0.7504198901041532">75.04%</meter> | 0.03767 <meter aria-label="平均MAE" min="0" max="0.04489191434282966" value="0.03767074619800061">0.03767</meter> | 37 / 40 <meter aria-label="有効組" min="0" max="40" value="37">37 / 40</meter> | 37 | 3 |
| SmoothGrad | 75% | — | 64.21% <meter aria-label="平均CER" min="0" max="1.0" value="0.6421406494882758">64.21%</meter> | 0.04028 <meter aria-label="平均MAE" min="0" max="0.04489191434282966" value="0.04028130550145663">0.04028</meter> | 37 / 40 <meter aria-label="有効組" min="0" max="40" value="37">37 / 40</meter> | 37 | 3 |
| SmoothGrad | 90% | 採用 | 42.26% <meter aria-label="平均CER" min="0" max="1.0" value="0.4225883246808092">42.26%</meter> | 0.04330 <meter aria-label="平均MAE" min="0" max="0.04489191434282966" value="0.043295014807797794">0.04330</meter> | 37 / 40 <meter aria-label="有効組" min="0" max="40" value="37">37 / 40</meter> | 37 | 3 |
| Grad-CAM | 30% | — | 94.16% <meter aria-label="平均CER" min="0" max="1.0" value="0.9416065801650041">94.16%</meter> | 0.03583 <meter aria-label="平均MAE" min="0" max="0.04489191434282966" value="0.035830882090831684">0.03583</meter> | 35 / 40 <meter aria-label="有効組" min="0" max="40" value="35">35 / 40</meter> | 35 | 5 |
| Grad-CAM | 45% | — | 86.54% <meter aria-label="平均CER" min="0" max="1.0" value="0.8654078332996572">86.54%</meter> | 0.03734 <meter aria-label="平均MAE" min="0" max="0.04489191434282966" value="0.037340610060386255">0.03734</meter> | 35 / 40 <meter aria-label="有効組" min="0" max="40" value="35">35 / 40</meter> | 35 | 5 |
| Grad-CAM | 60% | — | 77.99% <meter aria-label="平均CER" min="0" max="1.0" value="0.7798820808791237">77.99%</meter> | 0.03859 <meter aria-label="平均MAE" min="0" max="0.04489191434282966" value="0.03859116699188715">0.03859</meter> | 35 / 40 <meter aria-label="有効組" min="0" max="40" value="35">35 / 40</meter> | 35 | 5 |
| Grad-CAM | 75% | — | 57.80% <meter aria-label="平均CER" min="0" max="1.0" value="0.578026301330809">57.80%</meter> | 0.04243 <meter aria-label="平均MAE" min="0" max="0.04489191434282966" value="0.042426461831185855">0.04243</meter> | 35 / 40 <meter aria-label="有効組" min="0" max="40" value="35">35 / 40</meter> | 35 | 5 |
| Grad-CAM | 90% | 採用 | 47.29% <meter aria-label="平均CER" min="0" max="1.0" value="0.47289085796538644">47.29%</meter> | 0.04432 <meter aria-label="平均MAE" min="0" max="0.04489191434282966" value="0.04431949639619088">0.04432</meter> | 35 / 40 <meter aria-label="有効組" min="0" max="40" value="35">35 / 40</meter> | 35 | 5 |
| Attention Rollout | 30% | — | 88.53% <meter aria-label="平均CER" min="0" max="1.0" value="0.8852918259301598">88.53%</meter> | 0.03448 <meter aria-label="平均MAE" min="0" max="0.04489191434282966" value="0.03447553869850817">0.03448</meter> | 37 / 40 <meter aria-label="有効組" min="0" max="40" value="37">37 / 40</meter> | 37 | 3 |
| Attention Rollout | 45% | — | 83.97% <meter aria-label="平均CER" min="0" max="1.0" value="0.8396786658769422">83.97%</meter> | 0.03622 <meter aria-label="平均MAE" min="0" max="0.04489191434282966" value="0.03621537976360122">0.03622</meter> | 37 / 40 <meter aria-label="有効組" min="0" max="40" value="37">37 / 40</meter> | 37 | 3 |
| Attention Rollout | 60% | — | 77.56% <meter aria-label="平均CER" min="0" max="1.0" value="0.7756457197274679">77.56%</meter> | 0.03770 <meter aria-label="平均MAE" min="0" max="0.04489191434282966" value="0.03770105609584079">0.03770</meter> | 37 / 40 <meter aria-label="有効組" min="0" max="40" value="37">37 / 40</meter> | 37 | 3 |
| Attention Rollout | 75% | — | 55.50% <meter aria-label="平均CER" min="0" max="1.0" value="0.5550064542304259">55.50%</meter> | 0.04068 <meter aria-label="平均MAE" min="0" max="0.04489191434282966" value="0.040682083679358605">0.04068</meter> | 37 / 40 <meter aria-label="有効組" min="0" max="40" value="37">37 / 40</meter> | 37 | 3 |
| Attention Rollout | 90% | 採用 | 37.81% <meter aria-label="平均CER" min="0" max="1.0" value="0.37808660624072493">37.81%</meter> | 0.04319 <meter aria-label="平均MAE" min="0" max="0.04489191434282966" value="0.04318649028139499">0.04319</meter> | 37 / 40 <meter aria-label="有効組" min="0" max="40" value="37">37 / 40</meter> | 37 | 3 |

<details>
<summary>生成ASR別の候補成績</summary>

<div class='table-wrap'><table><thead><tr><th>手法</th><th>設定</th><th>生成ASR</th><th>平均CER</th><th>平均MAE</th><th>有効組</th><th>候補共通組</th></tr></thead><tbody>
<tr><td>絶対IG</td><td>97%</td><td>CSJ Transformer</td><td>31.70%</td><td>0.03838</td><td>10</td><td>10</td></tr>
<tr><td>絶対IG</td><td>97%</td><td>CSJ Conformer</td><td>37.39%</td><td>0.04147</td><td>9</td><td>9</td></tr>
<tr><td>絶対IG</td><td>97%</td><td>LaboroTV Conformer</td><td>34.28%</td><td>0.03399</td><td>8</td><td>8</td></tr>
<tr><td>絶対IG</td><td>97%</td><td>Whisper large-v3</td><td>30.20%</td><td>0.03964</td><td>10</td><td>10</td></tr>
<tr><td>絶対IG</td><td>95%</td><td>CSJ Transformer</td><td>39.55%</td><td>0.03690</td><td>10</td><td>10</td></tr>
<tr><td>絶対IG</td><td>95%</td><td>CSJ Conformer</td><td>41.01%</td><td>0.03987</td><td>9</td><td>9</td></tr>
<tr><td>絶対IG</td><td>95%</td><td>LaboroTV Conformer</td><td>33.10%</td><td>0.03203</td><td>8</td><td>8</td></tr>
<tr><td>絶対IG</td><td>95%</td><td>Whisper large-v3</td><td>33.76%</td><td>0.03777</td><td>10</td><td>10</td></tr>
<tr><td>絶対IG</td><td>90%</td><td>CSJ Transformer</td><td>42.65%</td><td>0.03460</td><td>10</td><td>10</td></tr>
<tr><td>絶対IG</td><td>90%</td><td>CSJ Conformer</td><td>46.73%</td><td>0.03706</td><td>9</td><td>9</td></tr>
<tr><td>絶対IG</td><td>90%</td><td>LaboroTV Conformer</td><td>30.83%</td><td>0.02881</td><td>8</td><td>8</td></tr>
<tr><td>絶対IG</td><td>90%</td><td>Whisper large-v3</td><td>41.14%</td><td>0.03429</td><td>10</td><td>10</td></tr>
<tr><td>絶対IG</td><td>85%</td><td>CSJ Transformer</td><td>42.89%</td><td>0.03285</td><td>10</td><td>10</td></tr>
<tr><td>絶対IG</td><td>85%</td><td>CSJ Conformer</td><td>51.48%</td><td>0.03515</td><td>9</td><td>9</td></tr>
<tr><td>絶対IG</td><td>85%</td><td>LaboroTV Conformer</td><td>32.40%</td><td>0.02657</td><td>8</td><td>8</td></tr>
<tr><td>絶対IG</td><td>85%</td><td>Whisper large-v3</td><td>44.38%</td><td>0.03181</td><td>10</td><td>10</td></tr>
<tr><td>絶対IG</td><td>80%</td><td>CSJ Transformer</td><td>49.10%</td><td>0.03166</td><td>10</td><td>10</td></tr>
<tr><td>絶対IG</td><td>80%</td><td>CSJ Conformer</td><td>51.80%</td><td>0.03374</td><td>9</td><td>9</td></tr>
<tr><td>絶対IG</td><td>80%</td><td>LaboroTV Conformer</td><td>34.46%</td><td>0.02503</td><td>8</td><td>8</td></tr>
<tr><td>絶対IG</td><td>80%</td><td>Whisper large-v3</td><td>45.35%</td><td>0.02973</td><td>10</td><td>10</td></tr>
<tr><td>絶対IG</td><td>75%</td><td>CSJ Transformer</td><td>50.06%</td><td>0.03084</td><td>10</td><td>10</td></tr>
<tr><td>絶対IG</td><td>75%</td><td>CSJ Conformer</td><td>52.29%</td><td>0.03266</td><td>9</td><td>9</td></tr>
<tr><td>絶対IG</td><td>75%</td><td>LaboroTV Conformer</td><td>35.95%</td><td>0.02410</td><td>8</td><td>8</td></tr>
<tr><td>絶対IG</td><td>75%</td><td>Whisper large-v3</td><td>53.15%</td><td>0.02809</td><td>10</td><td>10</td></tr>
<tr><td>絶対IG</td><td>70%</td><td>CSJ Transformer</td><td>49.26%</td><td>0.03022</td><td>10</td><td>10</td></tr>
<tr><td>絶対IG</td><td>70%</td><td>CSJ Conformer</td><td>59.30%</td><td>0.03180</td><td>9</td><td>9</td></tr>
<tr><td>絶対IG</td><td>70%</td><td>LaboroTV Conformer</td><td>39.56%</td><td>0.02354</td><td>8</td><td>8</td></tr>
<tr><td>絶対IG</td><td>70%</td><td>Whisper large-v3</td><td>54.04%</td><td>0.02688</td><td>10</td><td>10</td></tr>
<tr><td>絶対IG</td><td>60%</td><td>CSJ Transformer</td><td>56.25%</td><td>0.02944</td><td>10</td><td>10</td></tr>
<tr><td>絶対IG</td><td>60%</td><td>CSJ Conformer</td><td>66.76%</td><td>0.03063</td><td>9</td><td>9</td></tr>
<tr><td>絶対IG</td><td>60%</td><td>LaboroTV Conformer</td><td>47.92%</td><td>0.02286</td><td>8</td><td>8</td></tr>
<tr><td>絶対IG</td><td>60%</td><td>Whisper large-v3</td><td>57.63%</td><td>0.02484</td><td>10</td><td>10</td></tr>
<tr><td>絶対IG</td><td>50%</td><td>CSJ Transformer</td><td>74.99%</td><td>0.02906</td><td>10</td><td>10</td></tr>
<tr><td>絶対IG</td><td>50%</td><td>CSJ Conformer</td><td>65.02%</td><td>0.02993</td><td>9</td><td>9</td></tr>
<tr><td>絶対IG</td><td>50%</td><td>LaboroTV Conformer</td><td>50.02%</td><td>0.02331</td><td>8</td><td>8</td></tr>
<tr><td>絶対IG</td><td>50%</td><td>Whisper large-v3</td><td>70.17%</td><td>0.02389</td><td>10</td><td>10</td></tr>
<tr><td>正IG</td><td>97%</td><td>CSJ Transformer</td><td>41.92%</td><td>0.03024</td><td>10</td><td>10</td></tr>
<tr><td>正IG</td><td>97%</td><td>CSJ Conformer</td><td>55.00%</td><td>0.03079</td><td>9</td><td>9</td></tr>
<tr><td>正IG</td><td>97%</td><td>LaboroTV Conformer</td><td>32.30%</td><td>0.02550</td><td>8</td><td>8</td></tr>
<tr><td>正IG</td><td>97%</td><td>Whisper large-v3</td><td>47.01%</td><td>0.02992</td><td>10</td><td>10</td></tr>
<tr><td>正IG</td><td>95%</td><td>CSJ Transformer</td><td>46.53%</td><td>0.02983</td><td>10</td><td>10</td></tr>
<tr><td>正IG</td><td>95%</td><td>CSJ Conformer</td><td>64.22%</td><td>0.03043</td><td>9</td><td>9</td></tr>
<tr><td>正IG</td><td>95%</td><td>LaboroTV Conformer</td><td>32.05%</td><td>0.02474</td><td>8</td><td>8</td></tr>
<tr><td>正IG</td><td>95%</td><td>Whisper large-v3</td><td>46.17%</td><td>0.02891</td><td>10</td><td>10</td></tr>
<tr><td>正IG</td><td>90%</td><td>CSJ Transformer</td><td>44.84%</td><td>0.02923</td><td>10</td><td>10</td></tr>
<tr><td>正IG</td><td>90%</td><td>CSJ Conformer</td><td>60.09%</td><td>0.02959</td><td>9</td><td>9</td></tr>
<tr><td>正IG</td><td>90%</td><td>LaboroTV Conformer</td><td>35.43%</td><td>0.02355</td><td>8</td><td>8</td></tr>
<tr><td>正IG</td><td>90%</td><td>Whisper large-v3</td><td>47.74%</td><td>0.02704</td><td>10</td><td>10</td></tr>
<tr><td>正IG</td><td>85%</td><td>CSJ Transformer</td><td>45.95%</td><td>0.02863</td><td>10</td><td>10</td></tr>
<tr><td>正IG</td><td>85%</td><td>CSJ Conformer</td><td>63.09%</td><td>0.02901</td><td>9</td><td>9</td></tr>
<tr><td>正IG</td><td>85%</td><td>LaboroTV Conformer</td><td>36.54%</td><td>0.02283</td><td>8</td><td>8</td></tr>
<tr><td>正IG</td><td>85%</td><td>Whisper large-v3</td><td>47.55%</td><td>0.02563</td><td>10</td><td>10</td></tr>
<tr><td>正IG</td><td>80%</td><td>CSJ Transformer</td><td>52.92%</td><td>0.02825</td><td>10</td><td>10</td></tr>
<tr><td>正IG</td><td>80%</td><td>CSJ Conformer</td><td>65.10%</td><td>0.02868</td><td>9</td><td>9</td></tr>
<tr><td>正IG</td><td>80%</td><td>LaboroTV Conformer</td><td>35.27%</td><td>0.02230</td><td>8</td><td>8</td></tr>
<tr><td>正IG</td><td>80%</td><td>Whisper large-v3</td><td>47.05%</td><td>0.02461</td><td>10</td><td>10</td></tr>
<tr><td>正IG</td><td>75%</td><td>CSJ Transformer</td><td>50.57%</td><td>0.02805</td><td>10</td><td>10</td></tr>
<tr><td>正IG</td><td>75%</td><td>CSJ Conformer</td><td>66.77%</td><td>0.02855</td><td>9</td><td>9</td></tr>
<tr><td>正IG</td><td>75%</td><td>LaboroTV Conformer</td><td>42.30%</td><td>0.02225</td><td>8</td><td>8</td></tr>
<tr><td>正IG</td><td>75%</td><td>Whisper large-v3</td><td>49.83%</td><td>0.02389</td><td>10</td><td>10</td></tr>
<tr><td>正IG</td><td>70%</td><td>CSJ Transformer</td><td>57.66%</td><td>0.02802</td><td>10</td><td>10</td></tr>
<tr><td>正IG</td><td>70%</td><td>CSJ Conformer</td><td>64.07%</td><td>0.02850</td><td>9</td><td>9</td></tr>
<tr><td>正IG</td><td>70%</td><td>LaboroTV Conformer</td><td>42.20%</td><td>0.02227</td><td>8</td><td>8</td></tr>
<tr><td>正IG</td><td>70%</td><td>Whisper large-v3</td><td>51.93%</td><td>0.02334</td><td>10</td><td>10</td></tr>
<tr><td>正IG</td><td>60%</td><td>CSJ Transformer</td><td>64.40%</td><td>0.02809</td><td>10</td><td>10</td></tr>
<tr><td>正IG</td><td>60%</td><td>CSJ Conformer</td><td>72.15%</td><td>0.02849</td><td>9</td><td>9</td></tr>
<tr><td>正IG</td><td>60%</td><td>LaboroTV Conformer</td><td>50.29%</td><td>0.02292</td><td>8</td><td>8</td></tr>
<tr><td>正IG</td><td>60%</td><td>Whisper large-v3</td><td>63.63%</td><td>0.02283</td><td>10</td><td>10</td></tr>
<tr><td>正IG</td><td>50%</td><td>CSJ Transformer</td><td>78.06%</td><td>0.02832</td><td>10</td><td>10</td></tr>
<tr><td>正IG</td><td>50%</td><td>CSJ Conformer</td><td>72.08%</td><td>0.02870</td><td>9</td><td>9</td></tr>
<tr><td>正IG</td><td>50%</td><td>LaboroTV Conformer</td><td>57.71%</td><td>0.02384</td><td>8</td><td>8</td></tr>
<tr><td>正IG</td><td>50%</td><td>Whisper large-v3</td><td>74.09%</td><td>0.02325</td><td>10</td><td>10</td></tr>
<tr><td>Occlusion</td><td>30%</td><td>CSJ Transformer</td><td>90.70%</td><td>0.03354</td><td>10</td><td>10</td></tr>
<tr><td>Occlusion</td><td>30%</td><td>CSJ Conformer</td><td>92.16%</td><td>0.04130</td><td>9</td><td>9</td></tr>
<tr><td>Occlusion</td><td>30%</td><td>LaboroTV Conformer</td><td>81.97%</td><td>0.03429</td><td>8</td><td>8</td></tr>
<tr><td>Occlusion</td><td>30%</td><td>Whisper large-v3</td><td>85.61%</td><td>0.02993</td><td>10</td><td>10</td></tr>
<tr><td>Occlusion</td><td>45%</td><td>CSJ Transformer</td><td>85.49%</td><td>0.03532</td><td>10</td><td>10</td></tr>
<tr><td>Occlusion</td><td>45%</td><td>CSJ Conformer</td><td>86.77%</td><td>0.04424</td><td>9</td><td>9</td></tr>
<tr><td>Occlusion</td><td>45%</td><td>LaboroTV Conformer</td><td>80.38%</td><td>0.03550</td><td>8</td><td>8</td></tr>
<tr><td>Occlusion</td><td>45%</td><td>Whisper large-v3</td><td>72.22%</td><td>0.03310</td><td>10</td><td>10</td></tr>
<tr><td>Occlusion</td><td>60%</td><td>CSJ Transformer</td><td>74.14%</td><td>0.03759</td><td>10</td><td>10</td></tr>
<tr><td>Occlusion</td><td>60%</td><td>CSJ Conformer</td><td>79.52%</td><td>0.04542</td><td>9</td><td>9</td></tr>
<tr><td>Occlusion</td><td>60%</td><td>LaboroTV Conformer</td><td>74.72%</td><td>0.03744</td><td>8</td><td>8</td></tr>
<tr><td>Occlusion</td><td>60%</td><td>Whisper large-v3</td><td>72.41%</td><td>0.03755</td><td>10</td><td>10</td></tr>
<tr><td>Occlusion</td><td>75%</td><td>CSJ Transformer</td><td>57.08%</td><td>0.04138</td><td>10</td><td>10</td></tr>
<tr><td>Occlusion</td><td>75%</td><td>CSJ Conformer</td><td>58.69%</td><td>0.04710</td><td>9</td><td>9</td></tr>
<tr><td>Occlusion</td><td>75%</td><td>LaboroTV Conformer</td><td>63.48%</td><td>0.04063</td><td>8</td><td>8</td></tr>
<tr><td>Occlusion</td><td>75%</td><td>Whisper large-v3</td><td>49.79%</td><td>0.04142</td><td>10</td><td>10</td></tr>
<tr><td>Occlusion</td><td>90%</td><td>CSJ Transformer</td><td>41.85%</td><td>0.04438</td><td>10</td><td>10</td></tr>
<tr><td>Occlusion</td><td>90%</td><td>CSJ Conformer</td><td>46.09%</td><td>0.04789</td><td>9</td><td>9</td></tr>
<tr><td>Occlusion</td><td>90%</td><td>LaboroTV Conformer</td><td>46.76%</td><td>0.04180</td><td>8</td><td>8</td></tr>
<tr><td>Occlusion</td><td>90%</td><td>Whisper large-v3</td><td>46.45%</td><td>0.04453</td><td>10</td><td>10</td></tr>
<tr><td>Permutation SHAP</td><td>30%</td><td>CSJ Transformer</td><td>80.75%</td><td>0.02842</td><td>10</td><td>10</td></tr>
<tr><td>Permutation SHAP</td><td>30%</td><td>CSJ Conformer</td><td>82.39%</td><td>0.03349</td><td>9</td><td>9</td></tr>
<tr><td>Permutation SHAP</td><td>30%</td><td>LaboroTV Conformer</td><td>85.36%</td><td>0.03203</td><td>8</td><td>8</td></tr>
<tr><td>Permutation SHAP</td><td>30%</td><td>Whisper large-v3</td><td>77.31%</td><td>0.02972</td><td>10</td><td>10</td></tr>
<tr><td>Permutation SHAP</td><td>45%</td><td>CSJ Transformer</td><td>69.07%</td><td>0.03078</td><td>10</td><td>10</td></tr>
<tr><td>Permutation SHAP</td><td>45%</td><td>CSJ Conformer</td><td>76.51%</td><td>0.03633</td><td>9</td><td>9</td></tr>
<tr><td>Permutation SHAP</td><td>45%</td><td>LaboroTV Conformer</td><td>76.62%</td><td>0.03461</td><td>8</td><td>8</td></tr>
<tr><td>Permutation SHAP</td><td>45%</td><td>Whisper large-v3</td><td>75.43%</td><td>0.03402</td><td>10</td><td>10</td></tr>
<tr><td>Permutation SHAP</td><td>60%</td><td>CSJ Transformer</td><td>61.27%</td><td>0.03506</td><td>10</td><td>10</td></tr>
<tr><td>Permutation SHAP</td><td>60%</td><td>CSJ Conformer</td><td>66.01%</td><td>0.03933</td><td>9</td><td>9</td></tr>
<tr><td>Permutation SHAP</td><td>60%</td><td>LaboroTV Conformer</td><td>59.70%</td><td>0.03669</td><td>8</td><td>8</td></tr>
<tr><td>Permutation SHAP</td><td>60%</td><td>Whisper large-v3</td><td>67.50%</td><td>0.03833</td><td>10</td><td>10</td></tr>
<tr><td>Permutation SHAP</td><td>75%</td><td>CSJ Transformer</td><td>52.75%</td><td>0.04002</td><td>10</td><td>10</td></tr>
<tr><td>Permutation SHAP</td><td>75%</td><td>CSJ Conformer</td><td>55.65%</td><td>0.04347</td><td>9</td><td>9</td></tr>
<tr><td>Permutation SHAP</td><td>75%</td><td>LaboroTV Conformer</td><td>56.13%</td><td>0.03941</td><td>8</td><td>8</td></tr>
<tr><td>Permutation SHAP</td><td>75%</td><td>Whisper large-v3</td><td>59.58%</td><td>0.04044</td><td>10</td><td>10</td></tr>
<tr><td>Permutation SHAP</td><td>90%</td><td>CSJ Transformer</td><td>42.12%</td><td>0.04359</td><td>10</td><td>10</td></tr>
<tr><td>Permutation SHAP</td><td>90%</td><td>CSJ Conformer</td><td>41.94%</td><td>0.04702</td><td>9</td><td>9</td></tr>
<tr><td>Permutation SHAP</td><td>90%</td><td>LaboroTV Conformer</td><td>47.87%</td><td>0.04247</td><td>8</td><td>8</td></tr>
<tr><td>Permutation SHAP</td><td>90%</td><td>Whisper large-v3</td><td>38.61%</td><td>0.04400</td><td>10</td><td>10</td></tr>
<tr><td>LIME</td><td>30%</td><td>CSJ Transformer</td><td>87.72%</td><td>0.03191</td><td>10</td><td>10</td></tr>
<tr><td>LIME</td><td>30%</td><td>CSJ Conformer</td><td>89.24%</td><td>0.03708</td><td>9</td><td>9</td></tr>
<tr><td>LIME</td><td>30%</td><td>LaboroTV Conformer</td><td>85.19%</td><td>0.03172</td><td>8</td><td>8</td></tr>
<tr><td>LIME</td><td>30%</td><td>Whisper large-v3</td><td>76.94%</td><td>0.02939</td><td>10</td><td>10</td></tr>
<tr><td>LIME</td><td>45%</td><td>CSJ Transformer</td><td>72.45%</td><td>0.03461</td><td>10</td><td>10</td></tr>
<tr><td>LIME</td><td>45%</td><td>CSJ Conformer</td><td>77.83%</td><td>0.03910</td><td>9</td><td>9</td></tr>
<tr><td>LIME</td><td>45%</td><td>LaboroTV Conformer</td><td>74.79%</td><td>0.03483</td><td>8</td><td>8</td></tr>
<tr><td>LIME</td><td>45%</td><td>Whisper large-v3</td><td>77.04%</td><td>0.03389</td><td>10</td><td>10</td></tr>
<tr><td>LIME</td><td>60%</td><td>CSJ Transformer</td><td>63.32%</td><td>0.03634</td><td>10</td><td>10</td></tr>
<tr><td>LIME</td><td>60%</td><td>CSJ Conformer</td><td>73.52%</td><td>0.04014</td><td>9</td><td>9</td></tr>
<tr><td>LIME</td><td>60%</td><td>LaboroTV Conformer</td><td>69.21%</td><td>0.03716</td><td>8</td><td>8</td></tr>
<tr><td>LIME</td><td>60%</td><td>Whisper large-v3</td><td>72.06%</td><td>0.03675</td><td>10</td><td>10</td></tr>
<tr><td>LIME</td><td>75%</td><td>CSJ Transformer</td><td>49.74%</td><td>0.04068</td><td>10</td><td>10</td></tr>
<tr><td>LIME</td><td>75%</td><td>CSJ Conformer</td><td>64.87%</td><td>0.04303</td><td>9</td><td>9</td></tr>
<tr><td>LIME</td><td>75%</td><td>LaboroTV Conformer</td><td>52.91%</td><td>0.03944</td><td>8</td><td>8</td></tr>
<tr><td>LIME</td><td>75%</td><td>Whisper large-v3</td><td>57.76%</td><td>0.04148</td><td>10</td><td>10</td></tr>
<tr><td>LIME</td><td>90%</td><td>CSJ Transformer</td><td>38.29%</td><td>0.04424</td><td>10</td><td>10</td></tr>
<tr><td>LIME</td><td>90%</td><td>CSJ Conformer</td><td>47.99%</td><td>0.04739</td><td>9</td><td>9</td></tr>
<tr><td>LIME</td><td>90%</td><td>LaboroTV Conformer</td><td>40.97%</td><td>0.04149</td><td>8</td><td>8</td></tr>
<tr><td>LIME</td><td>90%</td><td>Whisper large-v3</td><td>46.84%</td><td>0.04421</td><td>10</td><td>10</td></tr>
<tr><td>Saliency</td><td>30%</td><td>CSJ Transformer</td><td>90.73%</td><td>0.03385</td><td>10</td><td>10</td></tr>
<tr><td>Saliency</td><td>30%</td><td>CSJ Conformer</td><td>88.99%</td><td>0.03427</td><td>9</td><td>9</td></tr>
<tr><td>Saliency</td><td>30%</td><td>LaboroTV Conformer</td><td>90.64%</td><td>0.03807</td><td>8</td><td>8</td></tr>
<tr><td>Saliency</td><td>30%</td><td>Whisper large-v3</td><td>96.15%</td><td>0.03663</td><td>10</td><td>10</td></tr>
<tr><td>Saliency</td><td>45%</td><td>CSJ Transformer</td><td>83.53%</td><td>0.03470</td><td>10</td><td>10</td></tr>
<tr><td>Saliency</td><td>45%</td><td>CSJ Conformer</td><td>85.27%</td><td>0.03689</td><td>9</td><td>9</td></tr>
<tr><td>Saliency</td><td>45%</td><td>LaboroTV Conformer</td><td>82.30%</td><td>0.03797</td><td>8</td><td>8</td></tr>
<tr><td>Saliency</td><td>45%</td><td>Whisper large-v3</td><td>85.03%</td><td>0.03752</td><td>10</td><td>10</td></tr>
<tr><td>Saliency</td><td>60%</td><td>CSJ Transformer</td><td>71.74%</td><td>0.03595</td><td>10</td><td>10</td></tr>
<tr><td>Saliency</td><td>60%</td><td>CSJ Conformer</td><td>76.46%</td><td>0.03808</td><td>9</td><td>9</td></tr>
<tr><td>Saliency</td><td>60%</td><td>LaboroTV Conformer</td><td>72.93%</td><td>0.03950</td><td>8</td><td>8</td></tr>
<tr><td>Saliency</td><td>60%</td><td>Whisper large-v3</td><td>75.87%</td><td>0.03801</td><td>10</td><td>10</td></tr>
<tr><td>Saliency</td><td>75%</td><td>CSJ Transformer</td><td>64.03%</td><td>0.03971</td><td>10</td><td>10</td></tr>
<tr><td>Saliency</td><td>75%</td><td>CSJ Conformer</td><td>62.44%</td><td>0.04091</td><td>9</td><td>9</td></tr>
<tr><td>Saliency</td><td>75%</td><td>LaboroTV Conformer</td><td>61.63%</td><td>0.04044</td><td>8</td><td>8</td></tr>
<tr><td>Saliency</td><td>75%</td><td>Whisper large-v3</td><td>57.83%</td><td>0.04181</td><td>10</td><td>10</td></tr>
<tr><td>Saliency</td><td>90%</td><td>CSJ Transformer</td><td>44.26%</td><td>0.04265</td><td>10</td><td>10</td></tr>
<tr><td>Saliency</td><td>90%</td><td>CSJ Conformer</td><td>47.09%</td><td>0.04681</td><td>9</td><td>9</td></tr>
<tr><td>Saliency</td><td>90%</td><td>LaboroTV Conformer</td><td>46.51%</td><td>0.04186</td><td>8</td><td>8</td></tr>
<tr><td>Saliency</td><td>90%</td><td>Whisper large-v3</td><td>35.84%</td><td>0.04489</td><td>10</td><td>10</td></tr>
<tr><td>Input × Gradient</td><td>30%</td><td>CSJ Transformer</td><td>92.65%</td><td>0.03455</td><td>10</td><td>10</td></tr>
<tr><td>Input × Gradient</td><td>30%</td><td>CSJ Conformer</td><td>93.36%</td><td>0.03578</td><td>9</td><td>9</td></tr>
<tr><td>Input × Gradient</td><td>30%</td><td>LaboroTV Conformer</td><td>97.27%</td><td>0.03747</td><td>8</td><td>8</td></tr>
<tr><td>Input × Gradient</td><td>30%</td><td>Whisper large-v3</td><td>87.92%</td><td>0.03525</td><td>10</td><td>10</td></tr>
<tr><td>Input × Gradient</td><td>45%</td><td>CSJ Transformer</td><td>89.93%</td><td>0.03638</td><td>10</td><td>10</td></tr>
<tr><td>Input × Gradient</td><td>45%</td><td>CSJ Conformer</td><td>87.63%</td><td>0.03531</td><td>9</td><td>9</td></tr>
<tr><td>Input × Gradient</td><td>45%</td><td>LaboroTV Conformer</td><td>93.90%</td><td>0.03957</td><td>8</td><td>8</td></tr>
<tr><td>Input × Gradient</td><td>45%</td><td>Whisper large-v3</td><td>87.32%</td><td>0.03673</td><td>10</td><td>10</td></tr>
<tr><td>Input × Gradient</td><td>60%</td><td>CSJ Transformer</td><td>80.52%</td><td>0.03673</td><td>10</td><td>10</td></tr>
<tr><td>Input × Gradient</td><td>60%</td><td>CSJ Conformer</td><td>82.61%</td><td>0.03839</td><td>9</td><td>9</td></tr>
<tr><td>Input × Gradient</td><td>60%</td><td>LaboroTV Conformer</td><td>91.78%</td><td>0.04113</td><td>8</td><td>8</td></tr>
<tr><td>Input × Gradient</td><td>60%</td><td>Whisper large-v3</td><td>70.15%</td><td>0.03933</td><td>10</td><td>10</td></tr>
<tr><td>Input × Gradient</td><td>75%</td><td>CSJ Transformer</td><td>69.94%</td><td>0.03955</td><td>10</td><td>10</td></tr>
<tr><td>Input × Gradient</td><td>75%</td><td>CSJ Conformer</td><td>75.13%</td><td>0.04234</td><td>9</td><td>9</td></tr>
<tr><td>Input × Gradient</td><td>75%</td><td>LaboroTV Conformer</td><td>74.05%</td><td>0.04395</td><td>8</td><td>8</td></tr>
<tr><td>Input × Gradient</td><td>75%</td><td>Whisper large-v3</td><td>61.87%</td><td>0.04179</td><td>10</td><td>10</td></tr>
<tr><td>Input × Gradient</td><td>90%</td><td>CSJ Transformer</td><td>48.10%</td><td>0.04396</td><td>10</td><td>10</td></tr>
<tr><td>Input × Gradient</td><td>90%</td><td>CSJ Conformer</td><td>53.70%</td><td>0.04615</td><td>9</td><td>9</td></tr>
<tr><td>Input × Gradient</td><td>90%</td><td>LaboroTV Conformer</td><td>59.44%</td><td>0.04462</td><td>8</td><td>8</td></tr>
<tr><td>Input × Gradient</td><td>90%</td><td>Whisper large-v3</td><td>39.09%</td><td>0.04484</td><td>10</td><td>10</td></tr>
<tr><td>SmoothGrad</td><td>30%</td><td>CSJ Transformer</td><td>92.19%</td><td>0.03274</td><td>10</td><td>10</td></tr>
<tr><td>SmoothGrad</td><td>30%</td><td>CSJ Conformer</td><td>90.62%</td><td>0.03389</td><td>9</td><td>9</td></tr>
<tr><td>SmoothGrad</td><td>30%</td><td>LaboroTV Conformer</td><td>91.83%</td><td>0.03762</td><td>8</td><td>8</td></tr>
<tr><td>SmoothGrad</td><td>30%</td><td>Whisper large-v3</td><td>96.18%</td><td>0.03564</td><td>10</td><td>10</td></tr>
<tr><td>SmoothGrad</td><td>45%</td><td>CSJ Transformer</td><td>79.53%</td><td>0.03510</td><td>10</td><td>10</td></tr>
<tr><td>SmoothGrad</td><td>45%</td><td>CSJ Conformer</td><td>87.40%</td><td>0.03741</td><td>9</td><td>9</td></tr>
<tr><td>SmoothGrad</td><td>45%</td><td>LaboroTV Conformer</td><td>87.99%</td><td>0.03813</td><td>8</td><td>8</td></tr>
<tr><td>SmoothGrad</td><td>45%</td><td>Whisper large-v3</td><td>84.11%</td><td>0.03743</td><td>10</td><td>10</td></tr>
<tr><td>SmoothGrad</td><td>60%</td><td>CSJ Transformer</td><td>68.45%</td><td>0.03561</td><td>10</td><td>10</td></tr>
<tr><td>SmoothGrad</td><td>60%</td><td>CSJ Conformer</td><td>76.28%</td><td>0.03761</td><td>9</td><td>9</td></tr>
<tr><td>SmoothGrad</td><td>60%</td><td>LaboroTV Conformer</td><td>84.36%</td><td>0.03868</td><td>8</td><td>8</td></tr>
<tr><td>SmoothGrad</td><td>60%</td><td>Whisper large-v3</td><td>71.07%</td><td>0.03878</td><td>10</td><td>10</td></tr>
<tr><td>SmoothGrad</td><td>75%</td><td>CSJ Transformer</td><td>64.88%</td><td>0.03992</td><td>10</td><td>10</td></tr>
<tr><td>SmoothGrad</td><td>75%</td><td>CSJ Conformer</td><td>65.12%</td><td>0.04060</td><td>9</td><td>9</td></tr>
<tr><td>SmoothGrad</td><td>75%</td><td>LaboroTV Conformer</td><td>69.06%</td><td>0.03893</td><td>8</td><td>8</td></tr>
<tr><td>SmoothGrad</td><td>75%</td><td>Whisper large-v3</td><td>57.80%</td><td>0.04168</td><td>10</td><td>10</td></tr>
<tr><td>SmoothGrad</td><td>90%</td><td>CSJ Transformer</td><td>42.43%</td><td>0.04178</td><td>10</td><td>10</td></tr>
<tr><td>SmoothGrad</td><td>90%</td><td>CSJ Conformer</td><td>45.95%</td><td>0.04520</td><td>9</td><td>9</td></tr>
<tr><td>SmoothGrad</td><td>90%</td><td>LaboroTV Conformer</td><td>44.82%</td><td>0.04117</td><td>8</td><td>8</td></tr>
<tr><td>SmoothGrad</td><td>90%</td><td>Whisper large-v3</td><td>35.84%</td><td>0.04503</td><td>10</td><td>10</td></tr>
<tr><td>Grad-CAM</td><td>30%</td><td>CSJ Transformer</td><td>95.63%</td><td>0.03542</td><td>10</td><td>10</td></tr>
<tr><td>Grad-CAM</td><td>30%</td><td>CSJ Conformer</td><td>90.14%</td><td>0.03676</td><td>8</td><td>8</td></tr>
<tr><td>Grad-CAM</td><td>30%</td><td>LaboroTV Conformer</td><td>95.23%</td><td>0.03728</td><td>7</td><td>7</td></tr>
<tr><td>Grad-CAM</td><td>30%</td><td>Whisper large-v3</td><td>95.64%</td><td>0.03387</td><td>10</td><td>10</td></tr>
<tr><td>Grad-CAM</td><td>45%</td><td>CSJ Transformer</td><td>89.68%</td><td>0.03701</td><td>10</td><td>10</td></tr>
<tr><td>Grad-CAM</td><td>45%</td><td>CSJ Conformer</td><td>85.95%</td><td>0.03898</td><td>8</td><td>8</td></tr>
<tr><td>Grad-CAM</td><td>45%</td><td>LaboroTV Conformer</td><td>88.63%</td><td>0.03820</td><td>7</td><td>7</td></tr>
<tr><td>Grad-CAM</td><td>45%</td><td>Whisper large-v3</td><td>81.90%</td><td>0.03518</td><td>10</td><td>10</td></tr>
<tr><td>Grad-CAM</td><td>60%</td><td>CSJ Transformer</td><td>81.64%</td><td>0.03899</td><td>10</td><td>10</td></tr>
<tr><td>Grad-CAM</td><td>60%</td><td>CSJ Conformer</td><td>77.96%</td><td>0.04026</td><td>8</td><td>8</td></tr>
<tr><td>Grad-CAM</td><td>60%</td><td>LaboroTV Conformer</td><td>82.83%</td><td>0.03847</td><td>7</td><td>7</td></tr>
<tr><td>Grad-CAM</td><td>60%</td><td>Whisper large-v3</td><td>69.52%</td><td>0.03664</td><td>10</td><td>10</td></tr>
<tr><td>Grad-CAM</td><td>75%</td><td>CSJ Transformer</td><td>54.73%</td><td>0.04278</td><td>10</td><td>10</td></tr>
<tr><td>Grad-CAM</td><td>75%</td><td>CSJ Conformer</td><td>57.97%</td><td>0.04377</td><td>8</td><td>8</td></tr>
<tr><td>Grad-CAM</td><td>75%</td><td>LaboroTV Conformer</td><td>60.59%</td><td>0.04239</td><td>7</td><td>7</td></tr>
<tr><td>Grad-CAM</td><td>75%</td><td>Whisper large-v3</td><td>57.92%</td><td>0.04077</td><td>10</td><td>10</td></tr>
<tr><td>Grad-CAM</td><td>90%</td><td>CSJ Transformer</td><td>50.08%</td><td>0.04458</td><td>10</td><td>10</td></tr>
<tr><td>Grad-CAM</td><td>90%</td><td>CSJ Conformer</td><td>47.72%</td><td>0.04539</td><td>8</td><td>8</td></tr>
<tr><td>Grad-CAM</td><td>90%</td><td>LaboroTV Conformer</td><td>47.69%</td><td>0.04351</td><td>7</td><td>7</td></tr>
<tr><td>Grad-CAM</td><td>90%</td><td>Whisper large-v3</td><td>43.67%</td><td>0.04379</td><td>10</td><td>10</td></tr>
<tr><td>Attention Rollout</td><td>30%</td><td>CSJ Transformer</td><td>86.51%</td><td>0.03565</td><td>10</td><td>10</td></tr>
<tr><td>Attention Rollout</td><td>30%</td><td>CSJ Conformer</td><td>90.57%</td><td>0.03620</td><td>9</td><td>9</td></tr>
<tr><td>Attention Rollout</td><td>30%</td><td>LaboroTV Conformer</td><td>88.60%</td><td>0.03172</td><td>8</td><td>8</td></tr>
<tr><td>Attention Rollout</td><td>30%</td><td>Whisper large-v3</td><td>88.43%</td><td>0.03433</td><td>10</td><td>10</td></tr>
<tr><td>Attention Rollout</td><td>45%</td><td>CSJ Transformer</td><td>84.48%</td><td>0.03807</td><td>10</td><td>10</td></tr>
<tr><td>Attention Rollout</td><td>45%</td><td>CSJ Conformer</td><td>86.22%</td><td>0.03804</td><td>9</td><td>9</td></tr>
<tr><td>Attention Rollout</td><td>45%</td><td>LaboroTV Conformer</td><td>85.77%</td><td>0.03260</td><td>8</td><td>8</td></tr>
<tr><td>Attention Rollout</td><td>45%</td><td>Whisper large-v3</td><td>79.41%</td><td>0.03616</td><td>10</td><td>10</td></tr>
<tr><td>Attention Rollout</td><td>60%</td><td>CSJ Transformer</td><td>74.21%</td><td>0.03866</td><td>10</td><td>10</td></tr>
<tr><td>Attention Rollout</td><td>60%</td><td>CSJ Conformer</td><td>83.78%</td><td>0.04047</td><td>9</td><td>9</td></tr>
<tr><td>Attention Rollout</td><td>60%</td><td>LaboroTV Conformer</td><td>78.97%</td><td>0.03412</td><td>8</td><td>8</td></tr>
<tr><td>Attention Rollout</td><td>60%</td><td>Whisper large-v3</td><td>73.30%</td><td>0.03754</td><td>10</td><td>10</td></tr>
<tr><td>Attention Rollout</td><td>75%</td><td>CSJ Transformer</td><td>60.94%</td><td>0.04090</td><td>10</td><td>10</td></tr>
<tr><td>Attention Rollout</td><td>75%</td><td>CSJ Conformer</td><td>53.27%</td><td>0.04359</td><td>9</td><td>9</td></tr>
<tr><td>Attention Rollout</td><td>75%</td><td>LaboroTV Conformer</td><td>53.67%</td><td>0.03811</td><td>8</td><td>8</td></tr>
<tr><td>Attention Rollout</td><td>75%</td><td>Whisper large-v3</td><td>54.12%</td><td>0.04013</td><td>10</td><td>10</td></tr>
<tr><td>Attention Rollout</td><td>90%</td><td>CSJ Transformer</td><td>37.82%</td><td>0.04310</td><td>10</td><td>10</td></tr>
<tr><td>Attention Rollout</td><td>90%</td><td>CSJ Conformer</td><td>38.16%</td><td>0.04665</td><td>9</td><td>9</td></tr>
<tr><td>Attention Rollout</td><td>90%</td><td>LaboroTV Conformer</td><td>38.72%</td><td>0.04036</td><td>8</td><td>8</td></tr>
<tr><td>Attention Rollout</td><td>90%</td><td>Whisper large-v3</td><td>36.54%</td><td>0.04264</td><td>10</td><td>10</td></tr>
</tbody></table></div>

</details>

## 採用設定を別の発話に適用した本実験

ΔCERはパーセントポイント単位で、負の値は文字誤り率の低下を表します。括弧の n は有効発話数です。

| 手法 | 追加① 絶対IG比 ΔCER (pp) | 追加② 開発選定条件 | 選定共通発話 | 追加② 混合音比 ΔCER (pp) |
| --- | --- | --- | --- | --- |
| 絶対IG | — (n=0) | — | 0 | — (n=0) |
| 正IG | — (n=0) | — | 0 | — (n=0) |
| Occlusion | — (n=0) | — | 0 | — (n=0) |
| Permutation SHAP | — (n=0) | — | 0 | — (n=0) |
| LIME | — (n=0) | — | 0 | — (n=0) |
| Saliency | — (n=0) | — | 0 | — (n=0) |
| Input × Gradient | — (n=0) | — | 0 | — (n=0) |
| SmoothGrad | — (n=0) | — | 0 | — (n=0) |
| Grad-CAM | — (n=0) | — | 0 | — (n=0) |
| Attention Rollout | — (n=0) | — | 0 | — (n=0) |

### 追加① 生成ASR別の集計

| 生成ASR | 手法 | Reazon CER | 混合音CER | 波形MAE | ΔSI-SDR (dB) | CER有効 | 波形有効 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CSJ Transformer | 絶対IG | — | — | — | — | 0 | 0 |
| CSJ Transformer | 正IG | — | — | — | — | 0 | 0 |
| CSJ Transformer | Occlusion | — | — | — | — | 0 | 0 |
| CSJ Transformer | Permutation SHAP | — | — | — | — | 0 | 0 |
| CSJ Transformer | LIME | — | — | — | — | 0 | 0 |
| CSJ Transformer | Saliency | — | — | — | — | 0 | 0 |
| CSJ Transformer | Input × Gradient | — | — | — | — | 0 | 0 |
| CSJ Transformer | SmoothGrad | — | — | — | — | 0 | 0 |
| CSJ Transformer | Grad-CAM | — | — | — | — | 0 | 0 |
| CSJ Transformer | Attention Rollout | — | — | — | — | 0 | 0 |
| CSJ Transformer | 全保持NNLS | — | — | — | — | 0 | 0 |
| CSJ Transformer | 絶対IG同面積 Energy | — | — | — | — | 0 | 0 |
| CSJ Transformer | 絶対IG同面積 Random | — | — | — | — | 0 | 0 |
| CSJ Transformer | 正IG同面積 Energy | — | — | — | — | 0 | 0 |
| CSJ Transformer | 正IG同面積 Random | — | — | — | — | 0 | 0 |
| CSJ Conformer | 絶対IG | — | — | — | — | 0 | 0 |
| CSJ Conformer | 正IG | — | — | — | — | 0 | 0 |
| CSJ Conformer | Occlusion | — | — | — | — | 0 | 0 |
| CSJ Conformer | Permutation SHAP | — | — | — | — | 0 | 0 |
| CSJ Conformer | LIME | — | — | — | — | 0 | 0 |
| CSJ Conformer | Saliency | — | — | — | — | 0 | 0 |
| CSJ Conformer | Input × Gradient | — | — | — | — | 0 | 0 |
| CSJ Conformer | SmoothGrad | — | — | — | — | 0 | 0 |
| CSJ Conformer | Grad-CAM | — | — | — | — | 0 | 0 |
| CSJ Conformer | Attention Rollout | — | — | — | — | 0 | 0 |
| CSJ Conformer | 全保持NNLS | — | — | — | — | 0 | 0 |
| CSJ Conformer | 絶対IG同面積 Energy | — | — | — | — | 0 | 0 |
| CSJ Conformer | 絶対IG同面積 Random | — | — | — | — | 0 | 0 |
| CSJ Conformer | 正IG同面積 Energy | — | — | — | — | 0 | 0 |
| CSJ Conformer | 正IG同面積 Random | — | — | — | — | 0 | 0 |
| LaboroTV Conformer | 絶対IG | — | — | — | — | 0 | 0 |
| LaboroTV Conformer | 正IG | — | — | — | — | 0 | 0 |
| LaboroTV Conformer | Occlusion | — | — | — | — | 0 | 0 |
| LaboroTV Conformer | Permutation SHAP | — | — | — | — | 0 | 0 |
| LaboroTV Conformer | LIME | — | — | — | — | 0 | 0 |
| LaboroTV Conformer | Saliency | — | — | — | — | 0 | 0 |
| LaboroTV Conformer | Input × Gradient | — | — | — | — | 0 | 0 |
| LaboroTV Conformer | SmoothGrad | — | — | — | — | 0 | 0 |
| LaboroTV Conformer | Grad-CAM | — | — | — | — | 0 | 0 |
| LaboroTV Conformer | Attention Rollout | — | — | — | — | 0 | 0 |
| LaboroTV Conformer | 全保持NNLS | — | — | — | — | 0 | 0 |
| LaboroTV Conformer | 絶対IG同面積 Energy | — | — | — | — | 0 | 0 |
| LaboroTV Conformer | 絶対IG同面積 Random | — | — | — | — | 0 | 0 |
| LaboroTV Conformer | 正IG同面積 Energy | — | — | — | — | 0 | 0 |
| LaboroTV Conformer | 正IG同面積 Random | — | — | — | — | 0 | 0 |
| Whisper large-v3 | 絶対IG | — | — | — | — | 0 | 0 |
| Whisper large-v3 | 正IG | — | — | — | — | 0 | 0 |
| Whisper large-v3 | Occlusion | — | — | — | — | 0 | 0 |
| Whisper large-v3 | Permutation SHAP | — | — | — | — | 0 | 0 |
| Whisper large-v3 | LIME | — | — | — | — | 0 | 0 |
| Whisper large-v3 | Saliency | — | — | — | — | 0 | 0 |
| Whisper large-v3 | Input × Gradient | — | — | — | — | 0 | 0 |
| Whisper large-v3 | SmoothGrad | — | — | — | — | 0 | 0 |
| Whisper large-v3 | Grad-CAM | — | — | — | — | 0 | 0 |
| Whisper large-v3 | Attention Rollout | — | — | — | — | 0 | 0 |
| Whisper large-v3 | 全保持NNLS | — | — | — | — | 0 | 0 |
| Whisper large-v3 | 絶対IG同面積 Energy | — | — | — | — | 0 | 0 |
| Whisper large-v3 | 絶対IG同面積 Random | — | — | — | — | 0 | 0 |
| Whisper large-v3 | 正IG同面積 Energy | — | — | — | — | 0 | 0 |
| Whisper large-v3 | 正IG同面積 Random | — | — | — | — | 0 | 0 |

### 追加② 雑音・SNR・評価器別

<details>
<summary>絶対IG ／ 評価器 CSJ Transformer</summary>

<div class='table-wrap'><table><thead><tr><th>生成ASR</th><th>white_-5</th><th>white_+0</th><th>white_+10</th><th>traffic_-5</th><th>traffic_+0</th><th>traffic_+10</th></tr></thead><tbody>
<tr><td>CSJ Transformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>Whisper large-v3</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
</tbody></table></div>

</details>

<details>
<summary>絶対IG ／ 評価器 CSJ Conformer</summary>

<div class='table-wrap'><table><thead><tr><th>生成ASR</th><th>white_-5</th><th>white_+0</th><th>white_+10</th><th>traffic_-5</th><th>traffic_+0</th><th>traffic_+10</th></tr></thead><tbody>
<tr><td>CSJ Transformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>Whisper large-v3</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
</tbody></table></div>

</details>

<details>
<summary>絶対IG ／ 評価器 LaboroTV Conformer</summary>

<div class='table-wrap'><table><thead><tr><th>生成ASR</th><th>white_-5</th><th>white_+0</th><th>white_+10</th><th>traffic_-5</th><th>traffic_+0</th><th>traffic_+10</th></tr></thead><tbody>
<tr><td>CSJ Transformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>Whisper large-v3</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
</tbody></table></div>

</details>

<details>
<summary>絶対IG ／ 評価器 Whisper large-v3</summary>

<div class='table-wrap'><table><thead><tr><th>生成ASR</th><th>white_-5</th><th>white_+0</th><th>white_+10</th><th>traffic_-5</th><th>traffic_+0</th><th>traffic_+10</th></tr></thead><tbody>
<tr><td>CSJ Transformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>Whisper large-v3</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
</tbody></table></div>

</details>

<details>
<summary>絶対IG ／ 評価器 Reazon</summary>

<div class='table-wrap'><table><thead><tr><th>生成ASR</th><th>white_-5</th><th>white_+0</th><th>white_+10</th><th>traffic_-5</th><th>traffic_+0</th><th>traffic_+10</th></tr></thead><tbody>
<tr><td>CSJ Transformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>Whisper large-v3</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
</tbody></table></div>

</details>

<details>
<summary>正IG ／ 評価器 CSJ Transformer</summary>

<div class='table-wrap'><table><thead><tr><th>生成ASR</th><th>white_-5</th><th>white_+0</th><th>white_+10</th><th>traffic_-5</th><th>traffic_+0</th><th>traffic_+10</th></tr></thead><tbody>
<tr><td>CSJ Transformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>Whisper large-v3</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
</tbody></table></div>

</details>

<details>
<summary>正IG ／ 評価器 CSJ Conformer</summary>

<div class='table-wrap'><table><thead><tr><th>生成ASR</th><th>white_-5</th><th>white_+0</th><th>white_+10</th><th>traffic_-5</th><th>traffic_+0</th><th>traffic_+10</th></tr></thead><tbody>
<tr><td>CSJ Transformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>Whisper large-v3</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
</tbody></table></div>

</details>

<details>
<summary>正IG ／ 評価器 LaboroTV Conformer</summary>

<div class='table-wrap'><table><thead><tr><th>生成ASR</th><th>white_-5</th><th>white_+0</th><th>white_+10</th><th>traffic_-5</th><th>traffic_+0</th><th>traffic_+10</th></tr></thead><tbody>
<tr><td>CSJ Transformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>Whisper large-v3</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
</tbody></table></div>

</details>

<details>
<summary>正IG ／ 評価器 Whisper large-v3</summary>

<div class='table-wrap'><table><thead><tr><th>生成ASR</th><th>white_-5</th><th>white_+0</th><th>white_+10</th><th>traffic_-5</th><th>traffic_+0</th><th>traffic_+10</th></tr></thead><tbody>
<tr><td>CSJ Transformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>Whisper large-v3</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
</tbody></table></div>

</details>

<details>
<summary>正IG ／ 評価器 Reazon</summary>

<div class='table-wrap'><table><thead><tr><th>生成ASR</th><th>white_-5</th><th>white_+0</th><th>white_+10</th><th>traffic_-5</th><th>traffic_+0</th><th>traffic_+10</th></tr></thead><tbody>
<tr><td>CSJ Transformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>Whisper large-v3</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
</tbody></table></div>

</details>

<details>
<summary>Occlusion ／ 評価器 CSJ Transformer</summary>

<div class='table-wrap'><table><thead><tr><th>生成ASR</th><th>white_-5</th><th>white_+0</th><th>white_+10</th><th>traffic_-5</th><th>traffic_+0</th><th>traffic_+10</th></tr></thead><tbody>
<tr><td>CSJ Transformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>Whisper large-v3</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
</tbody></table></div>

</details>

<details>
<summary>Occlusion ／ 評価器 CSJ Conformer</summary>

<div class='table-wrap'><table><thead><tr><th>生成ASR</th><th>white_-5</th><th>white_+0</th><th>white_+10</th><th>traffic_-5</th><th>traffic_+0</th><th>traffic_+10</th></tr></thead><tbody>
<tr><td>CSJ Transformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>Whisper large-v3</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
</tbody></table></div>

</details>

<details>
<summary>Occlusion ／ 評価器 LaboroTV Conformer</summary>

<div class='table-wrap'><table><thead><tr><th>生成ASR</th><th>white_-5</th><th>white_+0</th><th>white_+10</th><th>traffic_-5</th><th>traffic_+0</th><th>traffic_+10</th></tr></thead><tbody>
<tr><td>CSJ Transformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>Whisper large-v3</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
</tbody></table></div>

</details>

<details>
<summary>Occlusion ／ 評価器 Whisper large-v3</summary>

<div class='table-wrap'><table><thead><tr><th>生成ASR</th><th>white_-5</th><th>white_+0</th><th>white_+10</th><th>traffic_-5</th><th>traffic_+0</th><th>traffic_+10</th></tr></thead><tbody>
<tr><td>CSJ Transformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>Whisper large-v3</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
</tbody></table></div>

</details>

<details>
<summary>Occlusion ／ 評価器 Reazon</summary>

<div class='table-wrap'><table><thead><tr><th>生成ASR</th><th>white_-5</th><th>white_+0</th><th>white_+10</th><th>traffic_-5</th><th>traffic_+0</th><th>traffic_+10</th></tr></thead><tbody>
<tr><td>CSJ Transformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>Whisper large-v3</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
</tbody></table></div>

</details>

<details>
<summary>Permutation SHAP ／ 評価器 CSJ Transformer</summary>

<div class='table-wrap'><table><thead><tr><th>生成ASR</th><th>white_-5</th><th>white_+0</th><th>white_+10</th><th>traffic_-5</th><th>traffic_+0</th><th>traffic_+10</th></tr></thead><tbody>
<tr><td>CSJ Transformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>Whisper large-v3</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
</tbody></table></div>

</details>

<details>
<summary>Permutation SHAP ／ 評価器 CSJ Conformer</summary>

<div class='table-wrap'><table><thead><tr><th>生成ASR</th><th>white_-5</th><th>white_+0</th><th>white_+10</th><th>traffic_-5</th><th>traffic_+0</th><th>traffic_+10</th></tr></thead><tbody>
<tr><td>CSJ Transformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>Whisper large-v3</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
</tbody></table></div>

</details>

<details>
<summary>Permutation SHAP ／ 評価器 LaboroTV Conformer</summary>

<div class='table-wrap'><table><thead><tr><th>生成ASR</th><th>white_-5</th><th>white_+0</th><th>white_+10</th><th>traffic_-5</th><th>traffic_+0</th><th>traffic_+10</th></tr></thead><tbody>
<tr><td>CSJ Transformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>Whisper large-v3</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
</tbody></table></div>

</details>

<details>
<summary>Permutation SHAP ／ 評価器 Whisper large-v3</summary>

<div class='table-wrap'><table><thead><tr><th>生成ASR</th><th>white_-5</th><th>white_+0</th><th>white_+10</th><th>traffic_-5</th><th>traffic_+0</th><th>traffic_+10</th></tr></thead><tbody>
<tr><td>CSJ Transformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>Whisper large-v3</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
</tbody></table></div>

</details>

<details>
<summary>Permutation SHAP ／ 評価器 Reazon</summary>

<div class='table-wrap'><table><thead><tr><th>生成ASR</th><th>white_-5</th><th>white_+0</th><th>white_+10</th><th>traffic_-5</th><th>traffic_+0</th><th>traffic_+10</th></tr></thead><tbody>
<tr><td>CSJ Transformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>Whisper large-v3</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
</tbody></table></div>

</details>

<details>
<summary>LIME ／ 評価器 CSJ Transformer</summary>

<div class='table-wrap'><table><thead><tr><th>生成ASR</th><th>white_-5</th><th>white_+0</th><th>white_+10</th><th>traffic_-5</th><th>traffic_+0</th><th>traffic_+10</th></tr></thead><tbody>
<tr><td>CSJ Transformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>Whisper large-v3</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
</tbody></table></div>

</details>

<details>
<summary>LIME ／ 評価器 CSJ Conformer</summary>

<div class='table-wrap'><table><thead><tr><th>生成ASR</th><th>white_-5</th><th>white_+0</th><th>white_+10</th><th>traffic_-5</th><th>traffic_+0</th><th>traffic_+10</th></tr></thead><tbody>
<tr><td>CSJ Transformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>Whisper large-v3</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
</tbody></table></div>

</details>

<details>
<summary>LIME ／ 評価器 LaboroTV Conformer</summary>

<div class='table-wrap'><table><thead><tr><th>生成ASR</th><th>white_-5</th><th>white_+0</th><th>white_+10</th><th>traffic_-5</th><th>traffic_+0</th><th>traffic_+10</th></tr></thead><tbody>
<tr><td>CSJ Transformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>Whisper large-v3</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
</tbody></table></div>

</details>

<details>
<summary>LIME ／ 評価器 Whisper large-v3</summary>

<div class='table-wrap'><table><thead><tr><th>生成ASR</th><th>white_-5</th><th>white_+0</th><th>white_+10</th><th>traffic_-5</th><th>traffic_+0</th><th>traffic_+10</th></tr></thead><tbody>
<tr><td>CSJ Transformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>Whisper large-v3</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
</tbody></table></div>

</details>

<details>
<summary>LIME ／ 評価器 Reazon</summary>

<div class='table-wrap'><table><thead><tr><th>生成ASR</th><th>white_-5</th><th>white_+0</th><th>white_+10</th><th>traffic_-5</th><th>traffic_+0</th><th>traffic_+10</th></tr></thead><tbody>
<tr><td>CSJ Transformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>Whisper large-v3</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
</tbody></table></div>

</details>

<details>
<summary>Saliency ／ 評価器 CSJ Transformer</summary>

<div class='table-wrap'><table><thead><tr><th>生成ASR</th><th>white_-5</th><th>white_+0</th><th>white_+10</th><th>traffic_-5</th><th>traffic_+0</th><th>traffic_+10</th></tr></thead><tbody>
<tr><td>CSJ Transformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>Whisper large-v3</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
</tbody></table></div>

</details>

<details>
<summary>Saliency ／ 評価器 CSJ Conformer</summary>

<div class='table-wrap'><table><thead><tr><th>生成ASR</th><th>white_-5</th><th>white_+0</th><th>white_+10</th><th>traffic_-5</th><th>traffic_+0</th><th>traffic_+10</th></tr></thead><tbody>
<tr><td>CSJ Transformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>Whisper large-v3</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
</tbody></table></div>

</details>

<details>
<summary>Saliency ／ 評価器 LaboroTV Conformer</summary>

<div class='table-wrap'><table><thead><tr><th>生成ASR</th><th>white_-5</th><th>white_+0</th><th>white_+10</th><th>traffic_-5</th><th>traffic_+0</th><th>traffic_+10</th></tr></thead><tbody>
<tr><td>CSJ Transformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>Whisper large-v3</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
</tbody></table></div>

</details>

<details>
<summary>Saliency ／ 評価器 Whisper large-v3</summary>

<div class='table-wrap'><table><thead><tr><th>生成ASR</th><th>white_-5</th><th>white_+0</th><th>white_+10</th><th>traffic_-5</th><th>traffic_+0</th><th>traffic_+10</th></tr></thead><tbody>
<tr><td>CSJ Transformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>Whisper large-v3</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
</tbody></table></div>

</details>

<details>
<summary>Saliency ／ 評価器 Reazon</summary>

<div class='table-wrap'><table><thead><tr><th>生成ASR</th><th>white_-5</th><th>white_+0</th><th>white_+10</th><th>traffic_-5</th><th>traffic_+0</th><th>traffic_+10</th></tr></thead><tbody>
<tr><td>CSJ Transformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>Whisper large-v3</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
</tbody></table></div>

</details>

<details>
<summary>Input × Gradient ／ 評価器 CSJ Transformer</summary>

<div class='table-wrap'><table><thead><tr><th>生成ASR</th><th>white_-5</th><th>white_+0</th><th>white_+10</th><th>traffic_-5</th><th>traffic_+0</th><th>traffic_+10</th></tr></thead><tbody>
<tr><td>CSJ Transformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>Whisper large-v3</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
</tbody></table></div>

</details>

<details>
<summary>Input × Gradient ／ 評価器 CSJ Conformer</summary>

<div class='table-wrap'><table><thead><tr><th>生成ASR</th><th>white_-5</th><th>white_+0</th><th>white_+10</th><th>traffic_-5</th><th>traffic_+0</th><th>traffic_+10</th></tr></thead><tbody>
<tr><td>CSJ Transformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>Whisper large-v3</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
</tbody></table></div>

</details>

<details>
<summary>Input × Gradient ／ 評価器 LaboroTV Conformer</summary>

<div class='table-wrap'><table><thead><tr><th>生成ASR</th><th>white_-5</th><th>white_+0</th><th>white_+10</th><th>traffic_-5</th><th>traffic_+0</th><th>traffic_+10</th></tr></thead><tbody>
<tr><td>CSJ Transformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>Whisper large-v3</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
</tbody></table></div>

</details>

<details>
<summary>Input × Gradient ／ 評価器 Whisper large-v3</summary>

<div class='table-wrap'><table><thead><tr><th>生成ASR</th><th>white_-5</th><th>white_+0</th><th>white_+10</th><th>traffic_-5</th><th>traffic_+0</th><th>traffic_+10</th></tr></thead><tbody>
<tr><td>CSJ Transformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>Whisper large-v3</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
</tbody></table></div>

</details>

<details>
<summary>Input × Gradient ／ 評価器 Reazon</summary>

<div class='table-wrap'><table><thead><tr><th>生成ASR</th><th>white_-5</th><th>white_+0</th><th>white_+10</th><th>traffic_-5</th><th>traffic_+0</th><th>traffic_+10</th></tr></thead><tbody>
<tr><td>CSJ Transformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>Whisper large-v3</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
</tbody></table></div>

</details>

<details>
<summary>SmoothGrad ／ 評価器 CSJ Transformer</summary>

<div class='table-wrap'><table><thead><tr><th>生成ASR</th><th>white_-5</th><th>white_+0</th><th>white_+10</th><th>traffic_-5</th><th>traffic_+0</th><th>traffic_+10</th></tr></thead><tbody>
<tr><td>CSJ Transformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>Whisper large-v3</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
</tbody></table></div>

</details>

<details>
<summary>SmoothGrad ／ 評価器 CSJ Conformer</summary>

<div class='table-wrap'><table><thead><tr><th>生成ASR</th><th>white_-5</th><th>white_+0</th><th>white_+10</th><th>traffic_-5</th><th>traffic_+0</th><th>traffic_+10</th></tr></thead><tbody>
<tr><td>CSJ Transformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>Whisper large-v3</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
</tbody></table></div>

</details>

<details>
<summary>SmoothGrad ／ 評価器 LaboroTV Conformer</summary>

<div class='table-wrap'><table><thead><tr><th>生成ASR</th><th>white_-5</th><th>white_+0</th><th>white_+10</th><th>traffic_-5</th><th>traffic_+0</th><th>traffic_+10</th></tr></thead><tbody>
<tr><td>CSJ Transformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>Whisper large-v3</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
</tbody></table></div>

</details>

<details>
<summary>SmoothGrad ／ 評価器 Whisper large-v3</summary>

<div class='table-wrap'><table><thead><tr><th>生成ASR</th><th>white_-5</th><th>white_+0</th><th>white_+10</th><th>traffic_-5</th><th>traffic_+0</th><th>traffic_+10</th></tr></thead><tbody>
<tr><td>CSJ Transformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>Whisper large-v3</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
</tbody></table></div>

</details>

<details>
<summary>SmoothGrad ／ 評価器 Reazon</summary>

<div class='table-wrap'><table><thead><tr><th>生成ASR</th><th>white_-5</th><th>white_+0</th><th>white_+10</th><th>traffic_-5</th><th>traffic_+0</th><th>traffic_+10</th></tr></thead><tbody>
<tr><td>CSJ Transformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>Whisper large-v3</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
</tbody></table></div>

</details>

<details>
<summary>Grad-CAM ／ 評価器 CSJ Transformer</summary>

<div class='table-wrap'><table><thead><tr><th>生成ASR</th><th>white_-5</th><th>white_+0</th><th>white_+10</th><th>traffic_-5</th><th>traffic_+0</th><th>traffic_+10</th></tr></thead><tbody>
<tr><td>CSJ Transformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>Whisper large-v3</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
</tbody></table></div>

</details>

<details>
<summary>Grad-CAM ／ 評価器 CSJ Conformer</summary>

<div class='table-wrap'><table><thead><tr><th>生成ASR</th><th>white_-5</th><th>white_+0</th><th>white_+10</th><th>traffic_-5</th><th>traffic_+0</th><th>traffic_+10</th></tr></thead><tbody>
<tr><td>CSJ Transformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>Whisper large-v3</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
</tbody></table></div>

</details>

<details>
<summary>Grad-CAM ／ 評価器 LaboroTV Conformer</summary>

<div class='table-wrap'><table><thead><tr><th>生成ASR</th><th>white_-5</th><th>white_+0</th><th>white_+10</th><th>traffic_-5</th><th>traffic_+0</th><th>traffic_+10</th></tr></thead><tbody>
<tr><td>CSJ Transformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>Whisper large-v3</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
</tbody></table></div>

</details>

<details>
<summary>Grad-CAM ／ 評価器 Whisper large-v3</summary>

<div class='table-wrap'><table><thead><tr><th>生成ASR</th><th>white_-5</th><th>white_+0</th><th>white_+10</th><th>traffic_-5</th><th>traffic_+0</th><th>traffic_+10</th></tr></thead><tbody>
<tr><td>CSJ Transformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>Whisper large-v3</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
</tbody></table></div>

</details>

<details>
<summary>Grad-CAM ／ 評価器 Reazon</summary>

<div class='table-wrap'><table><thead><tr><th>生成ASR</th><th>white_-5</th><th>white_+0</th><th>white_+10</th><th>traffic_-5</th><th>traffic_+0</th><th>traffic_+10</th></tr></thead><tbody>
<tr><td>CSJ Transformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>Whisper large-v3</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
</tbody></table></div>

</details>

<details>
<summary>Attention Rollout ／ 評価器 CSJ Transformer</summary>

<div class='table-wrap'><table><thead><tr><th>生成ASR</th><th>white_-5</th><th>white_+0</th><th>white_+10</th><th>traffic_-5</th><th>traffic_+0</th><th>traffic_+10</th></tr></thead><tbody>
<tr><td>CSJ Transformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>Whisper large-v3</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
</tbody></table></div>

</details>

<details>
<summary>Attention Rollout ／ 評価器 CSJ Conformer</summary>

<div class='table-wrap'><table><thead><tr><th>生成ASR</th><th>white_-5</th><th>white_+0</th><th>white_+10</th><th>traffic_-5</th><th>traffic_+0</th><th>traffic_+10</th></tr></thead><tbody>
<tr><td>CSJ Transformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>Whisper large-v3</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
</tbody></table></div>

</details>

<details>
<summary>Attention Rollout ／ 評価器 LaboroTV Conformer</summary>

<div class='table-wrap'><table><thead><tr><th>生成ASR</th><th>white_-5</th><th>white_+0</th><th>white_+10</th><th>traffic_-5</th><th>traffic_+0</th><th>traffic_+10</th></tr></thead><tbody>
<tr><td>CSJ Transformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>Whisper large-v3</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
</tbody></table></div>

</details>

<details>
<summary>Attention Rollout ／ 評価器 Whisper large-v3</summary>

<div class='table-wrap'><table><thead><tr><th>生成ASR</th><th>white_-5</th><th>white_+0</th><th>white_+10</th><th>traffic_-5</th><th>traffic_+0</th><th>traffic_+10</th></tr></thead><tbody>
<tr><td>CSJ Transformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>Whisper large-v3</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
</tbody></table></div>

</details>

<details>
<summary>Attention Rollout ／ 評価器 Reazon</summary>

<div class='table-wrap'><table><thead><tr><th>生成ASR</th><th>white_-5</th><th>white_+0</th><th>white_+10</th><th>traffic_-5</th><th>traffic_+0</th><th>traffic_+10</th></tr></thead><tbody>
<tr><td>CSJ Transformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>Whisper large-v3</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td><td>— (n=0)</td></tr>
</tbody></table></div>

</details>

### 追加③ 声の優勢度との関係

<details>
<summary>既存1000混合</summary>

<div class='table-wrap'><table><thead><tr><th>生成ASR</th><th>手法</th><th>q–重要度 ρ</th><th>q–利得 ρ</th><th>J</th><th>ΔSI-SDR (dB)</th><th>ΔCER (pp)</th></tr></thead><tbody>
<tr><td>CSJ Transformer</td><td>絶対IG</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>CSJ Transformer</td><td>正IG</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>CSJ Transformer</td><td>Occlusion</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>CSJ Transformer</td><td>Permutation SHAP</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>CSJ Transformer</td><td>LIME</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>CSJ Transformer</td><td>Saliency</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>CSJ Transformer</td><td>Input × Gradient</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>CSJ Transformer</td><td>SmoothGrad</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>CSJ Transformer</td><td>Grad-CAM</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>CSJ Transformer</td><td>Attention Rollout</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>CSJ Conformer</td><td>絶対IG</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>CSJ Conformer</td><td>正IG</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>CSJ Conformer</td><td>Occlusion</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>CSJ Conformer</td><td>Permutation SHAP</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>CSJ Conformer</td><td>LIME</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>CSJ Conformer</td><td>Saliency</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>CSJ Conformer</td><td>Input × Gradient</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>CSJ Conformer</td><td>SmoothGrad</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>CSJ Conformer</td><td>Grad-CAM</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>CSJ Conformer</td><td>Attention Rollout</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>絶対IG</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>正IG</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>Occlusion</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>Permutation SHAP</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>LIME</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>Saliency</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>Input × Gradient</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>SmoothGrad</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>Grad-CAM</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>Attention Rollout</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>Whisper large-v3</td><td>絶対IG</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>Whisper large-v3</td><td>正IG</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>Whisper large-v3</td><td>Occlusion</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>Whisper large-v3</td><td>Permutation SHAP</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>Whisper large-v3</td><td>LIME</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>Whisper large-v3</td><td>Saliency</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>Whisper large-v3</td><td>Input × Gradient</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>Whisper large-v3</td><td>SmoothGrad</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>Whisper large-v3</td><td>Grad-CAM</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>Whisper large-v3</td><td>Attention Rollout</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
</tbody></table></div>

</details>

<details>
<summary>旧5組の混ぜ直し</summary>

<div class='table-wrap'><table><thead><tr><th>生成ASR</th><th>手法</th><th>q–重要度 ρ</th><th>q–利得 ρ</th><th>J</th><th>ΔSI-SDR (dB)</th><th>ΔCER (pp)</th></tr></thead><tbody>
<tr><td>CSJ Transformer</td><td>絶対IG</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>CSJ Transformer</td><td>正IG</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>CSJ Transformer</td><td>Occlusion</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>CSJ Transformer</td><td>Permutation SHAP</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>CSJ Transformer</td><td>LIME</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>CSJ Transformer</td><td>Saliency</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>CSJ Transformer</td><td>Input × Gradient</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>CSJ Transformer</td><td>SmoothGrad</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>CSJ Transformer</td><td>Grad-CAM</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>CSJ Transformer</td><td>Attention Rollout</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>CSJ Conformer</td><td>絶対IG</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>CSJ Conformer</td><td>正IG</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>CSJ Conformer</td><td>Occlusion</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>CSJ Conformer</td><td>Permutation SHAP</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>CSJ Conformer</td><td>LIME</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>CSJ Conformer</td><td>Saliency</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>CSJ Conformer</td><td>Input × Gradient</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>CSJ Conformer</td><td>SmoothGrad</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>CSJ Conformer</td><td>Grad-CAM</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>CSJ Conformer</td><td>Attention Rollout</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>絶対IG</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>正IG</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>Occlusion</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>Permutation SHAP</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>LIME</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>Saliency</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>Input × Gradient</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>SmoothGrad</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>Grad-CAM</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>Attention Rollout</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>Whisper large-v3</td><td>絶対IG</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>Whisper large-v3</td><td>正IG</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>Whisper large-v3</td><td>Occlusion</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>Whisper large-v3</td><td>Permutation SHAP</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>Whisper large-v3</td><td>LIME</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>Whisper large-v3</td><td>Saliency</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>Whisper large-v3</td><td>Input × Gradient</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>Whisper large-v3</td><td>SmoothGrad</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>Whisper large-v3</td><td>Grad-CAM</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>Whisper large-v3</td><td>Attention Rollout</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
</tbody></table></div>

<div class='table-wrap'><table><thead><tr><th>生成ASR</th><th>手法</th><th>寄与シェア追従 ρ</th><th>実出力利得追従 ρ</th></tr></thead><tbody>
<tr><td>CSJ Transformer</td><td>絶対IG</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Transformer</td><td>正IG</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Transformer</td><td>Occlusion</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Transformer</td><td>Permutation SHAP</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Transformer</td><td>LIME</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Transformer</td><td>Saliency</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Transformer</td><td>Input × Gradient</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Transformer</td><td>SmoothGrad</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Transformer</td><td>Grad-CAM</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Transformer</td><td>Attention Rollout</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Conformer</td><td>絶対IG</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Conformer</td><td>正IG</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Conformer</td><td>Occlusion</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Conformer</td><td>Permutation SHAP</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Conformer</td><td>LIME</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Conformer</td><td>Saliency</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Conformer</td><td>Input × Gradient</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Conformer</td><td>SmoothGrad</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Conformer</td><td>Grad-CAM</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Conformer</td><td>Attention Rollout</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>絶対IG</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>正IG</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>Occlusion</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>Permutation SHAP</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>LIME</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>Saliency</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>Input × Gradient</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>SmoothGrad</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>Grad-CAM</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>Attention Rollout</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>Whisper large-v3</td><td>絶対IG</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>Whisper large-v3</td><td>正IG</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>Whisper large-v3</td><td>Occlusion</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>Whisper large-v3</td><td>Permutation SHAP</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>Whisper large-v3</td><td>LIME</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>Whisper large-v3</td><td>Saliency</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>Whisper large-v3</td><td>Input × Gradient</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>Whisper large-v3</td><td>SmoothGrad</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>Whisper large-v3</td><td>Grad-CAM</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>Whisper large-v3</td><td>Attention Rollout</td><td>— (n=0)</td><td>— (n=0)</td></tr>
</tbody></table></div>

</details>

<details>
<summary>新30組の混ぜ直し</summary>

<div class='table-wrap'><table><thead><tr><th>生成ASR</th><th>手法</th><th>q–重要度 ρ</th><th>q–利得 ρ</th><th>J</th><th>ΔSI-SDR (dB)</th><th>ΔCER (pp)</th></tr></thead><tbody>
<tr><td>CSJ Transformer</td><td>絶対IG</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>CSJ Transformer</td><td>正IG</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>CSJ Transformer</td><td>Occlusion</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>CSJ Transformer</td><td>Permutation SHAP</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>CSJ Transformer</td><td>LIME</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>CSJ Transformer</td><td>Saliency</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>CSJ Transformer</td><td>Input × Gradient</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>CSJ Transformer</td><td>SmoothGrad</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>CSJ Transformer</td><td>Grad-CAM</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>CSJ Transformer</td><td>Attention Rollout</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>CSJ Conformer</td><td>絶対IG</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>CSJ Conformer</td><td>正IG</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>CSJ Conformer</td><td>Occlusion</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>CSJ Conformer</td><td>Permutation SHAP</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>CSJ Conformer</td><td>LIME</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>CSJ Conformer</td><td>Saliency</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>CSJ Conformer</td><td>Input × Gradient</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>CSJ Conformer</td><td>SmoothGrad</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>CSJ Conformer</td><td>Grad-CAM</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>CSJ Conformer</td><td>Attention Rollout</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>絶対IG</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>正IG</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>Occlusion</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>Permutation SHAP</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>LIME</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>Saliency</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>Input × Gradient</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>SmoothGrad</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>Grad-CAM</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>Attention Rollout</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>Whisper large-v3</td><td>絶対IG</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>Whisper large-v3</td><td>正IG</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>Whisper large-v3</td><td>Occlusion</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>Whisper large-v3</td><td>Permutation SHAP</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>Whisper large-v3</td><td>LIME</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>Whisper large-v3</td><td>Saliency</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>Whisper large-v3</td><td>Input × Gradient</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>Whisper large-v3</td><td>SmoothGrad</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>Whisper large-v3</td><td>Grad-CAM</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
<tr><td>Whisper large-v3</td><td>Attention Rollout</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td><td>— (0)</td></tr>
</tbody></table></div>

<div class='table-wrap'><table><thead><tr><th>生成ASR</th><th>手法</th><th>寄与シェア追従 ρ</th><th>実出力利得追従 ρ</th></tr></thead><tbody>
<tr><td>CSJ Transformer</td><td>絶対IG</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Transformer</td><td>正IG</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Transformer</td><td>Occlusion</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Transformer</td><td>Permutation SHAP</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Transformer</td><td>LIME</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Transformer</td><td>Saliency</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Transformer</td><td>Input × Gradient</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Transformer</td><td>SmoothGrad</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Transformer</td><td>Grad-CAM</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Transformer</td><td>Attention Rollout</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Conformer</td><td>絶対IG</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Conformer</td><td>正IG</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Conformer</td><td>Occlusion</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Conformer</td><td>Permutation SHAP</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Conformer</td><td>LIME</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Conformer</td><td>Saliency</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Conformer</td><td>Input × Gradient</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Conformer</td><td>SmoothGrad</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Conformer</td><td>Grad-CAM</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>CSJ Conformer</td><td>Attention Rollout</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>絶対IG</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>正IG</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>Occlusion</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>Permutation SHAP</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>LIME</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>Saliency</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>Input × Gradient</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>SmoothGrad</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>Grad-CAM</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>LaboroTV Conformer</td><td>Attention Rollout</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>Whisper large-v3</td><td>絶対IG</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>Whisper large-v3</td><td>正IG</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>Whisper large-v3</td><td>Occlusion</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>Whisper large-v3</td><td>Permutation SHAP</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>Whisper large-v3</td><td>LIME</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>Whisper large-v3</td><td>Saliency</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>Whisper large-v3</td><td>Input × Gradient</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>Whisper large-v3</td><td>SmoothGrad</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>Whisper large-v3</td><td>Grad-CAM</td><td>— (n=0)</td><td>— (n=0)</td></tr>
<tr><td>Whisper large-v3</td><td>Attention Rollout</td><td>— (n=0)</td><td>— (n=0)</td></tr>
</tbody></table></div>

</details>

### 処理状況

<details>
<summary>実験群・生成ASR・手法ごとの件数</summary>

<div class='table-wrap'><table><thead><tr><th>群</th><th>生成ASR</th><th>手法</th><th>予定</th><th>再構成</th><th>Reazon有効</th><th>失敗</th><th>評価欠測</th><th>未処理</th><th>選定不可</th><th>品質未達</th><th>NNLS未収束</th></tr></thead><tbody>
<tr><td>dev</td><td>CSJ Transformer</td><td>絶対IG</td><td>72</td><td>0</td><td>0</td><td>0</td><td>0</td><td>72</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>dev</td><td>CSJ Conformer</td><td>絶対IG</td><td>72</td><td>0</td><td>0</td><td>0</td><td>0</td><td>72</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>dev</td><td>LaboroTV Conformer</td><td>絶対IG</td><td>72</td><td>0</td><td>0</td><td>0</td><td>0</td><td>72</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>dev</td><td>Whisper large-v3</td><td>絶対IG</td><td>72</td><td>0</td><td>0</td><td>0</td><td>0</td><td>72</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>dev</td><td>CSJ Transformer</td><td>正IG</td><td>72</td><td>0</td><td>0</td><td>0</td><td>0</td><td>72</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>dev</td><td>CSJ Conformer</td><td>正IG</td><td>72</td><td>0</td><td>0</td><td>0</td><td>0</td><td>72</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>dev</td><td>LaboroTV Conformer</td><td>正IG</td><td>72</td><td>0</td><td>0</td><td>0</td><td>0</td><td>72</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>dev</td><td>Whisper large-v3</td><td>正IG</td><td>72</td><td>0</td><td>0</td><td>0</td><td>0</td><td>72</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>dev</td><td>CSJ Transformer</td><td>Occlusion</td><td>72</td><td>0</td><td>0</td><td>0</td><td>0</td><td>72</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>dev</td><td>CSJ Conformer</td><td>Occlusion</td><td>72</td><td>0</td><td>0</td><td>0</td><td>0</td><td>72</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>dev</td><td>LaboroTV Conformer</td><td>Occlusion</td><td>72</td><td>0</td><td>0</td><td>0</td><td>0</td><td>72</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>dev</td><td>Whisper large-v3</td><td>Occlusion</td><td>72</td><td>0</td><td>0</td><td>0</td><td>0</td><td>72</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>dev</td><td>CSJ Transformer</td><td>Permutation SHAP</td><td>72</td><td>0</td><td>0</td><td>0</td><td>0</td><td>72</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>dev</td><td>CSJ Conformer</td><td>Permutation SHAP</td><td>72</td><td>0</td><td>0</td><td>0</td><td>0</td><td>72</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>dev</td><td>LaboroTV Conformer</td><td>Permutation SHAP</td><td>72</td><td>0</td><td>0</td><td>0</td><td>0</td><td>72</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>dev</td><td>Whisper large-v3</td><td>Permutation SHAP</td><td>72</td><td>0</td><td>0</td><td>0</td><td>0</td><td>72</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>dev</td><td>CSJ Transformer</td><td>LIME</td><td>72</td><td>0</td><td>0</td><td>0</td><td>0</td><td>72</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>dev</td><td>CSJ Conformer</td><td>LIME</td><td>72</td><td>0</td><td>0</td><td>0</td><td>0</td><td>72</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>dev</td><td>LaboroTV Conformer</td><td>LIME</td><td>72</td><td>0</td><td>0</td><td>0</td><td>0</td><td>72</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>dev</td><td>Whisper large-v3</td><td>LIME</td><td>72</td><td>0</td><td>0</td><td>0</td><td>0</td><td>72</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>dev</td><td>CSJ Transformer</td><td>Saliency</td><td>72</td><td>0</td><td>0</td><td>0</td><td>0</td><td>72</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>dev</td><td>CSJ Conformer</td><td>Saliency</td><td>72</td><td>0</td><td>0</td><td>0</td><td>0</td><td>72</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>dev</td><td>LaboroTV Conformer</td><td>Saliency</td><td>72</td><td>0</td><td>0</td><td>0</td><td>0</td><td>72</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>dev</td><td>Whisper large-v3</td><td>Saliency</td><td>72</td><td>0</td><td>0</td><td>0</td><td>0</td><td>72</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>dev</td><td>CSJ Transformer</td><td>Input × Gradient</td><td>72</td><td>0</td><td>0</td><td>0</td><td>0</td><td>72</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>dev</td><td>CSJ Conformer</td><td>Input × Gradient</td><td>72</td><td>0</td><td>0</td><td>0</td><td>0</td><td>72</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>dev</td><td>LaboroTV Conformer</td><td>Input × Gradient</td><td>72</td><td>0</td><td>0</td><td>0</td><td>0</td><td>72</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>dev</td><td>Whisper large-v3</td><td>Input × Gradient</td><td>72</td><td>0</td><td>0</td><td>0</td><td>0</td><td>72</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>dev</td><td>CSJ Transformer</td><td>SmoothGrad</td><td>72</td><td>0</td><td>0</td><td>0</td><td>0</td><td>72</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>dev</td><td>CSJ Conformer</td><td>SmoothGrad</td><td>72</td><td>0</td><td>0</td><td>0</td><td>0</td><td>72</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>dev</td><td>LaboroTV Conformer</td><td>SmoothGrad</td><td>72</td><td>0</td><td>0</td><td>0</td><td>0</td><td>72</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>dev</td><td>Whisper large-v3</td><td>SmoothGrad</td><td>72</td><td>0</td><td>0</td><td>0</td><td>0</td><td>72</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>dev</td><td>CSJ Transformer</td><td>Grad-CAM</td><td>72</td><td>0</td><td>0</td><td>0</td><td>0</td><td>72</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>dev</td><td>CSJ Conformer</td><td>Grad-CAM</td><td>72</td><td>0</td><td>0</td><td>0</td><td>0</td><td>72</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>dev</td><td>LaboroTV Conformer</td><td>Grad-CAM</td><td>72</td><td>0</td><td>0</td><td>0</td><td>0</td><td>72</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>dev</td><td>Whisper large-v3</td><td>Grad-CAM</td><td>72</td><td>0</td><td>0</td><td>0</td><td>0</td><td>72</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>dev</td><td>CSJ Transformer</td><td>Attention Rollout</td><td>72</td><td>0</td><td>0</td><td>0</td><td>0</td><td>72</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>dev</td><td>CSJ Conformer</td><td>Attention Rollout</td><td>72</td><td>0</td><td>0</td><td>0</td><td>0</td><td>72</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>dev</td><td>LaboroTV Conformer</td><td>Attention Rollout</td><td>72</td><td>0</td><td>0</td><td>0</td><td>0</td><td>72</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>dev</td><td>Whisper large-v3</td><td>Attention Rollout</td><td>72</td><td>0</td><td>0</td><td>0</td><td>0</td><td>72</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>dev</td><td>CSJ Transformer</td><td>全保持NNLS</td><td>72</td><td>0</td><td>0</td><td>0</td><td>0</td><td>72</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>dev</td><td>CSJ Conformer</td><td>全保持NNLS</td><td>72</td><td>0</td><td>0</td><td>0</td><td>0</td><td>72</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>dev</td><td>LaboroTV Conformer</td><td>全保持NNLS</td><td>72</td><td>0</td><td>0</td><td>0</td><td>0</td><td>72</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>dev</td><td>Whisper large-v3</td><td>全保持NNLS</td><td>72</td><td>0</td><td>0</td><td>0</td><td>0</td><td>72</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>dev</td><td>CSJ Transformer</td><td>絶対IG同面積 Energy</td><td>72</td><td>0</td><td>0</td><td>0</td><td>0</td><td>72</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>dev</td><td>CSJ Conformer</td><td>絶対IG同面積 Energy</td><td>72</td><td>0</td><td>0</td><td>0</td><td>0</td><td>72</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>dev</td><td>LaboroTV Conformer</td><td>絶対IG同面積 Energy</td><td>72</td><td>0</td><td>0</td><td>0</td><td>0</td><td>72</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>dev</td><td>Whisper large-v3</td><td>絶対IG同面積 Energy</td><td>72</td><td>0</td><td>0</td><td>0</td><td>0</td><td>72</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>dev</td><td>CSJ Transformer</td><td>絶対IG同面積 Random</td><td>72</td><td>0</td><td>0</td><td>0</td><td>0</td><td>72</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>dev</td><td>CSJ Conformer</td><td>絶対IG同面積 Random</td><td>72</td><td>0</td><td>0</td><td>0</td><td>0</td><td>72</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>dev</td><td>LaboroTV Conformer</td><td>絶対IG同面積 Random</td><td>72</td><td>0</td><td>0</td><td>0</td><td>0</td><td>72</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>dev</td><td>Whisper large-v3</td><td>絶対IG同面積 Random</td><td>72</td><td>0</td><td>0</td><td>0</td><td>0</td><td>72</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>dev</td><td>CSJ Transformer</td><td>正IG同面積 Energy</td><td>72</td><td>0</td><td>0</td><td>0</td><td>0</td><td>72</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>dev</td><td>CSJ Conformer</td><td>正IG同面積 Energy</td><td>72</td><td>0</td><td>0</td><td>0</td><td>0</td><td>72</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>dev</td><td>LaboroTV Conformer</td><td>正IG同面積 Energy</td><td>72</td><td>0</td><td>0</td><td>0</td><td>0</td><td>72</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>dev</td><td>Whisper large-v3</td><td>正IG同面積 Energy</td><td>72</td><td>0</td><td>0</td><td>0</td><td>0</td><td>72</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>dev</td><td>CSJ Transformer</td><td>正IG同面積 Random</td><td>72</td><td>0</td><td>0</td><td>0</td><td>0</td><td>72</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>dev</td><td>CSJ Conformer</td><td>正IG同面積 Random</td><td>72</td><td>0</td><td>0</td><td>0</td><td>0</td><td>72</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>dev</td><td>LaboroTV Conformer</td><td>正IG同面積 Random</td><td>72</td><td>0</td><td>0</td><td>0</td><td>0</td><td>72</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>dev</td><td>Whisper large-v3</td><td>正IG同面積 Random</td><td>72</td><td>0</td><td>0</td><td>0</td><td>0</td><td>72</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>confirm</td><td>CSJ Transformer</td><td>絶対IG</td><td>360</td><td>0</td><td>0</td><td>0</td><td>0</td><td>360</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>confirm</td><td>CSJ Conformer</td><td>絶対IG</td><td>360</td><td>0</td><td>0</td><td>0</td><td>0</td><td>360</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>confirm</td><td>LaboroTV Conformer</td><td>絶対IG</td><td>360</td><td>0</td><td>0</td><td>0</td><td>0</td><td>360</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>confirm</td><td>Whisper large-v3</td><td>絶対IG</td><td>360</td><td>0</td><td>0</td><td>0</td><td>0</td><td>360</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>confirm</td><td>CSJ Transformer</td><td>正IG</td><td>360</td><td>0</td><td>0</td><td>0</td><td>0</td><td>360</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>confirm</td><td>CSJ Conformer</td><td>正IG</td><td>360</td><td>0</td><td>0</td><td>0</td><td>0</td><td>360</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>confirm</td><td>LaboroTV Conformer</td><td>正IG</td><td>360</td><td>0</td><td>0</td><td>0</td><td>0</td><td>360</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>confirm</td><td>Whisper large-v3</td><td>正IG</td><td>360</td><td>0</td><td>0</td><td>0</td><td>0</td><td>360</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>confirm</td><td>CSJ Transformer</td><td>Occlusion</td><td>360</td><td>0</td><td>0</td><td>0</td><td>0</td><td>360</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>confirm</td><td>CSJ Conformer</td><td>Occlusion</td><td>360</td><td>0</td><td>0</td><td>0</td><td>0</td><td>360</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>confirm</td><td>LaboroTV Conformer</td><td>Occlusion</td><td>360</td><td>0</td><td>0</td><td>0</td><td>0</td><td>360</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>confirm</td><td>Whisper large-v3</td><td>Occlusion</td><td>360</td><td>0</td><td>0</td><td>0</td><td>0</td><td>360</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>confirm</td><td>CSJ Transformer</td><td>Permutation SHAP</td><td>360</td><td>0</td><td>0</td><td>0</td><td>0</td><td>360</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>confirm</td><td>CSJ Conformer</td><td>Permutation SHAP</td><td>360</td><td>0</td><td>0</td><td>0</td><td>0</td><td>360</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>confirm</td><td>LaboroTV Conformer</td><td>Permutation SHAP</td><td>360</td><td>0</td><td>0</td><td>0</td><td>0</td><td>360</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>confirm</td><td>Whisper large-v3</td><td>Permutation SHAP</td><td>360</td><td>0</td><td>0</td><td>0</td><td>0</td><td>360</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>confirm</td><td>CSJ Transformer</td><td>LIME</td><td>360</td><td>0</td><td>0</td><td>0</td><td>0</td><td>360</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>confirm</td><td>CSJ Conformer</td><td>LIME</td><td>360</td><td>0</td><td>0</td><td>0</td><td>0</td><td>360</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>confirm</td><td>LaboroTV Conformer</td><td>LIME</td><td>360</td><td>0</td><td>0</td><td>0</td><td>0</td><td>360</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>confirm</td><td>Whisper large-v3</td><td>LIME</td><td>360</td><td>0</td><td>0</td><td>0</td><td>0</td><td>360</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>confirm</td><td>CSJ Transformer</td><td>Saliency</td><td>360</td><td>0</td><td>0</td><td>0</td><td>0</td><td>360</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>confirm</td><td>CSJ Conformer</td><td>Saliency</td><td>360</td><td>0</td><td>0</td><td>0</td><td>0</td><td>360</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>confirm</td><td>LaboroTV Conformer</td><td>Saliency</td><td>360</td><td>0</td><td>0</td><td>0</td><td>0</td><td>360</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>confirm</td><td>Whisper large-v3</td><td>Saliency</td><td>360</td><td>0</td><td>0</td><td>0</td><td>0</td><td>360</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>confirm</td><td>CSJ Transformer</td><td>Input × Gradient</td><td>360</td><td>0</td><td>0</td><td>0</td><td>0</td><td>360</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>confirm</td><td>CSJ Conformer</td><td>Input × Gradient</td><td>360</td><td>0</td><td>0</td><td>0</td><td>0</td><td>360</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>confirm</td><td>LaboroTV Conformer</td><td>Input × Gradient</td><td>360</td><td>0</td><td>0</td><td>0</td><td>0</td><td>360</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>confirm</td><td>Whisper large-v3</td><td>Input × Gradient</td><td>360</td><td>0</td><td>0</td><td>0</td><td>0</td><td>360</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>confirm</td><td>CSJ Transformer</td><td>SmoothGrad</td><td>360</td><td>0</td><td>0</td><td>0</td><td>0</td><td>360</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>confirm</td><td>CSJ Conformer</td><td>SmoothGrad</td><td>360</td><td>0</td><td>0</td><td>0</td><td>0</td><td>360</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>confirm</td><td>LaboroTV Conformer</td><td>SmoothGrad</td><td>360</td><td>0</td><td>0</td><td>0</td><td>0</td><td>360</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>confirm</td><td>Whisper large-v3</td><td>SmoothGrad</td><td>360</td><td>0</td><td>0</td><td>0</td><td>0</td><td>360</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>confirm</td><td>CSJ Transformer</td><td>Grad-CAM</td><td>360</td><td>0</td><td>0</td><td>0</td><td>0</td><td>360</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>confirm</td><td>CSJ Conformer</td><td>Grad-CAM</td><td>360</td><td>0</td><td>0</td><td>0</td><td>0</td><td>360</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>confirm</td><td>LaboroTV Conformer</td><td>Grad-CAM</td><td>360</td><td>0</td><td>0</td><td>0</td><td>0</td><td>360</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>confirm</td><td>Whisper large-v3</td><td>Grad-CAM</td><td>360</td><td>0</td><td>0</td><td>0</td><td>0</td><td>360</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>confirm</td><td>CSJ Transformer</td><td>Attention Rollout</td><td>360</td><td>0</td><td>0</td><td>0</td><td>0</td><td>360</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>confirm</td><td>CSJ Conformer</td><td>Attention Rollout</td><td>360</td><td>0</td><td>0</td><td>0</td><td>0</td><td>360</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>confirm</td><td>LaboroTV Conformer</td><td>Attention Rollout</td><td>360</td><td>0</td><td>0</td><td>0</td><td>0</td><td>360</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>confirm</td><td>Whisper large-v3</td><td>Attention Rollout</td><td>360</td><td>0</td><td>0</td><td>0</td><td>0</td><td>360</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>confirm</td><td>CSJ Transformer</td><td>全保持NNLS</td><td>360</td><td>0</td><td>0</td><td>0</td><td>0</td><td>360</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>confirm</td><td>CSJ Conformer</td><td>全保持NNLS</td><td>360</td><td>0</td><td>0</td><td>0</td><td>0</td><td>360</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>confirm</td><td>LaboroTV Conformer</td><td>全保持NNLS</td><td>360</td><td>0</td><td>0</td><td>0</td><td>0</td><td>360</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>confirm</td><td>Whisper large-v3</td><td>全保持NNLS</td><td>360</td><td>0</td><td>0</td><td>0</td><td>0</td><td>360</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>confirm</td><td>CSJ Transformer</td><td>絶対IG同面積 Energy</td><td>360</td><td>0</td><td>0</td><td>0</td><td>0</td><td>360</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>confirm</td><td>CSJ Conformer</td><td>絶対IG同面積 Energy</td><td>360</td><td>0</td><td>0</td><td>0</td><td>0</td><td>360</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>confirm</td><td>LaboroTV Conformer</td><td>絶対IG同面積 Energy</td><td>360</td><td>0</td><td>0</td><td>0</td><td>0</td><td>360</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>confirm</td><td>Whisper large-v3</td><td>絶対IG同面積 Energy</td><td>360</td><td>0</td><td>0</td><td>0</td><td>0</td><td>360</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>confirm</td><td>CSJ Transformer</td><td>絶対IG同面積 Random</td><td>360</td><td>0</td><td>0</td><td>0</td><td>0</td><td>360</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>confirm</td><td>CSJ Conformer</td><td>絶対IG同面積 Random</td><td>360</td><td>0</td><td>0</td><td>0</td><td>0</td><td>360</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>confirm</td><td>LaboroTV Conformer</td><td>絶対IG同面積 Random</td><td>360</td><td>0</td><td>0</td><td>0</td><td>0</td><td>360</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>confirm</td><td>Whisper large-v3</td><td>絶対IG同面積 Random</td><td>360</td><td>0</td><td>0</td><td>0</td><td>0</td><td>360</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>confirm</td><td>CSJ Transformer</td><td>正IG同面積 Energy</td><td>360</td><td>0</td><td>0</td><td>0</td><td>0</td><td>360</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>confirm</td><td>CSJ Conformer</td><td>正IG同面積 Energy</td><td>360</td><td>0</td><td>0</td><td>0</td><td>0</td><td>360</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>confirm</td><td>LaboroTV Conformer</td><td>正IG同面積 Energy</td><td>360</td><td>0</td><td>0</td><td>0</td><td>0</td><td>360</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>confirm</td><td>Whisper large-v3</td><td>正IG同面積 Energy</td><td>360</td><td>0</td><td>0</td><td>0</td><td>0</td><td>360</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>confirm</td><td>CSJ Transformer</td><td>正IG同面積 Random</td><td>360</td><td>0</td><td>0</td><td>0</td><td>0</td><td>360</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>confirm</td><td>CSJ Conformer</td><td>正IG同面積 Random</td><td>360</td><td>0</td><td>0</td><td>0</td><td>0</td><td>360</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>confirm</td><td>LaboroTV Conformer</td><td>正IG同面積 Random</td><td>360</td><td>0</td><td>0</td><td>0</td><td>0</td><td>360</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>confirm</td><td>Whisper large-v3</td><td>正IG同面積 Random</td><td>360</td><td>0</td><td>0</td><td>0</td><td>0</td><td>360</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>old</td><td>CSJ Transformer</td><td>絶対IG</td><td>20</td><td>0</td><td>0</td><td>0</td><td>0</td><td>20</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>old</td><td>CSJ Conformer</td><td>絶対IG</td><td>20</td><td>0</td><td>0</td><td>0</td><td>0</td><td>20</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>old</td><td>LaboroTV Conformer</td><td>絶対IG</td><td>20</td><td>0</td><td>0</td><td>0</td><td>0</td><td>20</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>old</td><td>Whisper large-v3</td><td>絶対IG</td><td>20</td><td>0</td><td>0</td><td>0</td><td>0</td><td>20</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>old</td><td>CSJ Transformer</td><td>正IG</td><td>20</td><td>0</td><td>0</td><td>0</td><td>0</td><td>20</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>old</td><td>CSJ Conformer</td><td>正IG</td><td>20</td><td>0</td><td>0</td><td>0</td><td>0</td><td>20</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>old</td><td>LaboroTV Conformer</td><td>正IG</td><td>20</td><td>0</td><td>0</td><td>0</td><td>0</td><td>20</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>old</td><td>Whisper large-v3</td><td>正IG</td><td>20</td><td>0</td><td>0</td><td>0</td><td>0</td><td>20</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>old</td><td>CSJ Transformer</td><td>Occlusion</td><td>20</td><td>0</td><td>0</td><td>0</td><td>0</td><td>20</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>old</td><td>CSJ Conformer</td><td>Occlusion</td><td>20</td><td>0</td><td>0</td><td>0</td><td>0</td><td>20</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>old</td><td>LaboroTV Conformer</td><td>Occlusion</td><td>20</td><td>0</td><td>0</td><td>0</td><td>0</td><td>20</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>old</td><td>Whisper large-v3</td><td>Occlusion</td><td>20</td><td>0</td><td>0</td><td>0</td><td>0</td><td>20</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>old</td><td>CSJ Transformer</td><td>Permutation SHAP</td><td>20</td><td>0</td><td>0</td><td>0</td><td>0</td><td>20</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>old</td><td>CSJ Conformer</td><td>Permutation SHAP</td><td>20</td><td>0</td><td>0</td><td>0</td><td>0</td><td>20</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>old</td><td>LaboroTV Conformer</td><td>Permutation SHAP</td><td>20</td><td>0</td><td>0</td><td>0</td><td>0</td><td>20</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>old</td><td>Whisper large-v3</td><td>Permutation SHAP</td><td>20</td><td>0</td><td>0</td><td>0</td><td>0</td><td>20</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>old</td><td>CSJ Transformer</td><td>LIME</td><td>20</td><td>0</td><td>0</td><td>0</td><td>0</td><td>20</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>old</td><td>CSJ Conformer</td><td>LIME</td><td>20</td><td>0</td><td>0</td><td>0</td><td>0</td><td>20</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>old</td><td>LaboroTV Conformer</td><td>LIME</td><td>20</td><td>0</td><td>0</td><td>0</td><td>0</td><td>20</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>old</td><td>Whisper large-v3</td><td>LIME</td><td>20</td><td>0</td><td>0</td><td>0</td><td>0</td><td>20</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>old</td><td>CSJ Transformer</td><td>Saliency</td><td>20</td><td>0</td><td>0</td><td>0</td><td>0</td><td>20</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>old</td><td>CSJ Conformer</td><td>Saliency</td><td>20</td><td>0</td><td>0</td><td>0</td><td>0</td><td>20</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>old</td><td>LaboroTV Conformer</td><td>Saliency</td><td>20</td><td>0</td><td>0</td><td>0</td><td>0</td><td>20</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>old</td><td>Whisper large-v3</td><td>Saliency</td><td>20</td><td>0</td><td>0</td><td>0</td><td>0</td><td>20</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>old</td><td>CSJ Transformer</td><td>Input × Gradient</td><td>20</td><td>0</td><td>0</td><td>0</td><td>0</td><td>20</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>old</td><td>CSJ Conformer</td><td>Input × Gradient</td><td>20</td><td>0</td><td>0</td><td>0</td><td>0</td><td>20</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>old</td><td>LaboroTV Conformer</td><td>Input × Gradient</td><td>20</td><td>0</td><td>0</td><td>0</td><td>0</td><td>20</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>old</td><td>Whisper large-v3</td><td>Input × Gradient</td><td>20</td><td>0</td><td>0</td><td>0</td><td>0</td><td>20</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>old</td><td>CSJ Transformer</td><td>SmoothGrad</td><td>20</td><td>0</td><td>0</td><td>0</td><td>0</td><td>20</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>old</td><td>CSJ Conformer</td><td>SmoothGrad</td><td>20</td><td>0</td><td>0</td><td>0</td><td>0</td><td>20</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>old</td><td>LaboroTV Conformer</td><td>SmoothGrad</td><td>20</td><td>0</td><td>0</td><td>0</td><td>0</td><td>20</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>old</td><td>Whisper large-v3</td><td>SmoothGrad</td><td>20</td><td>0</td><td>0</td><td>0</td><td>0</td><td>20</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>old</td><td>CSJ Transformer</td><td>Grad-CAM</td><td>20</td><td>0</td><td>0</td><td>0</td><td>0</td><td>20</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>old</td><td>CSJ Conformer</td><td>Grad-CAM</td><td>20</td><td>0</td><td>0</td><td>0</td><td>0</td><td>20</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>old</td><td>LaboroTV Conformer</td><td>Grad-CAM</td><td>20</td><td>0</td><td>0</td><td>0</td><td>0</td><td>20</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>old</td><td>Whisper large-v3</td><td>Grad-CAM</td><td>20</td><td>0</td><td>0</td><td>0</td><td>0</td><td>20</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>old</td><td>CSJ Transformer</td><td>Attention Rollout</td><td>20</td><td>0</td><td>0</td><td>0</td><td>0</td><td>20</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>old</td><td>CSJ Conformer</td><td>Attention Rollout</td><td>20</td><td>0</td><td>0</td><td>0</td><td>0</td><td>20</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>old</td><td>LaboroTV Conformer</td><td>Attention Rollout</td><td>20</td><td>0</td><td>0</td><td>0</td><td>0</td><td>20</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>old</td><td>Whisper large-v3</td><td>Attention Rollout</td><td>20</td><td>0</td><td>0</td><td>0</td><td>0</td><td>20</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>old</td><td>CSJ Transformer</td><td>全保持NNLS</td><td>20</td><td>0</td><td>0</td><td>0</td><td>0</td><td>20</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>old</td><td>CSJ Conformer</td><td>全保持NNLS</td><td>20</td><td>0</td><td>0</td><td>0</td><td>0</td><td>20</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>old</td><td>LaboroTV Conformer</td><td>全保持NNLS</td><td>20</td><td>0</td><td>0</td><td>0</td><td>0</td><td>20</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>old</td><td>Whisper large-v3</td><td>全保持NNLS</td><td>20</td><td>0</td><td>0</td><td>0</td><td>0</td><td>20</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>old</td><td>CSJ Transformer</td><td>絶対IG同面積 Energy</td><td>20</td><td>0</td><td>0</td><td>0</td><td>0</td><td>20</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>old</td><td>CSJ Conformer</td><td>絶対IG同面積 Energy</td><td>20</td><td>0</td><td>0</td><td>0</td><td>0</td><td>20</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>old</td><td>LaboroTV Conformer</td><td>絶対IG同面積 Energy</td><td>20</td><td>0</td><td>0</td><td>0</td><td>0</td><td>20</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>old</td><td>Whisper large-v3</td><td>絶対IG同面積 Energy</td><td>20</td><td>0</td><td>0</td><td>0</td><td>0</td><td>20</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>old</td><td>CSJ Transformer</td><td>絶対IG同面積 Random</td><td>20</td><td>0</td><td>0</td><td>0</td><td>0</td><td>20</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>old</td><td>CSJ Conformer</td><td>絶対IG同面積 Random</td><td>20</td><td>0</td><td>0</td><td>0</td><td>0</td><td>20</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>old</td><td>LaboroTV Conformer</td><td>絶対IG同面積 Random</td><td>20</td><td>0</td><td>0</td><td>0</td><td>0</td><td>20</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>old</td><td>Whisper large-v3</td><td>絶対IG同面積 Random</td><td>20</td><td>0</td><td>0</td><td>0</td><td>0</td><td>20</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>old</td><td>CSJ Transformer</td><td>正IG同面積 Energy</td><td>20</td><td>0</td><td>0</td><td>0</td><td>0</td><td>20</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>old</td><td>CSJ Conformer</td><td>正IG同面積 Energy</td><td>20</td><td>0</td><td>0</td><td>0</td><td>0</td><td>20</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>old</td><td>LaboroTV Conformer</td><td>正IG同面積 Energy</td><td>20</td><td>0</td><td>0</td><td>0</td><td>0</td><td>20</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>old</td><td>Whisper large-v3</td><td>正IG同面積 Energy</td><td>20</td><td>0</td><td>0</td><td>0</td><td>0</td><td>20</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>old</td><td>CSJ Transformer</td><td>正IG同面積 Random</td><td>20</td><td>0</td><td>0</td><td>0</td><td>0</td><td>20</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>old</td><td>CSJ Conformer</td><td>正IG同面積 Random</td><td>20</td><td>0</td><td>0</td><td>0</td><td>0</td><td>20</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>old</td><td>LaboroTV Conformer</td><td>正IG同面積 Random</td><td>20</td><td>0</td><td>0</td><td>0</td><td>0</td><td>20</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>old</td><td>Whisper large-v3</td><td>正IG同面積 Random</td><td>20</td><td>0</td><td>0</td><td>0</td><td>0</td><td>20</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>new</td><td>CSJ Transformer</td><td>絶対IG</td><td>120</td><td>0</td><td>0</td><td>0</td><td>0</td><td>120</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>new</td><td>CSJ Conformer</td><td>絶対IG</td><td>120</td><td>0</td><td>0</td><td>0</td><td>0</td><td>120</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>new</td><td>LaboroTV Conformer</td><td>絶対IG</td><td>120</td><td>0</td><td>0</td><td>0</td><td>0</td><td>120</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>new</td><td>Whisper large-v3</td><td>絶対IG</td><td>120</td><td>0</td><td>0</td><td>0</td><td>0</td><td>120</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>new</td><td>CSJ Transformer</td><td>正IG</td><td>120</td><td>0</td><td>0</td><td>0</td><td>0</td><td>120</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>new</td><td>CSJ Conformer</td><td>正IG</td><td>120</td><td>0</td><td>0</td><td>0</td><td>0</td><td>120</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>new</td><td>LaboroTV Conformer</td><td>正IG</td><td>120</td><td>0</td><td>0</td><td>0</td><td>0</td><td>120</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>new</td><td>Whisper large-v3</td><td>正IG</td><td>120</td><td>0</td><td>0</td><td>0</td><td>0</td><td>120</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>new</td><td>CSJ Transformer</td><td>Occlusion</td><td>120</td><td>0</td><td>0</td><td>0</td><td>0</td><td>120</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>new</td><td>CSJ Conformer</td><td>Occlusion</td><td>120</td><td>0</td><td>0</td><td>0</td><td>0</td><td>120</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>new</td><td>LaboroTV Conformer</td><td>Occlusion</td><td>120</td><td>0</td><td>0</td><td>0</td><td>0</td><td>120</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>new</td><td>Whisper large-v3</td><td>Occlusion</td><td>120</td><td>0</td><td>0</td><td>0</td><td>0</td><td>120</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>new</td><td>CSJ Transformer</td><td>Permutation SHAP</td><td>120</td><td>0</td><td>0</td><td>0</td><td>0</td><td>120</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>new</td><td>CSJ Conformer</td><td>Permutation SHAP</td><td>120</td><td>0</td><td>0</td><td>0</td><td>0</td><td>120</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>new</td><td>LaboroTV Conformer</td><td>Permutation SHAP</td><td>120</td><td>0</td><td>0</td><td>0</td><td>0</td><td>120</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>new</td><td>Whisper large-v3</td><td>Permutation SHAP</td><td>120</td><td>0</td><td>0</td><td>0</td><td>0</td><td>120</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>new</td><td>CSJ Transformer</td><td>LIME</td><td>120</td><td>0</td><td>0</td><td>0</td><td>0</td><td>120</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>new</td><td>CSJ Conformer</td><td>LIME</td><td>120</td><td>0</td><td>0</td><td>0</td><td>0</td><td>120</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>new</td><td>LaboroTV Conformer</td><td>LIME</td><td>120</td><td>0</td><td>0</td><td>0</td><td>0</td><td>120</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>new</td><td>Whisper large-v3</td><td>LIME</td><td>120</td><td>0</td><td>0</td><td>0</td><td>0</td><td>120</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>new</td><td>CSJ Transformer</td><td>Saliency</td><td>120</td><td>0</td><td>0</td><td>0</td><td>0</td><td>120</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>new</td><td>CSJ Conformer</td><td>Saliency</td><td>120</td><td>0</td><td>0</td><td>0</td><td>0</td><td>120</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>new</td><td>LaboroTV Conformer</td><td>Saliency</td><td>120</td><td>0</td><td>0</td><td>0</td><td>0</td><td>120</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>new</td><td>Whisper large-v3</td><td>Saliency</td><td>120</td><td>0</td><td>0</td><td>0</td><td>0</td><td>120</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>new</td><td>CSJ Transformer</td><td>Input × Gradient</td><td>120</td><td>0</td><td>0</td><td>0</td><td>0</td><td>120</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>new</td><td>CSJ Conformer</td><td>Input × Gradient</td><td>120</td><td>0</td><td>0</td><td>0</td><td>0</td><td>120</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>new</td><td>LaboroTV Conformer</td><td>Input × Gradient</td><td>120</td><td>0</td><td>0</td><td>0</td><td>0</td><td>120</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>new</td><td>Whisper large-v3</td><td>Input × Gradient</td><td>120</td><td>0</td><td>0</td><td>0</td><td>0</td><td>120</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>new</td><td>CSJ Transformer</td><td>SmoothGrad</td><td>120</td><td>0</td><td>0</td><td>0</td><td>0</td><td>120</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>new</td><td>CSJ Conformer</td><td>SmoothGrad</td><td>120</td><td>0</td><td>0</td><td>0</td><td>0</td><td>120</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>new</td><td>LaboroTV Conformer</td><td>SmoothGrad</td><td>120</td><td>0</td><td>0</td><td>0</td><td>0</td><td>120</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>new</td><td>Whisper large-v3</td><td>SmoothGrad</td><td>120</td><td>0</td><td>0</td><td>0</td><td>0</td><td>120</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>new</td><td>CSJ Transformer</td><td>Grad-CAM</td><td>120</td><td>0</td><td>0</td><td>0</td><td>0</td><td>120</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>new</td><td>CSJ Conformer</td><td>Grad-CAM</td><td>120</td><td>0</td><td>0</td><td>0</td><td>0</td><td>120</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>new</td><td>LaboroTV Conformer</td><td>Grad-CAM</td><td>120</td><td>0</td><td>0</td><td>0</td><td>0</td><td>120</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>new</td><td>Whisper large-v3</td><td>Grad-CAM</td><td>120</td><td>0</td><td>0</td><td>0</td><td>0</td><td>120</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>new</td><td>CSJ Transformer</td><td>Attention Rollout</td><td>120</td><td>0</td><td>0</td><td>0</td><td>0</td><td>120</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>new</td><td>CSJ Conformer</td><td>Attention Rollout</td><td>120</td><td>0</td><td>0</td><td>0</td><td>0</td><td>120</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>new</td><td>LaboroTV Conformer</td><td>Attention Rollout</td><td>120</td><td>0</td><td>0</td><td>0</td><td>0</td><td>120</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>new</td><td>Whisper large-v3</td><td>Attention Rollout</td><td>120</td><td>0</td><td>0</td><td>0</td><td>0</td><td>120</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>new</td><td>CSJ Transformer</td><td>全保持NNLS</td><td>120</td><td>0</td><td>0</td><td>0</td><td>0</td><td>120</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>new</td><td>CSJ Conformer</td><td>全保持NNLS</td><td>120</td><td>0</td><td>0</td><td>0</td><td>0</td><td>120</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>new</td><td>LaboroTV Conformer</td><td>全保持NNLS</td><td>120</td><td>0</td><td>0</td><td>0</td><td>0</td><td>120</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>new</td><td>Whisper large-v3</td><td>全保持NNLS</td><td>120</td><td>0</td><td>0</td><td>0</td><td>0</td><td>120</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>new</td><td>CSJ Transformer</td><td>絶対IG同面積 Energy</td><td>120</td><td>0</td><td>0</td><td>0</td><td>0</td><td>120</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>new</td><td>CSJ Conformer</td><td>絶対IG同面積 Energy</td><td>120</td><td>0</td><td>0</td><td>0</td><td>0</td><td>120</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>new</td><td>LaboroTV Conformer</td><td>絶対IG同面積 Energy</td><td>120</td><td>0</td><td>0</td><td>0</td><td>0</td><td>120</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>new</td><td>Whisper large-v3</td><td>絶対IG同面積 Energy</td><td>120</td><td>0</td><td>0</td><td>0</td><td>0</td><td>120</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>new</td><td>CSJ Transformer</td><td>絶対IG同面積 Random</td><td>120</td><td>0</td><td>0</td><td>0</td><td>0</td><td>120</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>new</td><td>CSJ Conformer</td><td>絶対IG同面積 Random</td><td>120</td><td>0</td><td>0</td><td>0</td><td>0</td><td>120</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>new</td><td>LaboroTV Conformer</td><td>絶対IG同面積 Random</td><td>120</td><td>0</td><td>0</td><td>0</td><td>0</td><td>120</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>new</td><td>Whisper large-v3</td><td>絶対IG同面積 Random</td><td>120</td><td>0</td><td>0</td><td>0</td><td>0</td><td>120</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>new</td><td>CSJ Transformer</td><td>正IG同面積 Energy</td><td>120</td><td>0</td><td>0</td><td>0</td><td>0</td><td>120</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>new</td><td>CSJ Conformer</td><td>正IG同面積 Energy</td><td>120</td><td>0</td><td>0</td><td>0</td><td>0</td><td>120</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>new</td><td>LaboroTV Conformer</td><td>正IG同面積 Energy</td><td>120</td><td>0</td><td>0</td><td>0</td><td>0</td><td>120</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>new</td><td>Whisper large-v3</td><td>正IG同面積 Energy</td><td>120</td><td>0</td><td>0</td><td>0</td><td>0</td><td>120</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>new</td><td>CSJ Transformer</td><td>正IG同面積 Random</td><td>120</td><td>0</td><td>0</td><td>0</td><td>0</td><td>120</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>new</td><td>CSJ Conformer</td><td>正IG同面積 Random</td><td>120</td><td>0</td><td>0</td><td>0</td><td>0</td><td>120</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>new</td><td>LaboroTV Conformer</td><td>正IG同面積 Random</td><td>120</td><td>0</td><td>0</td><td>0</td><td>0</td><td>120</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>new</td><td>Whisper large-v3</td><td>正IG同面積 Random</td><td>120</td><td>0</td><td>0</td><td>0</td><td>0</td><td>120</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>observe</td><td>CSJ Transformer</td><td>絶対IG</td><td>1000</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1000</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>observe</td><td>CSJ Conformer</td><td>絶対IG</td><td>1000</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1000</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>observe</td><td>LaboroTV Conformer</td><td>絶対IG</td><td>1000</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1000</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>observe</td><td>Whisper large-v3</td><td>絶対IG</td><td>1000</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1000</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>observe</td><td>CSJ Transformer</td><td>正IG</td><td>1000</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1000</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>observe</td><td>CSJ Conformer</td><td>正IG</td><td>1000</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1000</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>observe</td><td>LaboroTV Conformer</td><td>正IG</td><td>1000</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1000</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>observe</td><td>Whisper large-v3</td><td>正IG</td><td>1000</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1000</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>observe</td><td>CSJ Transformer</td><td>Occlusion</td><td>1000</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1000</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>observe</td><td>CSJ Conformer</td><td>Occlusion</td><td>1000</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1000</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>observe</td><td>LaboroTV Conformer</td><td>Occlusion</td><td>1000</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1000</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>observe</td><td>Whisper large-v3</td><td>Occlusion</td><td>1000</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1000</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>observe</td><td>CSJ Transformer</td><td>Permutation SHAP</td><td>1000</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1000</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>observe</td><td>CSJ Conformer</td><td>Permutation SHAP</td><td>1000</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1000</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>observe</td><td>LaboroTV Conformer</td><td>Permutation SHAP</td><td>1000</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1000</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>observe</td><td>Whisper large-v3</td><td>Permutation SHAP</td><td>1000</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1000</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>observe</td><td>CSJ Transformer</td><td>LIME</td><td>1000</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1000</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>observe</td><td>CSJ Conformer</td><td>LIME</td><td>1000</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1000</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>observe</td><td>LaboroTV Conformer</td><td>LIME</td><td>1000</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1000</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>observe</td><td>Whisper large-v3</td><td>LIME</td><td>1000</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1000</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>observe</td><td>CSJ Transformer</td><td>Saliency</td><td>1000</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1000</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>observe</td><td>CSJ Conformer</td><td>Saliency</td><td>1000</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1000</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>observe</td><td>LaboroTV Conformer</td><td>Saliency</td><td>1000</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1000</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>observe</td><td>Whisper large-v3</td><td>Saliency</td><td>1000</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1000</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>observe</td><td>CSJ Transformer</td><td>Input × Gradient</td><td>1000</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1000</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>observe</td><td>CSJ Conformer</td><td>Input × Gradient</td><td>1000</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1000</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>observe</td><td>LaboroTV Conformer</td><td>Input × Gradient</td><td>1000</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1000</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>observe</td><td>Whisper large-v3</td><td>Input × Gradient</td><td>1000</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1000</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>observe</td><td>CSJ Transformer</td><td>SmoothGrad</td><td>1000</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1000</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>observe</td><td>CSJ Conformer</td><td>SmoothGrad</td><td>1000</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1000</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>observe</td><td>LaboroTV Conformer</td><td>SmoothGrad</td><td>1000</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1000</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>observe</td><td>Whisper large-v3</td><td>SmoothGrad</td><td>1000</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1000</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>observe</td><td>CSJ Transformer</td><td>Grad-CAM</td><td>1000</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1000</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>observe</td><td>CSJ Conformer</td><td>Grad-CAM</td><td>1000</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1000</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>observe</td><td>LaboroTV Conformer</td><td>Grad-CAM</td><td>1000</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1000</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>observe</td><td>Whisper large-v3</td><td>Grad-CAM</td><td>1000</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1000</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>observe</td><td>CSJ Transformer</td><td>Attention Rollout</td><td>1000</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1000</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>observe</td><td>CSJ Conformer</td><td>Attention Rollout</td><td>1000</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1000</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>observe</td><td>LaboroTV Conformer</td><td>Attention Rollout</td><td>1000</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1000</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>observe</td><td>Whisper large-v3</td><td>Attention Rollout</td><td>1000</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1000</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>observe</td><td>CSJ Transformer</td><td>全保持NNLS</td><td>1000</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1000</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>observe</td><td>CSJ Conformer</td><td>全保持NNLS</td><td>1000</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1000</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>observe</td><td>LaboroTV Conformer</td><td>全保持NNLS</td><td>1000</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1000</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>observe</td><td>Whisper large-v3</td><td>全保持NNLS</td><td>1000</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1000</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>observe</td><td>CSJ Transformer</td><td>絶対IG同面積 Energy</td><td>1000</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1000</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>observe</td><td>CSJ Conformer</td><td>絶対IG同面積 Energy</td><td>1000</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1000</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>observe</td><td>LaboroTV Conformer</td><td>絶対IG同面積 Energy</td><td>1000</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1000</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>observe</td><td>Whisper large-v3</td><td>絶対IG同面積 Energy</td><td>1000</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1000</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>observe</td><td>CSJ Transformer</td><td>絶対IG同面積 Random</td><td>1000</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1000</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>observe</td><td>CSJ Conformer</td><td>絶対IG同面積 Random</td><td>1000</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1000</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>observe</td><td>LaboroTV Conformer</td><td>絶対IG同面積 Random</td><td>1000</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1000</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>observe</td><td>Whisper large-v3</td><td>絶対IG同面積 Random</td><td>1000</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1000</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>observe</td><td>CSJ Transformer</td><td>正IG同面積 Energy</td><td>1000</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1000</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>observe</td><td>CSJ Conformer</td><td>正IG同面積 Energy</td><td>1000</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1000</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>observe</td><td>LaboroTV Conformer</td><td>正IG同面積 Energy</td><td>1000</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1000</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>observe</td><td>Whisper large-v3</td><td>正IG同面積 Energy</td><td>1000</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1000</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>observe</td><td>CSJ Transformer</td><td>正IG同面積 Random</td><td>1000</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1000</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>observe</td><td>CSJ Conformer</td><td>正IG同面積 Random</td><td>1000</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1000</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>observe</td><td>LaboroTV Conformer</td><td>正IG同面積 Random</td><td>1000</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1000</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>observe</td><td>Whisper large-v3</td><td>正IG同面積 Random</td><td>1000</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1000</td><td>0</td><td>0</td><td>0</td></tr>
</tbody></table></div>

</details>
