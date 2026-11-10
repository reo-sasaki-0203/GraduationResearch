# トークンIGから発音部分を取り出せるか：仮説・先行研究・検証計画

調査日：2026-11-10。このページは研究方針の検討です。「WhisperのトークンごとのIGでメルをマスクし再構成すると、そのトークンの発音だけを取り出せる」は**検証すべき仮説**であり、成立済みの手法ではありません。今回実行した実験は[同じ10音声のトークン・単語IGと4保持率](../../../../../ASR/whisper_ig_reconstruction/notes/research_hub/token-word-ig.html)だけです。以下のアライメント、追加指標、基準比較、IG再計算、モデル比較は**提案・未実施**です。

[研究計画](../../../../../ASR/whisper_ig_reconstruction/notes/research_hub/plan.html) · [スコアの定義](../../../../../ASR/whisper_ig_reconstruction/notes/research_hub/score.html) · [結果一覧](../../../../../ASR/whisper_ig_reconstruction/notes/research_hub/results.html)

## 研究上の判断

「認識の根拠を音声として聴く」ことには既にL2I・L-MACという先行研究があり、ASRについてもフレーム選択による説明研究があります。したがって、単にIG→マスク→音声化したことや、Whisperを使ったことだけを新規性にしません。候補となる問いは、**自己回帰ASRの出力トークンを条件にした寄与が、実際の日本語発音の位置・内容にどの程度対応するか、どこで破綻するか**です。これは本ページの調査からの提案であり、新規性の立証ではありません。[L2I](https://proceedings.neurips.cc/paper_files/paper/2022/hash/e53280d73dd5389e820f4a6250365b0e-Abstract-Conference.html)、[L-MAC](https://proceedings.mlr.press/v235/paissan24a.html)、[ASRの説明](https://arxiv.org/abs/2302.14062)。

仮説が成立すれば、モデルが何を根拠に個々の認識をしたかを試聴する診断、誤認識・雑音への依存の分析、分散した時間周波数証拠と単純な時間切り出しの比較に価値があり得ます。一方、語の音声クリップが欲しいだけなら、正しい転記と強制アライメントから切り出す方が簡単な可能性があります。教材、検索、個別発音分析への実用価値は、聴取可能性・正確さ・計算費用を既存手法に対して確認するまで未検証です。音声匿名化や特定語の完全消去にも現状では使えません。[MFA](https://www.isca-archive.org/interspeech_2017/mcauliffe17_interspeech.html)、[WhisperX](https://arxiv.org/abs/2303.00747)。

## 三つの主張を分ける

1. **モデル内の寄与**：固定した前置トークンの下で、入力セルが対象トークンの対数確率を、ある基準からどれだけ変えるか。IGが直接扱うのはこれです。
2. **言語音の位置**：対象語・音素を人間が実際に発音した時間範囲。転記と人手修正したアライメントで別に決めます。
3. **再構成音の内容**：その範囲の音が残り、それ以外の発話や雑音を十分除けたか。聴取・参照信号・別ASRなどで別に評価します。

IGのcompleteness（寄与の総和がスコア差に合う性質）は1の検査で、2・3の証明ではありません。音響的に同じ部分が複数トークンの証拠になり、あるトークンが前後の音や話者情報を使うことも可能です。時間周波数セルの集合は、独立した音源の集合とも限りません。このため「認識に寄与した入力＝そのトークンの発音」と置く論理には欠落があります。[IG原論文](https://proceedings.mlr.press/v70/sundararajan17a.html)、[音素認識のXAI評価](https://arxiv.org/abs/2305.18011)。

## 論点ごとの説明案・検証・残る問題

以下で「提案」は根拠に基づいて考えた検証案であり、実験結果ではありません。

|論点・想定質問|根拠と説明案|解決策候補・検証方法|残る問題・現在の判定|
|---|---|---|---|
|何のために取り出すのか、何が面白いか|可聴化はヒートマップを読めない人にもモデルの依存先を示し得る。L2I・L-MACが既に同じ方向を研究 [R5–6]|まず用途を「ASRの語ごとの依存の診断」に絞り、同一音声の寄与・正解発音・聴取を照合。誤認識理由の発見に役立つかも評価|診断を実際に改善する証拠なし。単なる試聴UIに留まる可能性。実用性は未検証|
|既存のアライメント・切り出しで十分か|MFA・WhisperXは文字と時間の対応を与える [R3–4]。IGはモデルスコアへの依存を扱う|人手修正境界での時間切り出しと、同じ時間予算・保持面積のマスクを対照にする。非局所の証拠が診断に有益か調べる|抽出性能が同等以下で独自の診断価値もなければ、抽出手法としての意義は弱い。現時点で優位性なし|
|既存の音声分離との違いは|Conv-TasNetは混合話者の音源復元を学習する [R9]。本仮説は出力トークン条件の事後寄与|話者分離と語抽出を別課題として定義。必要なら分離・強調＋アライメントを強い対照候補にする|発話中の単語は独立音源ではない。IGに音源推定の保証はなく、教師なし分離と呼べない|
|なぜWhisperか、他モデルでもよいのか|多言語の学習と公開重みがあり、既存runとの整合、固定列の微分が可能 [R2]。これは再現性上の選択理由|まず版・精度・frontendを固定。将来はCTC型ASRとの比較で自己回帰文脈の影響を切り分ける|Whisperの最適性・日本語での一般性は未検証。large-v3の設定は本研究のローカル記録から確認し、2023原論文の全設定と同一とは扱わない|
|なぜメルなのか、波形/STFTではだめか|メルはWhisperが実際に受け取る入力で、勾配対象と対応する。周波数圧縮・対数化・床処理を含むため可逆ではない [R2,R11]|現行128メル帯域、FFT400、hop160、16kHzを固定。線形メルパワーへマスクしNNLSでSTFTパワーを推定、元位相でiSTFT。WAVを再分析した実メルを必ず表示|メルの逆は一意でなく、正解の位相は得られない。NNLS未収束・目標/実メル差が残る。完全な逆変換には現時点で解決策なし|
|位相・復元器が見かけの結果を作らないか|L2I・L-MACも元位相を使うが、それで位相が正しいとはならない。WaveGlowはメルから高品質音を生成する別方向 [R5–6,R11]|未マスクの再構成だけの対照を設ける。目標メルと実メルの差、NNLS残差、聴感を別軸に。将来の位相法・vocoder比較は条件を分ける|生成器は入力にない成分を補う可能性。聴きやすさと根拠への忠実性は同じでない。今回の復元誤差の解消は未達|
|正IGなら発音を残すのか、負IGは不要か|IGの符号は基準からのスコア増減で、音声/雑音ラベルではない [R1]。前後音や雑音が識別の証拠になり得る|正IG、絶対IG、負IG、ランダム、エネルギー、時間切り出しを面積統制して比較する案|正IGだけで対象発音が残る保証なし。必要な負寄与や冗長な低寄与を消す可能性。未検証|
|保持率95%は音声の95%か|保持率は正のIG総和に対する割合。エネルギー・時間・面積ではない。非線形モデルでセル間相互作用もある [R1,R10]|95/90/80/60を同じ音声で比較し、保持セル面積・エネルギー・時間支持を別々に記録。面積を揃えた対照を将来用意|累積IGが大きくてもマスク後の確率保持を保証しない。最良保持率のテスト結果による後付け選択を避ける|
|トークンはどの音に対応するのか|日本語のbyte BPEは単語や文字境界をまたぎ得る。Sudachiは別の短単位分割 [R12]。PDSMは音素境界による説明を検討 [R8]|今回の文字/byte範囲照合を使い、厳密対応と境界内近似を分ける。将来の時間評価は日本語語または音素に限定して人手対応を作る|byteの一部分は独立に発音されない。重なる全文トークンの合算は語のみの確率ではない。厳密化は現時点で解決策なし|
|前の文脈だけで認識できるのでは|固定前置列により言語的な予測可能性を含む条件付き確率になる [R2]。無音基準でも後続語を高く予測し得る|将来、無音スコア・対象音の除去・文脈変更・free decodingを分けて比較。固定文脈評価と文脈なし評価を混ぜない|固定列でスコアが高いことは、出力音を単独で聴いて分かる証明にならない。寄与を音響と言語に一意分解する方法は本研究で未確立|
|誤認識した語にも「正しい発音」があるか|出力トークンはモデルの仮説であり真の発話ではない。Wuらも転記説明と正しさ判定を課題にする [R7]|正解転記との対応を作り、誤認識・挿入・削除を別群にする。存在しない対象は「抽出不能」と評価し、失敗を落とさない|幻覚語や挿入語に同名の参照音声は存在しない。成功例だけに限定すれば研究の問いが変わる|
|IGの基準・積分品質が悪くないか|IGは基準依存で、直線上の特徴が実音声の分布内とは限らない [R1]。今回226トークン中180が既存delta基準未達|元baseline・経路・版・精度・点数とdeltaを保持。将来、点数/精度の収束・基準違いの順位/マスク安定性を先に調べる|今回追加IG再計算はなし。品質未達を解決済みとしない。delta合格だけでも局所化の妥当性や安定性は未保証|
|単語合算は本当に正しいか|共通経路と固定文脈なら微分と積分の線形性でスコア合計のIGも合計になる [R1]。正値化と合計は交換できない|signedを先に足してから正値選択。元トークンを重複なく各語内で1回合算、範囲・共有を記録。語のdeltaと構成トークンの未達を両方表示|共有トークンは語間重複。合算で誤差相殺も起こる。線形性は音声分離の線形性を意味しない|
|本当に「だけ」を抽出できたか|XAIの忠実性・人の理解可能性・発音区間の一致は独立。見た目だけの評価は不十分 [R6,R13]|下記の三軸評価。対象語正答・非対象語漏出・境界外エネルギー・信号歪みを同時に確認し、ブラインド聴取を含める|単一指標では十分でない。全員が同じ境界に合意できるとは限らず、共調音により純粋な語の正解も曖昧|
|他人から「時間と計算量が割に合わない」と言われたら|IGは積分点×本文トークンの逆伝播が必要。学習型説明器や強制アライメントとは費用構造が違う [R5–7]|時間・GPUメモリ・再構成時間を記録し、診断精度/試聴負担と比較。今回の追加保持率はIG再利用で費用を抑える|大規模処理の効率性を立証していない。一般用途の切り出しとして不利なら診断用に絞る|

## 主要な先行研究

各項目の「示唆」は今回の研究への解釈・提案です。原論文が今回のWhisper日本語トークン実験を検証したという意味ではありません。タイトル、著者、年、一次資料の書誌と要旨を確認し、特に近いR5–8は手法説明も照合しました。

### R1：寄与の定義

**Axiomatic Attribution for Deep Networks** — Mukund Sundararajan, Ankur Taly, Qiqi Yan、2017（ICML）。[論文](https://proceedings.mlr.press/v70/sundararajan17a.html)。目的は予測を入力特徴へ帰属させること。基準からの経路上で勾配を積分するIGを定義。今回と共通なのは寄与計算そのもの。相違は、原論文の公理が発音局所化や音源分離を保証しない点。示唆：スコア・基準・経路を明示し、completenessと抽出評価を分ける。

### R2：ASRを選ぶ根拠

**Robust Speech Recognition via Large-Scale Weak Supervision** — Alec Radford, Jong Wook Kim, Tao Xu, Greg Brockman, Christine McLeavey, Ilya Sutskever、2023（ICML、preprint 2022）。[論文](https://proceedings.mlr.press/v202/radford23a.html)。大規模な弱教師付き音声・転記対から多言語encoder-decoderを学習し、汎化を評価。共通：メル入力と自己回帰の文字出力。相違：原論文の目的はASRで、出力語の音声抽出ではない。示唆：前置列、認識誤り、音響と言語文脈の影響を固定条件として記録する。

### R3–4：音声と文字を時間で結び付ける既存の選択肢

**Montreal Forced Aligner: Trainable Text-Speech Alignment Using Kaldi** — Michael McAuliffe, Michaela Socolof, Sarah Mihuc, Michael Wagner, Morgan Sonderegger、2017（Interspeech）。[論文](https://www.isca-archive.org/interspeech_2017/mcauliffe17_interspeech.html)。既知転記と発音辞書・音響モデルで単語/音素境界を推定。共通：対象語の音声位置を得たい目的。相違：転記との時間整列であり認識器の寄与ではない。示唆：時間切り出しの有力対照、人手修正した境界の初期案。ただし自動境界を正解と断定しない。

**WhisperX: Time-Accurate Speech Transcription of Long-Form Audio** — Max Bain, Jaesung Huh, Tengda Han, Andrew Zisserman、2023（Interspeech）。[論文](https://arxiv.org/abs/2303.00747)、[会議版PDF](https://www.isca-archive.org/interspeech_2023/bain23_interspeech.pdf)。VADで区切りWhisperで転記し、外部音素モデルの強制整列で単語時刻を得る。共通：Whisper出力を細かく音声へ対応させる。相違：時刻が目的で、IGの時間周波数選択ではない。示唆：Whisperを使うだけの新規性は弱い。日本語でのモデル適用と誤転記の扱いを独立確認する。

### R5–6：寄与・説明を聴ける形にする直接の関連研究

**Listen to Interpret: Post-hoc Interpretability for Audio Networks with NMF** — Jayneel Parekh, Sanjeel Parekh, Pavlo Mozharovskyi, Florence d’Alché-Buc, Gaël Richard、2022（NeurIPS）。[論文](https://proceedings.neurips.cc/paper_files/paper/2022/hash/e53280d73dd5389e820f4a6250365b0e-Abstract-Conference.html)、[本文PDF](https://papers.nips.cc/paper/2022/file/e53280d73dd5389e820f4a6250365b0e-Paper-Conference.pdf)。音分類ネットの中間特徴から学習済みNMF辞書の時間活性を推定し、重要成分のsoft maskと元位相から可聴説明を作る。共通：判断根拠をマスク・再構成して聴く。相違：学習する説明器・NMF成分・分類ラベルであり、固定ASR出力トークンのIGではない。示唆：忠実性と理解可能性の評価を分ける。元位相の限界も先行研究に既に存在する。

**Listenable Maps for Audio Classifiers** — Francesco Paissan, Mirco Ravanelli, Cem Subakan、2024（ICML）。[論文](https://proceedings.mlr.press/v235/paissan24a.html)、[本文](https://openreview.net/pdf?id=kAfYYg6PX8)。分類器にdecoderを付け、残す音での予測保持と除く音での予測低下を学習する。STFT振幅マスクと元位相の逆変換で聴ける説明を得る。共通：マスク→再構成と予測の根拠。相違：学習型マスク・音分類でありトークンごとのIGではない。示唆：可聴化だけでは新規ではなく、保持・除去の両方、他手法、利用者評価が必要。

**Listenable Maps for Zero-Shot Audio Classifiers** — Francesco Paissan, Luca Della Libera, Mirco Ravanelli, Cem Subakan、2024（NeurIPS）。[論文](https://arxiv.org/abs/2405.17615)、[会議版](https://proceedings.neurips.cc/paper_files/paper/2024/file/77fd93190fdcfc26023c3cbb1ce8bcf0-Paper-Conference.pdf)。CLAPのテキスト・音声類似度に忠実な説明器を学習。共通：テキスト条件付きの音声説明。相違：ASRの自己回帰トークン確率ではなくテキスト・音声の類似度。示唆：「テキストを指定して説明音を得る」だけでも先行例がある。

**LMAC-TD: Producing Time Domain Explanations for Audio Classifiers** — Eleonora Mancini, Francesco Paissan, Mirco Ravanelli, Cem Subakan、2024 preprint（ここでは確認したpreprint年を使用）。[論文](https://arxiv.org/abs/2409.08655)。SepFormerを取り込んだdecoderで時間領域の説明を作り、可聴品質と忠実性を評価。共通：聴ける説明の品質問題。相違：波形領域の学習型説明、ASRトークンIGではない。示唆：メル逆変換は唯一の道ではない。今回その追加比較は行わない。

### R7–8：ASRと音素の説明・正解との照合

**Explanations for Automatic Speech Recognition** — Xiaoliang Wu, Peter Bell, Ajitha Rajan、2023（ICASSP）。[論文](https://arxiv.org/abs/2302.14062)、[大学の著者版・書誌](https://www.research.ed.ac.uk/en/publications/explanations-for-automatic-speech-recognition/)。SFL・Causal方式とLIMEをASRへ適用し、転記を支える小さい音声フレーム集合を求める。共通：認識出力を支える入力部分。相違：主にフレーム摂動・転記の保持であり、個別トークンのメルIGを逆変換する設計ではない。示唆：ASR説明という目的自体も既存。最小性・十分性を比較に取り入れ、物理的な発音との一致は別に調べる。

**Can We Trust Explainable AI Methods on ASR? An Evaluation on Phoneme Recognition** — Xiaoliang Wu, Peter Bell, Ajitha Rajan、2023 preprint / 2024 ICASSP。[一次資料](https://arxiv.org/abs/2305.18011)、[本文](https://arxiv.org/html/2305.18011v1)。TIMITの音素認識を制御環境とし、専門家の境界正解に対してLIMEの時間・周波数分割を評価。共通：説明が発音位置に対応するかという問い。相違：音素分類とLIMEで、Whisperの日本語byteトークンではない。示唆：既存モデルのスコア保持だけで完結せず、独立した人手境界を使う。

**Phoneme Discretized Saliency Maps for Explainable Detection of AI-Generated Voice** — Shubham Gupta, Mirco Ravanelli, Pascal Germain, Cem Subakan、2024（Interspeech）。[論文](https://www.isca-archive.org/interspeech_2024/gupta24b_interspeech.html)。音素境界を使ってsaliency mapを離散化し、合成音検出の説明を評価。共通：言語的単位と音声の説明を結ぶ。相違：合成音検出が対象で、ASRの語ごとの確率スコアではない。示唆：語/音素の境界に寄せること自体も先行例があり、単位の選択と境界誤差の評価が必要。

### R9–11：分離・選択・逆変換

**Conv-TasNet: Surpassing Ideal Time-Frequency Magnitude Masking for Speech Separation** — Yi Luo, Nima Mesgarani、2019（IEEE/ACM TASLP、preprint 2018）。[論文](https://arxiv.org/abs/1809.07454)。学習した時間領域encoder表現へマスクを掛けdecoderで話者波形を復元。共通：特徴表現にマスクを掛け波形へ戻す。相違：教師付き音源分離の損失と正解音源がある。示唆：時間周波数振幅だけと元位相に依存する制約を意識し、語抽出を話者分離と同一視しない。

**Interpretable Explanations of Black Boxes by Meaningful Perturbation** — Ruth C. Fong, Andrea Vedaldi、2017（ICCV）。[論文](https://arxiv.org/abs/1704.03296)。画像に明示した摂動を加え、判断を変える小さい領域を最適化。共通：マスクを通した判断の説明。相違：画像領域と最適化マスクであり、IGでも音声復元でもない。示唆：入力をゼロ化する意味と分布外効果を定義し、単に見栄えで選ばない。

**Understanding Deep Image Representations by Inverting Them** — Aravindh Mahendran, Andrea Vedaldi、2015（CVPR）。[論文](https://openaccess.thecvf.com/content_cvpr_2015/html/Mahendran_Understanding_Deep_Image_2015_CVPR_paper.html)。画像特徴と事前制約から画像を再構成し、表現に残る情報を調べる。共通：中間表現からの復元を通じた解釈。相違：元特徴を反転する問題で、クラス寄与マスクの音源抽出ではない。示唆：復元物は表現と復元器の両方に依存するため、元の実体と同一としない。

**WaveGlow: A Flow-based Generative Network for Speech Synthesis** — Ryan Prenger, Rafael Valle, Bryan Catanzaro、2019（ICASSP、preprint 2018）。[著者preprint](https://arxiv.org/abs/1811.00002)。メル条件付きのflowモデルで波形を生成。共通：メルから波形を得る。相違：学習した音声事前分布を使い、元音の厳密な逆変換ではない。示唆：音質向上案にはなるが、生成補完と入力根拠の保存を分ける必要がある。

### R12–13：言語単位と説明評価の周辺研究

**Sudachi: a Japanese Tokenizer for Business** — Kazuma Takaoka, Sorami Hisamoto, Noriko Kawahara, Miho Sakamoto, Yoshitaka Uchida, Yuji Matsumoto、2018（LREC）。[論文](https://aclanthology.org/L18-1355/)。複数粒度の日本語形態素解析器・辞書を開発。共通：日本語の言語単位を定義する。相違：音声・IG・音声復元を扱わない。示唆：分割法・辞書・モードを固定し、Whisper BPEの単位と区別する。

**Rationalizing Neural Predictions** — Tao Lei, Regina Barzilay, Tommi Jaakkola、2016（EMNLP）。[論文](https://aclanthology.org/D16-1011/)。予測に十分で短く連続した入力語句をgenerator/encoderで学習。共通：モデルの予測を保つ入力部分を説明とする。相違：自然言語の入力語句選択で、出力トークンから音声へ帰属する課題ではない。示唆：十分性だけでなく、短さ・連続性や人手の根拠との一致を別に評価する。

**Learning to Explain: An Information-Theoretic Perspective on Model Interpretation** — Jianbo Chen, Le Song, Martin J. Wainwright, Michael I. Jordan、2018（ICML）。[論文](https://proceedings.mlr.press/v80/chen18j.html)。各例の応答に有益な特徴部分集合を相互情報量の変分近似で学習。共通：予測情報を残す特徴選択。相違：学習する説明器と一般特徴選択で、発音信号の復元ではない。示唆：情報の保持と元の原因・物理的音源の特定を区別する。

**Sanity Checks for Saliency Maps** — Julius Adebayo, Justin Gilmer, Michael Muelly, Ian Goodfellow, Moritz Hardt, Been Kim、2018（NeurIPS）。[論文](https://arxiv.org/abs/1810.03292)。重み・データの無作為化への依存を検査し、見た目の妥当性だけでは説明の信頼性を判断できないことを示す。共通：saliencyの検査。相違：主な実験は画像で、今回のWhisper IGの失敗を直接示したものではない。示唆：数値delta・マスク安定性・別の正解との照合を組み合わせる。無作為化検査を通過しても発音抽出の証明にはならない。

## 評価設計案：「だけ取り出せた」を反証できるようにする

**正解の作り方（未実施）**：まず同じ10音声の正解転記と認識文を照合し、語の置換・挿入・削除を明記します。正しく認識された厳密対応語について、clear音声に日本語の語/音素境界を付け、強制アライメントの結果を人が修正します。複数人で境界の揺れを記録し、共調音を含む前後余裕付き区間も併記。単語境界に唯一の物理的正解があるとは仮定しません。誤認識語を消さず、対応不能群として別に集計します。

単語の参照波形はclearの対象区間を元時間軸上に残して他をゼロにした信号とし、端点の処理を固定します。これは評価用の操作的定義であり、自然に発音された独立語音源の真値ではありません。時間整列を崩したクリップ同士のSI-SDR比較や、全文cleanに対する誤差を語抽出成功の代わりに使うことは避けます。

|評価軸|対照と測定案|分かること・分からないこと|
|---|---|---|
|モデルへの忠実性|元音、マスク保持部、除去部を同じ固定文脈で再採点。対象語合計スコアの保持差と、除去による低下を測定。別にfree decodingと別ASRも確認|保持だけでなく必要性を点検できる。ただし固定文脈やモデル自身の誤りから独立ではない|
|時間局所化|正のIG質量の人手区間内割合、同面積マスクの時間支持IoU・precision/recall、境界からの距離を測定。ランダム・energy・時間切り出し・gradient系を同じ面積で比較|発音位置と寄与の対応を測れる。時間一致だけでは周波数内容や聴感を保証しない|
|抽出信号の品質|参照語との時間を合わせたSI-SDR、WAV由来実メル誤差、対象区間内の残存と区間外の漏出エネルギーを別々に測る。未マスクNNLS再構成を対照にする|復元器の歪みとマスクの損失を切り分ける。無音付近では比が不安定なので分母と欠測規則を事前固定|
|人間に何が聞こえるか|条件を伏せた聴取で対象語の書き取り、余分な語の書き取り、明瞭度・不自然さを評価。元語を見せない評価と見せる評価を分ける|対象の可聴性と漏出を直接点検。ただし聞き手差・予備知識・反復効果があり、十分な人数と条件順の統制が必要|
|安定性と費用|IG点数/精度/基準/文脈/保持率ごとのdelta、順位相関、同面積Jaccard、語単位の失敗率、処理時間/メモリを比較|説明が設定に敏感かを測る。どこまで変動を許すかは実験前に定義する|

対照候補の優先順は、(a) 人手修正した時間切り出し、(b) 未マスクのNNLS再構成、(c) 同じ保持面積のランダム・エネルギー、(d) 絶対IG・単純勾配/摂動、(e) 実装可能性を確認した学習型説明器です。現行10件の同じ保持率でも面積は同じとは限らないため、保持率比較と面積統制比較を分けます。語を独立な大量標本として扱わず、発話ごとの集計と対応比較を基本にし、探索用10件での後付け最適化は一般性能として主張しません。

## 優先する仮説と、その結果に応じた判断

|優先|反証可能な仮説|次に検証する内容（すべて未実施）|結果に応じた方針|
|---|---|---|---|
|P0|現在のIGは数値・設定に対して十分安定している|品質未達を含む固定対象で積分収束と同面積マスク安定性を確認。合算での誤差相殺も分ける|不安定なら発音抽出の主張を止め、数値計算・基準の検討を先にする。高精度でも不安定なら別の説明法を検討|
|P1|対象語IGは、対象外語や同面積対照より人手の発音区間へ集中する|厳密対応で正しく認識した語から境界正解を作り、発話単位の対照比較をする|集中しなければ「発音部分抽出」の仮説を棄却/限定し、分散したASR依存の可視化へ目的変更|
|P2|IGマスク後の音は、同面積対照より対象語を保ち、他語の漏出が少ない|独立聴取・別ASR・区間内残存/区間外漏出・復元対照を併用|スコアのみ保ち聴取不能なら、音声抽出成功とはしない。復元器が原因なら復元の研究を別課題にする|
|P3|単語集約や保持率の選択は、安定した意味のある改善をもたらす|厳密/近似、短語/長語、正解/誤認識、4保持率を区別。面積と語内トークン数の交絡を統制|近似だけの効果なら対応方法を再考。改善が再現しなければ最適保持率や単語化の利点を主張しない|
|P4|既存手法に対し、計算費用に見合う診断価値がある|時間切り出し・強い説明器と比較し、発見できた依存/誤りと試聴負担を評価|既存法で十分なら実用抽出器としての開発をやめる。系統的な不一致・失敗の知見が得られればASR解釈研究として整理|

合格しきい値は結果を見て都合よく決めず、境界注釈の誤差幅・用途で必要な正答/漏出を基に別途事前登録する必要があります。現時点でその具体値を正当化する根拠はなく、**未決定**です。今回はタスク1の範囲を超える実験を実行していません。

## 調査した範囲と限界

検索範囲は、音声のASR説明・音素境界・強制整列、音分類の可聴説明・マスキング、音源分離、画像の摂動説明・特徴逆変換、自然言語のrationale・特徴選択、メル条件付き音声生成。検索語は `speech recognition integrated gradients explanation`、`Explanations for Automatic Speech Recognition`、`listenable saliency reconstruction`、`Listen to Interpret NMF`、`Listenable Maps`、`WhisperX forced alignment`、`phoneme saliency`、`meaningful perturbation`、`rationalizing neural predictions`、`inverting representations` などです。

PMLR・NeurIPS・ISCA・ACL・著者所属大学・著者arXivを優先し、各リンクの実在と書誌・要旨を確認。R5–6の本文のマスク/復元・評価、R7のASRフレーム説明、R8の正解音素境界を使う設定も確認しました。全関連研究の網羅的レビュー、全実装の再現、2026年までの全引用網羅、日本語への適用可否確認は行っていません。Griffin–Lim、SoundLIME、AttHearなども検索で候補に入りましたが、このページで主要手法として詳細を検証した一覧は上記です。「完全に同じ例が検索で見つからなかった」ことを独創性の証明にはしません。

最終的な新規性の候補は、既存の可聴説明を踏まえた**日本語の自己回帰ASRでのトークン/単語寄与と発音区間の対応・不一致を、品質と対応近似を隠さず評価すること**。その価値が既存の音素認識XAI評価を超えるかは、比較と追加の文献精査まで未検証です。
