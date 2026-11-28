# 寄与度手法・認識器・混合比の実験結果

雑音の混じった音声から、音声認識モデルが判断に使う部分を残すと、文字起こしは良くなるでしょうか。2026年11月25〜27日に行った3案と、それぞれの追加実験の結果です。

<ul><li><a href="#attribution">案①・追加①　基準と寄与度手法</a></li><li><a href="#cross-asr">案②・追加②　生成ASRとSNR</a></li><li><a href="#dominance">案③・追加③　声の優勢度</a></li></ul>

**ASR**は音声を文字に起こす仕組みです。このページでは、どの音を残すかを決める側を「生成ASR」、出来上がった音を文字に起こす側を「評価器」と呼びます。Reazonは再構成に使っていない評価器です。**XAI**は、AIが何を手がかりに判断したかを調べる方法の総称です。

**CER**は文字の置き換え・抜け・余分な文字の合計を、正解の文字数で割った値です。小さいほど正確です。**ΔCER**は再構成音と元の混合音のCERの差で、たとえば20%から16%に下がると−4ポイント（pp）です。**SNR**は声と雑音の強さの比です。0 dBでは両者のパワーが同じで、数値が低いほど雑音が強くなります。

<h2 id="attribution">案①　基準と寄与度手法</h2>

音声を「いつ、どの高さの音が、どれくらい強いか」を表すメルスペクトログラムに変え、小さな区画に分けました。**IG（Integrated Gradients）**は、基準の値から混合音の値へ少しずつ近づけ、どの区画が認識に効いたかを見積もる方法です。基準には無音と、音の高さごとに求めた典型的な値（中央値）の2種類を使いました。**入力勾配**は入力を少し変えたときの認識の変わりやすさ、**遮蔽**は区画を別の値で覆ったときの変化を測ります。

重要と判定した区画から順に弱め、Whisperが同じ文を出すスコアがどれほど変わるかを測りました。その変化をまとめた値が介入AUCです。確認できた59発話で、遮蔽のAUCは無音基準IGより0.137高くなりました（98.75%区間 +0.087〜+0.185）。一方、遮蔽が重要とした区画を残して音を作ると、ReazonのCERは元の混合音より30.87ポイント高くなりました。**認識に効く箇所を見つけても、その箇所を残すだけで文字起こししやすい音になるとは限りません。** [検定と数値品質の詳細](../../../../../ASR/whisper_ig_reconstruction/notes/research_hub/advisor-followups.html)

<table><thead><tr><th scope="col">手法</th><th scope="col">介入AUC</th><th scope="col">Reazon ΔCER (pp)</th></tr></thead><tbody><tr><td>無音基準IG</td><td>0.491</td><td>+23.69</td></tr><tr><td>中央値基準IG</td><td>0.566</td><td>+22.13</td></tr><tr><td>入力勾配</td><td>0.354</td><td>+26.88</td></tr><tr><td>遮蔽</td><td>0.628</td><td>+30.87</td></tr><tr><td>エネルギー</td><td>0.282</td><td>+16.74</td></tr><tr><td>ランダム</td><td>0.263</td><td>+45.90</td></tr><tr><td>全保持</td><td>—</td><td>-1.13</td></tr></tbody></table>





### 追加①　4モデルでCERとMAEを比べる

生成ASRを4種類に増やし、重要と判定された上位60%を目安に区画を残して、音声に戻しました。**絶対IG**は認識スコアを上げる区画と下げる区画をどちらも変化の大きさで選び、**正IG**はスコアを上げる方向に働く区画を優先します。入力×勾配は、入力勾配に元の入力値を掛ける方法です。

CERは文字起こしの正確さ、波形MAEは雑音を混ぜる前のきれいな音と各時点の振幅がどれほど違うかを示します。どちらも小さいほど良く、表では同じモデルの各手法を同じ発話で比べています。MAEに使った波形は保存音声や元の音響評価値と照合しました。たとえばWhisperでは、入力勾配は混合音より波形MAEが小さくなりましたが、CERは31.30%から58.42%に上がりました。波形の誤差と文字起こしの誤りは別々に読みます。

4モデルでの差を各発話で平均すると、3つの非IG手法はいずれも無音基準の絶対IGよりReazonのCERが高く、差は13.02〜23.03ポイントでした。下の区間は、発話によるばらつきを考慮した推定の幅です。

<table><thead><tr><th scope="col">手法</th><th scope="col">対応n</th><th scope="col">平均差・相関</th><th scope="col">98.33%区間</th></tr></thead><tbody><tr><td>入力勾配</td><td>58</td><td>+13.021</td><td>+10.327 ～ +15.827</td></tr><tr><td>入力×勾配</td><td>58</td><td>+23.029</td><td>+20.203 ～ +25.842</td></tr><tr><td>遮蔽</td><td>58</td><td>+16.836</td><td>+13.830 ～ +20.019</td></tr></tbody></table>

<details open><summary>Whisper large-v3</summary>

<table><thead><tr><th scope="col">手法</th><th scope="col">CER % (n=60)</th><th scope="col">MAE (n=60)</th></tr></thead><tbody><tr><td>混合音</td><td>31.30</td><td>0.04287</td></tr><tr><td>絶対IG</td><td>53.74</td><td>0.03378</td></tr><tr><td>正IG</td><td>45.07</td><td>0.03459</td></tr><tr><td>中央値基準・絶対IG</td><td>50.43</td><td>0.03446</td></tr><tr><td>中央値基準・正IG</td><td>49.32</td><td>0.03432</td></tr><tr><td>入力勾配</td><td>58.42</td><td>0.03162</td></tr><tr><td>入力×勾配</td><td>48.96</td><td>0.03513</td></tr><tr><td>遮蔽</td><td>69.61</td><td>0.03619</td></tr><tr><td>全保持</td><td>30.00</td><td>0.04041</td></tr><tr><td>エネルギー</td><td>48.11</td><td>0.03471</td></tr><tr><td>ランダム</td><td>78.94</td><td>0.03786</td></tr></tbody></table>

</details>

<details open><summary>CSJ Transformer</summary>

<table><thead><tr><th scope="col">手法</th><th scope="col">CER % (n=60)</th><th scope="col">MAE (n=60)</th></tr></thead><tbody><tr><td>混合音</td><td>31.30</td><td>0.04287</td></tr><tr><td>絶対IG</td><td>63.11</td><td>0.03472</td></tr><tr><td>正IG</td><td>57.09</td><td>0.03419</td></tr><tr><td>中央値基準・絶対IG</td><td>63.86</td><td>0.03495</td></tr><tr><td>中央値基準・正IG</td><td>59.84</td><td>0.03490</td></tr><tr><td>入力勾配</td><td>76.78</td><td>0.03385</td></tr><tr><td>入力×勾配</td><td>90.84</td><td>0.03497</td></tr><tr><td>遮蔽</td><td>76.33</td><td>0.03659</td></tr><tr><td>全保持</td><td>29.92</td><td>0.04074</td></tr><tr><td>エネルギー</td><td>52.74</td><td>0.03485</td></tr><tr><td>ランダム</td><td>83.75</td><td>0.03898</td></tr></tbody></table>

</details>

<details open><summary>CSJ Conformer</summary>

<table><thead><tr><th scope="col">手法</th><th scope="col">CER % (n=60)</th><th scope="col">MAE (n=60)</th></tr></thead><tbody><tr><td>混合音</td><td>31.30</td><td>0.04287</td></tr><tr><td>絶対IG</td><td>59.38</td><td>0.03604</td></tr><tr><td>正IG</td><td>53.47</td><td>0.03531</td></tr><tr><td>中央値基準・絶対IG</td><td>62.54</td><td>0.03719</td></tr><tr><td>中央値基準・正IG</td><td>59.92</td><td>0.03676</td></tr><tr><td>入力勾配</td><td>75.39</td><td>0.03425</td></tr><tr><td>入力×勾配</td><td>89.11</td><td>0.03522</td></tr><tr><td>遮蔽</td><td>75.91</td><td>0.03695</td></tr><tr><td>全保持</td><td>29.92</td><td>0.04074</td></tr><tr><td>エネルギー</td><td>52.74</td><td>0.03485</td></tr><tr><td>ランダム</td><td>83.75</td><td>0.03898</td></tr></tbody></table>

</details>

<details open><summary>LaboroTV Conformer</summary>

<table><thead><tr><th scope="col">手法</th><th scope="col">CER % (n=58)</th><th scope="col">MAE (n=58)</th></tr></thead><tbody><tr><td>混合音</td><td>30.71</td><td>0.04289</td></tr><tr><td>絶対IG</td><td>51.25</td><td>0.03199</td></tr><tr><td>正IG</td><td>48.83</td><td>0.03255</td></tr><tr><td>中央値基準・絶対IG</td><td>56.48</td><td>0.03468</td></tr><tr><td>中央値基準・正IG</td><td>49.83</td><td>0.03488</td></tr><tr><td>入力勾配</td><td>66.81</td><td>0.03448</td></tr><tr><td>入力×勾配</td><td>88.60</td><td>0.03684</td></tr><tr><td>遮蔽</td><td>71.10</td><td>0.03545</td></tr><tr><td>全保持</td><td>29.39</td><td>0.04075</td></tr><tr><td>エネルギー</td><td>52.11</td><td>0.03504</td></tr><tr><td>ランダム</td><td>83.59</td><td>0.03899</td></tr></tbody></table>

</details>











<h2 id="cross-asr">案②　生成ASRと雑音強度による違い</h2>

声を残すのが得意なASRは、雑音の種類や強さで変わるでしょうか。85発話を白色雑音（サーッという音）・交通雑音の2種類、−5・0・+10 dBの3段階で混ぜた計510条件を比較しました。4つの生成ASRが、同じ時間・周波数の目盛り上でIGを計算し、同じ割合だけ音の区画を残しました。

事前の開発データで選んだ条件を別の85発話で確かめると、**LaboroTV・−5 dBではReazonのCERが混合音より3.99ポイント下がりました**（95%区間 −5.49〜−2.46）。白色と交通は同じ重みで平均しました。表は生成ASRを行、雑音とSNRを列にしており、負の値ほど元の混合音より文字起こしが改善しています。括弧はReazonで比較できた発話数です。生成ASRが混合音から文字を出せず、再構成を行えなかった条件が9件ありました。[主比較と処理の詳細](../../../../../ASR/whisper_ig_reconstruction/notes/research_hub/advisor-followups.html)

<details><summary>評価器 Whisper large-v3</summary>

<table><thead><tr><th scope="col">生成ASR</th><th scope="col">白色 −5</th><th scope="col">白色 0</th><th scope="col">白色 +10</th><th scope="col">交通 −5</th><th scope="col">交通 0</th><th scope="col">交通 +10</th></tr></thead><tbody><tr><td>Whisper large-v3</td><td>+2.62</td><td>+0.63</td><td>+0.62</td><td>+0.44</td><td>-0.03</td><td>+0.16</td></tr><tr><td>CSJ Transformer</td><td>+2.88</td><td>+2.36</td><td>+0.03</td><td>+2.97</td><td>+1.03</td><td>-0.02</td></tr><tr><td>CSJ Conformer</td><td>+4.07</td><td>+2.37</td><td>-0.30</td><td>+3.12</td><td>+0.32</td><td>-0.12</td></tr><tr><td>LaboroTV Conformer</td><td>+1.41</td><td>+0.81</td><td>-0.06</td><td>+0.04</td><td>+0.24</td><td>+0.15</td></tr></tbody></table>

</details>

<details><summary>評価器 CSJ Transformer</summary>

<table><thead><tr><th scope="col">生成ASR</th><th scope="col">白色 −5</th><th scope="col">白色 0</th><th scope="col">白色 +10</th><th scope="col">交通 −5</th><th scope="col">交通 0</th><th scope="col">交通 +10</th></tr></thead><tbody><tr><td>Whisper large-v3</td><td>+22.42</td><td>+28.73</td><td>+7.75</td><td>+24.72</td><td>+10.08</td><td>+0.78</td></tr><tr><td>CSJ Transformer</td><td>+6.15</td><td>+6.86</td><td>+5.43</td><td>+9.21</td><td>+4.56</td><td>-0.05</td></tr><tr><td>CSJ Conformer</td><td>+2.91</td><td>+6.03</td><td>+4.34</td><td>+6.21</td><td>+2.99</td><td>+0.50</td></tr><tr><td>LaboroTV Conformer</td><td>+3.58</td><td>+9.46</td><td>+4.48</td><td>+10.67</td><td>+3.46</td><td>+0.54</td></tr></tbody></table>

</details>

<details><summary>評価器 CSJ Conformer</summary>

<table><thead><tr><th scope="col">生成ASR</th><th scope="col">白色 −5</th><th scope="col">白色 0</th><th scope="col">白色 +10</th><th scope="col">交通 −5</th><th scope="col">交通 0</th><th scope="col">交通 +10</th></tr></thead><tbody><tr><td>Whisper large-v3</td><td>-1.87</td><td>+3.64</td><td>-4.75</td><td>-11.44</td><td>-5.79</td><td>-0.94</td></tr><tr><td>CSJ Transformer</td><td>-4.17</td><td>+0.36</td><td>-1.40</td><td>-10.07</td><td>-11.81</td><td>-0.52</td></tr><tr><td>CSJ Conformer</td><td>-3.40</td><td>+0.88</td><td>+0.79</td><td>-8.15</td><td>-10.59</td><td>-0.35</td></tr><tr><td>LaboroTV Conformer</td><td>-3.61</td><td>-0.27</td><td>-3.68</td><td>-13.29</td><td>-11.78</td><td>+0.02</td></tr></tbody></table>

</details>

<details><summary>評価器 LaboroTV Conformer</summary>

<table><thead><tr><th scope="col">生成ASR</th><th scope="col">白色 −5</th><th scope="col">白色 0</th><th scope="col">白色 +10</th><th scope="col">交通 −5</th><th scope="col">交通 0</th><th scope="col">交通 +10</th></tr></thead><tbody><tr><td>Whisper large-v3</td><td>+0.03</td><td>-1.56</td><td>+1.44</td><td>-23.21</td><td>+0.30</td><td>+0.09</td></tr><tr><td>CSJ Transformer</td><td>+0.00</td><td>+1.47</td><td>+0.93</td><td>-13.25</td><td>-0.64</td><td>-0.37</td></tr><tr><td>CSJ Conformer</td><td>+0.03</td><td>+1.37</td><td>+1.09</td><td>-14.39</td><td>-0.30</td><td>+0.01</td></tr><tr><td>LaboroTV Conformer</td><td>+0.03</td><td>+2.95</td><td>+1.37</td><td>-17.09</td><td>-0.67</td><td>-0.04</td></tr></tbody></table>

</details>

<table><thead><tr><th scope="col">生成ASR</th><th scope="col">白色 −5</th><th scope="col">白色 0</th><th scope="col">白色 +10</th><th scope="col">交通 −5</th><th scope="col">交通 0</th><th scope="col">交通 +10</th></tr></thead><tbody><tr><td>Whisper large-v3</td><td>-4.89（85）</td><td>-1.58（85）</td><td>+1.16（85）</td><td>+0.51（85）</td><td>+0.38（85）</td><td>-0.02（85）</td></tr><tr><td>CSJ Transformer</td><td>-6.34（85）</td><td>-2.97（85）</td><td>+1.23（85）</td><td>-0.38（85）</td><td>-0.24（85）</td><td>+0.26（85）</td></tr><tr><td>CSJ Conformer</td><td>-5.89（85）</td><td>-3.71（85）</td><td>+0.78（85）</td><td>-0.70（84）</td><td>-0.14（85）</td><td>+0.32（85）</td></tr><tr><td>LaboroTV Conformer</td><td>-8.30（85）</td><td>-2.82（77）</td><td>+0.86（85）</td><td>+0.32（85）</td><td>+0.21（85）</td><td>+0.41（85）</td></tr></tbody></table>









### 追加②　同じ5評価器で非IG手法も比較

追加①で試した手法から、無音基準の絶対IG・正IGと非IGの3手法を使いました。確認用の60発話を、2種類の雑音と3段階の強さで比べました。1つの再構成音を4モデルとReazonの計5つで文字に起こしたので、改善が他の評価器にも表れるかを確認できます。手法を開くとReazonの表があり、その中で他の評価器の表も開けます。

開発用データで各手法の候補条件を選び、別の60発話で試すと、非IGの3手法とも元の混合音よりReazonのCERが高くなりました。候補の選定に共通して使えた開発発話は各手法2件です。開発時は、認識スコアや波形が元の計算と十分に一致するかを確かめ、29のモデル・混合音の組み合わせがその基準を外れました。先行②と追加②では、使った発話と音の作り方も変わっています。

<table><thead><tr><th scope="col">手法</th><th scope="col">対応n</th><th scope="col">平均差・相関</th><th scope="col">98.33%区間</th></tr></thead><tbody><tr><td>入力勾配</td><td>60</td><td>+34.183</td><td>+30.297 ～ +38.030</td></tr><tr><td>入力×勾配</td><td>60</td><td>+43.499</td><td>+39.077 ～ +47.913</td></tr><tr><td>遮蔽</td><td>60</td><td>+36.964</td><td>+32.874 ～ +41.050</td></tr></tbody></table>

<details open><summary>絶対IG</summary>

<table><thead><tr><th scope="col">生成ASR</th><th scope="col">白色 −5</th><th scope="col">白色 0</th><th scope="col">白色 +10</th><th scope="col">交通 −5</th><th scope="col">交通 0</th><th scope="col">交通 +10</th></tr></thead><tbody><tr><td>Whisper large-v3</td><td>+18.12（60）</td><td>+27.25（60）</td><td>+18.08（60）</td><td>+35.88（60）</td><td>+28.88（60）</td><td>+12.50（60）</td></tr><tr><td>CSJ Transformer</td><td>+24.16（60）</td><td>+35.24（60）</td><td>+45.61（60）</td><td>+35.70（60）</td><td>+39.95（60）</td><td>+27.70（60）</td></tr><tr><td>CSJ Conformer</td><td>+23.51（60）</td><td>+37.11（60）</td><td>+34.72（60）</td><td>+41.53（60）</td><td>+29.64（60）</td><td>+15.13（60）</td></tr><tr><td>LaboroTV Conformer</td><td>+21.97（60）</td><td>+31.50（55）</td><td>+22.07（60）</td><td>+33.94（60）</td><td>+23.57（60）</td><td>+7.78（60）</td></tr></tbody></table>

<details><summary>評価器 Whisper large-v3</summary>

<table><thead><tr><th scope="col">生成ASR</th><th scope="col">白色 −5</th><th scope="col">白色 0</th><th scope="col">白色 +10</th><th scope="col">交通 −5</th><th scope="col">交通 0</th><th scope="col">交通 +10</th></tr></thead><tbody><tr><td>Whisper large-v3</td><td>+47.46</td><td>+34.88</td><td>+5.61</td><td>+21.73</td><td>+7.72</td><td>+2.66</td></tr><tr><td>CSJ Transformer</td><td>+40.12</td><td>+39.30</td><td>+21.84</td><td>+28.58</td><td>+17.79</td><td>+6.19</td></tr><tr><td>CSJ Conformer</td><td>+55.93</td><td>+51.70</td><td>+22.38</td><td>+41.46</td><td>+16.34</td><td>+4.30</td></tr><tr><td>LaboroTV Conformer</td><td>+41.43</td><td>+36.61</td><td>+7.89</td><td>+23.32</td><td>+5.09</td><td>+1.66</td></tr></tbody></table>

</details>

<details><summary>評価器 CSJ Transformer</summary>

<table><thead><tr><th scope="col">生成ASR</th><th scope="col">白色 −5</th><th scope="col">白色 0</th><th scope="col">白色 +10</th><th scope="col">交通 −5</th><th scope="col">交通 0</th><th scope="col">交通 +10</th></tr></thead><tbody><tr><td>Whisper large-v3</td><td>-2.74</td><td>+30.56</td><td>+69.70</td><td>+34.25</td><td>+56.48</td><td>+61.47</td></tr><tr><td>CSJ Transformer</td><td>-2.72</td><td>+33.35</td><td>+70.94</td><td>+35.90</td><td>+62.46</td><td>+59.27</td></tr><tr><td>CSJ Conformer</td><td>-0.79</td><td>+33.52</td><td>+69.27</td><td>+36.50</td><td>+58.37</td><td>+59.13</td></tr><tr><td>LaboroTV Conformer</td><td>-1.95</td><td>+31.42</td><td>+67.09</td><td>+35.87</td><td>+53.88</td><td>+40.43</td></tr></tbody></table>

</details>

<details><summary>評価器 CSJ Conformer</summary>

<table><thead><tr><th scope="col">生成ASR</th><th scope="col">白色 −5</th><th scope="col">白色 0</th><th scope="col">白色 +10</th><th scope="col">交通 −5</th><th scope="col">交通 0</th><th scope="col">交通 +10</th></tr></thead><tbody><tr><td>Whisper large-v3</td><td>-6.39</td><td>-10.60</td><td>+53.28</td><td>-14.98</td><td>+26.93</td><td>+65.71</td></tr><tr><td>CSJ Transformer</td><td>-5.82</td><td>-11.55</td><td>+55.85</td><td>-15.45</td><td>+29.47</td><td>+66.09</td></tr><tr><td>CSJ Conformer</td><td>-6.54</td><td>-11.04</td><td>+54.10</td><td>-16.58</td><td>+28.02</td><td>+64.66</td></tr><tr><td>LaboroTV Conformer</td><td>-6.56</td><td>-12.50</td><td>+52.84</td><td>-15.87</td><td>+26.41</td><td>+46.37</td></tr></tbody></table>

</details>

<details><summary>評価器 LaboroTV Conformer</summary>

<table><thead><tr><th scope="col">生成ASR</th><th scope="col">白色 −5</th><th scope="col">白色 0</th><th scope="col">白色 +10</th><th scope="col">交通 −5</th><th scope="col">交通 0</th><th scope="col">交通 +10</th></tr></thead><tbody><tr><td>Whisper large-v3</td><td>+0.19</td><td>+6.78</td><td>+78.05</td><td>+45.01</td><td>+79.21</td><td>+37.89</td></tr><tr><td>CSJ Transformer</td><td>+0.00</td><td>+6.74</td><td>+84.48</td><td>+44.37</td><td>+83.14</td><td>+58.44</td></tr><tr><td>CSJ Conformer</td><td>-0.09</td><td>+6.74</td><td>+83.62</td><td>+44.48</td><td>+78.87</td><td>+43.01</td></tr><tr><td>LaboroTV Conformer</td><td>-0.11</td><td>+7.35</td><td>+75.13</td><td>+42.49</td><td>+67.46</td><td>+23.92</td></tr></tbody></table>

</details>

</details>

<details><summary>正IG</summary>

<table><thead><tr><th scope="col">生成ASR</th><th scope="col">白色 −5</th><th scope="col">白色 0</th><th scope="col">白色 +10</th><th scope="col">交通 −5</th><th scope="col">交通 0</th><th scope="col">交通 +10</th></tr></thead><tbody><tr><td>Whisper large-v3</td><td>+14.92（60）</td><td>+24.18（60）</td><td>+12.39（60）</td><td>+24.68（60）</td><td>+15.92（60）</td><td>+5.57（60）</td></tr><tr><td>CSJ Transformer</td><td>+20.31（60）</td><td>+29.43（60）</td><td>+35.11（60）</td><td>+30.94（60）</td><td>+29.06（60）</td><td>+17.19（60）</td></tr><tr><td>CSJ Conformer</td><td>+22.99（60）</td><td>+35.37（60）</td><td>+26.43（60）</td><td>+36.65（60）</td><td>+23.27（60）</td><td>+8.69（60）</td></tr><tr><td>LaboroTV Conformer</td><td>+21.85（60）</td><td>+33.40（55）</td><td>+15.43（60）</td><td>+32.03（60）</td><td>+17.24（60）</td><td>+3.79（60）</td></tr></tbody></table>

<details><summary>評価器 Whisper large-v3</summary>

<table><thead><tr><th scope="col">生成ASR</th><th scope="col">白色 −5</th><th scope="col">白色 0</th><th scope="col">白色 +10</th><th scope="col">交通 −5</th><th scope="col">交通 0</th><th scope="col">交通 +10</th></tr></thead><tbody><tr><td>Whisper large-v3</td><td>+53.10</td><td>+35.33</td><td>+6.46</td><td>+22.04</td><td>+6.05</td><td>+1.55</td></tr><tr><td>CSJ Transformer</td><td>+42.88</td><td>+39.29</td><td>+14.32</td><td>+28.51</td><td>+13.49</td><td>+2.38</td></tr><tr><td>CSJ Conformer</td><td>+57.81</td><td>+55.79</td><td>+14.93</td><td>+33.95</td><td>+13.78</td><td>+2.60</td></tr><tr><td>LaboroTV Conformer</td><td>+42.47</td><td>+44.70</td><td>+5.59</td><td>+27.58</td><td>+6.06</td><td>+0.89</td></tr></tbody></table>

</details>

<details><summary>評価器 CSJ Transformer</summary>

<table><thead><tr><th scope="col">生成ASR</th><th scope="col">白色 −5</th><th scope="col">白色 0</th><th scope="col">白色 +10</th><th scope="col">交通 −5</th><th scope="col">交通 0</th><th scope="col">交通 +10</th></tr></thead><tbody><tr><td>Whisper large-v3</td><td>+0.53</td><td>+32.62</td><td>+72.75</td><td>+35.99</td><td>+61.32</td><td>+68.26</td></tr><tr><td>CSJ Transformer</td><td>-0.77</td><td>+33.68</td><td>+72.52</td><td>+38.00</td><td>+61.82</td><td>+57.98</td></tr><tr><td>CSJ Conformer</td><td>+1.82</td><td>+34.01</td><td>+68.06</td><td>+36.67</td><td>+56.23</td><td>+56.18</td></tr><tr><td>LaboroTV Conformer</td><td>-1.38</td><td>+31.96</td><td>+66.52</td><td>+37.56</td><td>+55.71</td><td>+41.18</td></tr></tbody></table>

</details>

<details><summary>評価器 CSJ Conformer</summary>

<table><thead><tr><th scope="col">生成ASR</th><th scope="col">白色 −5</th><th scope="col">白色 0</th><th scope="col">白色 +10</th><th scope="col">交通 −5</th><th scope="col">交通 0</th><th scope="col">交通 +10</th></tr></thead><tbody><tr><td>Whisper large-v3</td><td>-5.01</td><td>-10.49</td><td>+54.24</td><td>-15.23</td><td>+30.13</td><td>+68.68</td></tr><tr><td>CSJ Transformer</td><td>-5.79</td><td>-11.70</td><td>+54.25</td><td>-15.74</td><td>+27.87</td><td>+62.17</td></tr><tr><td>CSJ Conformer</td><td>-6.61</td><td>-12.00</td><td>+51.74</td><td>-16.59</td><td>+26.75</td><td>+60.95</td></tr><tr><td>LaboroTV Conformer</td><td>-7.65</td><td>-11.56</td><td>+53.10</td><td>-15.43</td><td>+25.95</td><td>+45.07</td></tr></tbody></table>

</details>

<details><summary>評価器 LaboroTV Conformer</summary>

<table><thead><tr><th scope="col">生成ASR</th><th scope="col">白色 −5</th><th scope="col">白色 0</th><th scope="col">白色 +10</th><th scope="col">交通 −5</th><th scope="col">交通 0</th><th scope="col">交通 +10</th></tr></thead><tbody><tr><td>Whisper large-v3</td><td>+0.03</td><td>+6.74</td><td>+82.53</td><td>+44.63</td><td>+80.53</td><td>+30.69</td></tr><tr><td>CSJ Transformer</td><td>+0.00</td><td>+6.66</td><td>+82.43</td><td>+43.54</td><td>+77.76</td><td>+45.38</td></tr><tr><td>CSJ Conformer</td><td>+0.09</td><td>+6.74</td><td>+82.10</td><td>+45.01</td><td>+75.19</td><td>+19.79</td></tr><tr><td>LaboroTV Conformer</td><td>+0.00</td><td>+7.22</td><td>+62.97</td><td>+43.09</td><td>+64.72</td><td>+18.11</td></tr></tbody></table>

</details>

</details>

<details><summary>入力勾配</summary>

<table><thead><tr><th scope="col">生成ASR</th><th scope="col">白色 −5</th><th scope="col">白色 0</th><th scope="col">白色 +10</th><th scope="col">交通 −5</th><th scope="col">交通 0</th><th scope="col">交通 +10</th></tr></thead><tbody><tr><td>Whisper large-v3</td><td>+20.96（60）</td><td>+23.31（60）</td><td>+25.44（60）</td><td>+36.13（60）</td><td>+32.10（60）</td><td>+22.17（60）</td></tr><tr><td>CSJ Transformer</td><td>+25.32（60）</td><td>+42.73（60）</td><td>+56.53（60）</td><td>+48.17（60）</td><td>+58.61（60）</td><td>+55.85（60）</td></tr><tr><td>CSJ Conformer</td><td>+24.37（60）</td><td>+33.72（60）</td><td>+49.83（60）</td><td>+46.89（60）</td><td>+56.39（60）</td><td>+51.30（60）</td></tr><tr><td>LaboroTV Conformer</td><td>+24.50（60）</td><td>+37.08（55）</td><td>+38.86（60）</td><td>+50.02（60）</td><td>+45.30（60）</td><td>+29.50（60）</td></tr></tbody></table>

<details><summary>評価器 Whisper large-v3</summary>

<table><thead><tr><th scope="col">生成ASR</th><th scope="col">白色 −5</th><th scope="col">白色 0</th><th scope="col">白色 +10</th><th scope="col">交通 −5</th><th scope="col">交通 0</th><th scope="col">交通 +10</th></tr></thead><tbody><tr><td>Whisper large-v3</td><td>+55.77</td><td>+37.77</td><td>+19.03</td><td>+40.46</td><td>+18.27</td><td>+7.11</td></tr><tr><td>CSJ Transformer</td><td>+42.87</td><td>+41.09</td><td>+42.74</td><td>+47.78</td><td>+49.04</td><td>+31.20</td></tr><tr><td>CSJ Conformer</td><td>+44.36</td><td>+35.61</td><td>+34.91</td><td>+48.56</td><td>+39.66</td><td>+27.13</td></tr><tr><td>LaboroTV Conformer</td><td>+47.52</td><td>+45.68</td><td>+24.13</td><td>+40.54</td><td>+23.46</td><td>+10.35</td></tr></tbody></table>

</details>

<details><summary>評価器 CSJ Transformer</summary>

<table><thead><tr><th scope="col">生成ASR</th><th scope="col">白色 −5</th><th scope="col">白色 0</th><th scope="col">白色 +10</th><th scope="col">交通 −5</th><th scope="col">交通 0</th><th scope="col">交通 +10</th></tr></thead><tbody><tr><td>Whisper large-v3</td><td>-5.38</td><td>+30.43</td><td>+70.02</td><td>+33.26</td><td>+57.60</td><td>+68.54</td></tr><tr><td>CSJ Transformer</td><td>-0.80</td><td>+34.11</td><td>+70.37</td><td>+34.25</td><td>+56.62</td><td>+67.18</td></tr><tr><td>CSJ Conformer</td><td>-0.44</td><td>+34.22</td><td>+69.62</td><td>+33.26</td><td>+55.65</td><td>+68.43</td></tr><tr><td>LaboroTV Conformer</td><td>-0.61</td><td>+32.68</td><td>+68.90</td><td>+34.24</td><td>+58.69</td><td>+64.24</td></tr></tbody></table>

</details>

<details><summary>評価器 CSJ Conformer</summary>

<table><thead><tr><th scope="col">生成ASR</th><th scope="col">白色 −5</th><th scope="col">白色 0</th><th scope="col">白色 +10</th><th scope="col">交通 −5</th><th scope="col">交通 0</th><th scope="col">交通 +10</th></tr></thead><tbody><tr><td>Whisper large-v3</td><td>-6.20</td><td>-10.98</td><td>+53.23</td><td>-14.80</td><td>+29.44</td><td>+73.36</td></tr><tr><td>CSJ Transformer</td><td>-5.80</td><td>-10.39</td><td>+54.70</td><td>-14.38</td><td>+29.70</td><td>+71.82</td></tr><tr><td>CSJ Conformer</td><td>-6.70</td><td>-11.36</td><td>+54.30</td><td>-16.20</td><td>+28.82</td><td>+68.24</td></tr><tr><td>LaboroTV Conformer</td><td>-6.07</td><td>-11.67</td><td>+54.06</td><td>-15.43</td><td>+29.13</td><td>+67.19</td></tr></tbody></table>

</details>

<details><summary>評価器 LaboroTV Conformer</summary>

<table><thead><tr><th scope="col">生成ASR</th><th scope="col">白色 −5</th><th scope="col">白色 0</th><th scope="col">白色 +10</th><th scope="col">交通 −5</th><th scope="col">交通 0</th><th scope="col">交通 +10</th></tr></thead><tbody><tr><td>Whisper large-v3</td><td>-0.16</td><td>+6.46</td><td>+86.23</td><td>+45.01</td><td>+86.44</td><td>+72.30</td></tr><tr><td>CSJ Transformer</td><td>+0.18</td><td>+6.58</td><td>+84.97</td><td>+44.94</td><td>+86.21</td><td>+80.47</td></tr><tr><td>CSJ Conformer</td><td>+0.00</td><td>+6.49</td><td>+83.77</td><td>+45.41</td><td>+84.76</td><td>+78.01</td></tr><tr><td>LaboroTV Conformer</td><td>+0.00</td><td>+7.24</td><td>+82.11</td><td>+45.36</td><td>+85.10</td><td>+68.62</td></tr></tbody></table>

</details>

</details>

<details><summary>入力×勾配</summary>

<table><thead><tr><th scope="col">生成ASR</th><th scope="col">白色 −5</th><th scope="col">白色 0</th><th scope="col">白色 +10</th><th scope="col">交通 −5</th><th scope="col">交通 0</th><th scope="col">交通 +10</th></tr></thead><tbody><tr><td>Whisper large-v3</td><td>+20.97（60）</td><td>+21.11（60）</td><td>+12.36（60）</td><td>+35.77（60）</td><td>+20.13（60）</td><td>+8.19（60）</td></tr><tr><td>CSJ Transformer</td><td>+26.15（60）</td><td>+47.91（60）</td><td>+73.94（60）</td><td>+62.01（60）</td><td>+78.98（60）</td><td>+81.08（60）</td></tr><tr><td>CSJ Conformer</td><td>+25.59（60）</td><td>+41.69（60）</td><td>+67.20（60）</td><td>+61.41（60）</td><td>+76.77（60）</td><td>+79.68（60）</td></tr><tr><td>LaboroTV Conformer</td><td>+27.09（60）</td><td>+49.01（55）</td><td>+64.53（60）</td><td>+62.17（60）</td><td>+73.07（60）</td><td>+72.80（60）</td></tr></tbody></table>

<details><summary>評価器 Whisper large-v3</summary>

<table><thead><tr><th scope="col">生成ASR</th><th scope="col">白色 −5</th><th scope="col">白色 0</th><th scope="col">白色 +10</th><th scope="col">交通 −5</th><th scope="col">交通 0</th><th scope="col">交通 +10</th></tr></thead><tbody><tr><td>Whisper large-v3</td><td>+50.37</td><td>+33.42</td><td>+7.71</td><td>+16.35</td><td>+6.49</td><td>+1.90</td></tr><tr><td>CSJ Transformer</td><td>+46.88</td><td>+59.05</td><td>+68.42</td><td>+76.19</td><td>+80.48</td><td>+66.16</td></tr><tr><td>CSJ Conformer</td><td>+48.91</td><td>+54.37</td><td>+57.24</td><td>+77.12</td><td>+93.45</td><td>+60.90</td></tr><tr><td>LaboroTV Conformer</td><td>+52.16</td><td>+62.43</td><td>+59.10</td><td>+75.54</td><td>+75.15</td><td>+46.86</td></tr></tbody></table>

</details>

<details><summary>評価器 CSJ Transformer</summary>

<table><thead><tr><th scope="col">生成ASR</th><th scope="col">白色 −5</th><th scope="col">白色 0</th><th scope="col">白色 +10</th><th scope="col">交通 −5</th><th scope="col">交通 0</th><th scope="col">交通 +10</th></tr></thead><tbody><tr><td>Whisper large-v3</td><td>-3.94</td><td>+28.74</td><td>+67.83</td><td>+34.06</td><td>+59.60</td><td>+74.42</td></tr><tr><td>CSJ Transformer</td><td>-0.44</td><td>+34.31</td><td>+70.09</td><td>+33.19</td><td>+58.06</td><td>+72.29</td></tr><tr><td>CSJ Conformer</td><td>-1.18</td><td>+33.95</td><td>+70.23</td><td>+34.10</td><td>+58.38</td><td>+72.76</td></tr><tr><td>LaboroTV Conformer</td><td>-1.43</td><td>+29.86</td><td>+66.50</td><td>+33.32</td><td>+58.56</td><td>+69.69</td></tr></tbody></table>

</details>

<details><summary>評価器 CSJ Conformer</summary>

<table><thead><tr><th scope="col">生成ASR</th><th scope="col">白色 −5</th><th scope="col">白色 0</th><th scope="col">白色 +10</th><th scope="col">交通 −5</th><th scope="col">交通 0</th><th scope="col">交通 +10</th></tr></thead><tbody><tr><td>Whisper large-v3</td><td>-6.88</td><td>-11.31</td><td>+52.00</td><td>-13.81</td><td>+31.23</td><td>+73.46</td></tr><tr><td>CSJ Transformer</td><td>-6.07</td><td>-11.08</td><td>+55.08</td><td>-13.09</td><td>+32.66</td><td>+76.37</td></tr><tr><td>CSJ Conformer</td><td>-6.17</td><td>-11.23</td><td>+53.92</td><td>-13.78</td><td>+31.66</td><td>+74.32</td></tr><tr><td>LaboroTV Conformer</td><td>-6.25</td><td>-10.56</td><td>+54.05</td><td>-13.61</td><td>+30.94</td><td>+73.31</td></tr></tbody></table>

</details>

<details><summary>評価器 LaboroTV Conformer</summary>

<table><thead><tr><th scope="col">生成ASR</th><th scope="col">白色 −5</th><th scope="col">白色 0</th><th scope="col">白色 +10</th><th scope="col">交通 −5</th><th scope="col">交通 0</th><th scope="col">交通 +10</th></tr></thead><tbody><tr><td>Whisper large-v3</td><td>-0.24</td><td>+6.75</td><td>+82.29</td><td>+44.50</td><td>+85.25</td><td>+57.13</td></tr><tr><td>CSJ Transformer</td><td>-0.09</td><td>+6.39</td><td>+85.50</td><td>+45.25</td><td>+86.73</td><td>+86.59</td></tr><tr><td>CSJ Conformer</td><td>-0.10</td><td>+6.63</td><td>+86.86</td><td>+45.63</td><td>+87.12</td><td>+87.35</td></tr><tr><td>LaboroTV Conformer</td><td>+0.00</td><td>+7.23</td><td>+85.49</td><td>+45.20</td><td>+86.52</td><td>+85.82</td></tr></tbody></table>

</details>

</details>

<details><summary>遮蔽</summary>

<table><thead><tr><th scope="col">生成ASR</th><th scope="col">白色 −5</th><th scope="col">白色 0</th><th scope="col">白色 +10</th><th scope="col">交通 −5</th><th scope="col">交通 0</th><th scope="col">交通 +10</th></tr></thead><tbody><tr><td>Whisper large-v3</td><td>+22.09（60）</td><td>+36.90（60）</td><td>+45.14（60）</td><td>+49.04（60）</td><td>+47.99（60）</td><td>+38.82（60）</td></tr><tr><td>CSJ Transformer</td><td>+24.99（60）</td><td>+43.24（60）</td><td>+49.79（60）</td><td>+51.07（60）</td><td>+55.39（60）</td><td>+60.36（60）</td></tr><tr><td>CSJ Conformer</td><td>+26.96（60）</td><td>+42.26（60）</td><td>+44.96（60）</td><td>+46.97（60）</td><td>+48.17（60）</td><td>+54.81（60）</td></tr><tr><td>LaboroTV Conformer</td><td>+24.73（60）</td><td>+36.77（55）</td><td>+34.64（60）</td><td>+48.80（60）</td><td>+43.92（60）</td><td>+43.94（60）</td></tr></tbody></table>

<details><summary>評価器 Whisper large-v3</summary>

<table><thead><tr><th scope="col">生成ASR</th><th scope="col">白色 −5</th><th scope="col">白色 0</th><th scope="col">白色 +10</th><th scope="col">交通 −5</th><th scope="col">交通 0</th><th scope="col">交通 +10</th></tr></thead><tbody><tr><td>Whisper large-v3</td><td>+57.40</td><td>+71.18</td><td>+46.86</td><td>+58.64</td><td>+42.65</td><td>+17.37</td></tr><tr><td>CSJ Transformer</td><td>+57.14</td><td>+73.37</td><td>+33.03</td><td>+56.14</td><td>+45.84</td><td>+33.33</td></tr><tr><td>CSJ Conformer</td><td>+58.57</td><td>+66.46</td><td>+29.05</td><td>+56.22</td><td>+40.27</td><td>+27.52</td></tr><tr><td>LaboroTV Conformer</td><td>+57.66</td><td>+63.69</td><td>+21.34</td><td>+50.82</td><td>+28.20</td><td>+14.58</td></tr></tbody></table>

</details>

<details><summary>評価器 CSJ Transformer</summary>

<table><thead><tr><th scope="col">生成ASR</th><th scope="col">白色 −5</th><th scope="col">白色 0</th><th scope="col">白色 +10</th><th scope="col">交通 −5</th><th scope="col">交通 0</th><th scope="col">交通 +10</th></tr></thead><tbody><tr><td>Whisper large-v3</td><td>-2.30</td><td>+32.49</td><td>+75.54</td><td>+36.75</td><td>+66.33</td><td>+80.53</td></tr><tr><td>CSJ Transformer</td><td>+6.94</td><td>+39.21</td><td>+78.03</td><td>+43.97</td><td>+62.52</td><td>+81.36</td></tr><tr><td>CSJ Conformer</td><td>+5.31</td><td>+38.25</td><td>+78.07</td><td>+42.65</td><td>+65.74</td><td>+81.64</td></tr><tr><td>LaboroTV Conformer</td><td>+6.92</td><td>+38.58</td><td>+80.98</td><td>+39.48</td><td>+63.80</td><td>+84.15</td></tr></tbody></table>

</details>

<details><summary>評価器 CSJ Conformer</summary>

<table><thead><tr><th scope="col">生成ASR</th><th scope="col">白色 −5</th><th scope="col">白色 0</th><th scope="col">白色 +10</th><th scope="col">交通 −5</th><th scope="col">交通 0</th><th scope="col">交通 +10</th></tr></thead><tbody><tr><td>Whisper large-v3</td><td>-4.34</td><td>-8.64</td><td>+55.95</td><td>-12.35</td><td>+32.62</td><td>+76.88</td></tr><tr><td>CSJ Transformer</td><td>-5.72</td><td>-10.36</td><td>+56.38</td><td>-13.52</td><td>+31.76</td><td>+77.66</td></tr><tr><td>CSJ Conformer</td><td>-4.66</td><td>-10.62</td><td>+54.84</td><td>-13.07</td><td>+31.96</td><td>+76.58</td></tr><tr><td>LaboroTV Conformer</td><td>-4.69</td><td>-9.94</td><td>+54.00</td><td>-12.51</td><td>+32.26</td><td>+77.90</td></tr></tbody></table>

</details>

<details><summary>評価器 LaboroTV Conformer</summary>

<table><thead><tr><th scope="col">生成ASR</th><th scope="col">白色 −5</th><th scope="col">白色 0</th><th scope="col">白色 +10</th><th scope="col">交通 −5</th><th scope="col">交通 0</th><th scope="col">交通 +10</th></tr></thead><tbody><tr><td>Whisper large-v3</td><td>+0.15</td><td>+6.73</td><td>+86.57</td><td>+44.87</td><td>+87.15</td><td>+87.92</td></tr><tr><td>CSJ Transformer</td><td>+0.02</td><td>+6.74</td><td>+86.40</td><td>+45.44</td><td>+87.05</td><td>+88.21</td></tr><tr><td>CSJ Conformer</td><td>+0.00</td><td>+6.76</td><td>+87.17</td><td>+45.27</td><td>+87.01</td><td>+87.29</td></tr><tr><td>LaboroTV Conformer</td><td>+0.00</td><td>+7.35</td><td>+86.62</td><td>+45.45</td><td>+87.08</td><td>+87.02</td></tr></tbody></table>

</details>

</details>

<details><summary>全保持</summary>

<table><thead><tr><th scope="col">生成ASR</th><th scope="col">白色 −5</th><th scope="col">白色 0</th><th scope="col">白色 +10</th><th scope="col">交通 −5</th><th scope="col">交通 0</th><th scope="col">交通 +10</th></tr></thead><tbody><tr><td>Whisper large-v3</td><td>-1.79（60）</td><td>-2.88（60）</td><td>-0.31（60）</td><td>-2.22（60）</td><td>-1.53（60）</td><td>-0.20（60）</td></tr><tr><td>CSJ Transformer</td><td>-1.43（60）</td><td>-1.56（60）</td><td>-0.28（60）</td><td>-0.60（60）</td><td>-1.13（60）</td><td>-0.35（60）</td></tr><tr><td>CSJ Conformer</td><td>-1.43（60）</td><td>-1.56（60）</td><td>-0.28（60）</td><td>-0.60（60）</td><td>-1.13（60）</td><td>-0.35（60）</td></tr><tr><td>LaboroTV Conformer</td><td>-1.43（60）</td><td>-1.78（55）</td><td>-0.28（60）</td><td>-0.60（60）</td><td>-1.13（60）</td><td>-0.35（60）</td></tr></tbody></table>

<details><summary>評価器 Whisper large-v3</summary>

<table><thead><tr><th scope="col">生成ASR</th><th scope="col">白色 −5</th><th scope="col">白色 0</th><th scope="col">白色 +10</th><th scope="col">交通 −5</th><th scope="col">交通 0</th><th scope="col">交通 +10</th></tr></thead><tbody><tr><td>Whisper large-v3</td><td>-0.97</td><td>+1.16</td><td>+0.00</td><td>-0.15</td><td>-0.12</td><td>+0.00</td></tr><tr><td>CSJ Transformer</td><td>-1.04</td><td>+1.12</td><td>+0.14</td><td>-0.19</td><td>+0.12</td><td>-0.06</td></tr><tr><td>CSJ Conformer</td><td>-1.04</td><td>+1.12</td><td>+0.14</td><td>-0.19</td><td>+0.12</td><td>-0.06</td></tr><tr><td>LaboroTV Conformer</td><td>-1.04</td><td>+1.22</td><td>+0.14</td><td>-0.19</td><td>+0.12</td><td>-0.06</td></tr></tbody></table>

</details>

<details><summary>評価器 CSJ Transformer</summary>

<table><thead><tr><th scope="col">生成ASR</th><th scope="col">白色 −5</th><th scope="col">白色 0</th><th scope="col">白色 +10</th><th scope="col">交通 −5</th><th scope="col">交通 0</th><th scope="col">交通 +10</th></tr></thead><tbody><tr><td>Whisper large-v3</td><td>+0.27</td><td>-2.18</td><td>-0.39</td><td>+0.56</td><td>+0.49</td><td>+0.08</td></tr><tr><td>CSJ Transformer</td><td>+1.20</td><td>-1.72</td><td>-0.19</td><td>+1.79</td><td>+0.18</td><td>-0.11</td></tr><tr><td>CSJ Conformer</td><td>+1.20</td><td>-1.72</td><td>-0.19</td><td>+1.79</td><td>+0.18</td><td>-0.11</td></tr><tr><td>LaboroTV Conformer</td><td>+1.20</td><td>-1.64</td><td>-0.19</td><td>+1.79</td><td>+0.18</td><td>-0.11</td></tr></tbody></table>

</details>

<details><summary>評価器 CSJ Conformer</summary>

<table><thead><tr><th scope="col">生成ASR</th><th scope="col">白色 −5</th><th scope="col">白色 0</th><th scope="col">白色 +10</th><th scope="col">交通 −5</th><th scope="col">交通 0</th><th scope="col">交通 +10</th></tr></thead><tbody><tr><td>Whisper large-v3</td><td>-1.34</td><td>+0.49</td><td>+1.26</td><td>+1.09</td><td>+1.21</td><td>-0.63</td></tr><tr><td>CSJ Transformer</td><td>-0.25</td><td>+1.13</td><td>+1.29</td><td>+3.19</td><td>+0.30</td><td>-0.79</td></tr><tr><td>CSJ Conformer</td><td>-0.25</td><td>+1.13</td><td>+1.29</td><td>+3.19</td><td>+0.30</td><td>-0.79</td></tr><tr><td>LaboroTV Conformer</td><td>-0.25</td><td>+1.50</td><td>+1.29</td><td>+3.19</td><td>+0.30</td><td>-0.79</td></tr></tbody></table>

</details>

<details><summary>評価器 LaboroTV Conformer</summary>

<table><thead><tr><th scope="col">生成ASR</th><th scope="col">白色 −5</th><th scope="col">白色 0</th><th scope="col">白色 +10</th><th scope="col">交通 −5</th><th scope="col">交通 0</th><th scope="col">交通 +10</th></tr></thead><tbody><tr><td>Whisper large-v3</td><td>+0.00</td><td>+1.25</td><td>+0.36</td><td>-2.48</td><td>-0.00</td><td>-0.19</td></tr><tr><td>CSJ Transformer</td><td>+0.00</td><td>+0.64</td><td>+0.33</td><td>-4.50</td><td>-0.55</td><td>-0.30</td></tr><tr><td>CSJ Conformer</td><td>+0.00</td><td>+0.64</td><td>+0.33</td><td>-4.50</td><td>-0.55</td><td>-0.30</td></tr><tr><td>LaboroTV Conformer</td><td>+0.00</td><td>+0.70</td><td>+0.33</td><td>-4.50</td><td>-0.55</td><td>-0.30</td></tr></tbody></table>

</details>

</details>

<details><summary>エネルギー</summary>

<table><thead><tr><th scope="col">生成ASR</th><th scope="col">白色 −5</th><th scope="col">白色 0</th><th scope="col">白色 +10</th><th scope="col">交通 −5</th><th scope="col">交通 0</th><th scope="col">交通 +10</th></tr></thead><tbody><tr><td>Whisper large-v3</td><td>+13.70（60）</td><td>+20.21（60）</td><td>+7.97（60）</td><td>+39.74（60）</td><td>+26.69（60）</td><td>+5.45（60）</td></tr><tr><td>CSJ Transformer</td><td>+19.32（60）</td><td>+27.39（60）</td><td>+13.55（60）</td><td>+42.13（60）</td><td>+28.99（60）</td><td>+5.95（60）</td></tr><tr><td>CSJ Conformer</td><td>+19.32（60）</td><td>+27.39（60）</td><td>+13.55（60）</td><td>+42.13（60）</td><td>+28.99（60）</td><td>+5.95（60）</td></tr><tr><td>LaboroTV Conformer</td><td>+19.32（60）</td><td>+27.15（55）</td><td>+13.55（60）</td><td>+42.13（60）</td><td>+28.99（60）</td><td>+5.95（60）</td></tr></tbody></table>

<details><summary>評価器 Whisper large-v3</summary>

<table><thead><tr><th scope="col">生成ASR</th><th scope="col">白色 −5</th><th scope="col">白色 0</th><th scope="col">白色 +10</th><th scope="col">交通 −5</th><th scope="col">交通 0</th><th scope="col">交通 +10</th></tr></thead><tbody><tr><td>Whisper large-v3</td><td>+56.93</td><td>+30.78</td><td>+4.05</td><td>+16.38</td><td>+6.99</td><td>+1.32</td></tr><tr><td>CSJ Transformer</td><td>+58.28</td><td>+33.61</td><td>+4.16</td><td>+16.27</td><td>+6.46</td><td>+1.97</td></tr><tr><td>CSJ Conformer</td><td>+58.28</td><td>+33.61</td><td>+4.16</td><td>+16.27</td><td>+6.46</td><td>+1.97</td></tr><tr><td>LaboroTV Conformer</td><td>+58.28</td><td>+32.29</td><td>+4.16</td><td>+16.27</td><td>+6.46</td><td>+1.97</td></tr></tbody></table>

</details>

<details><summary>評価器 CSJ Transformer</summary>

<table><thead><tr><th scope="col">生成ASR</th><th scope="col">白色 −5</th><th scope="col">白色 0</th><th scope="col">白色 +10</th><th scope="col">交通 −5</th><th scope="col">交通 0</th><th scope="col">交通 +10</th></tr></thead><tbody><tr><td>Whisper large-v3</td><td>+4.41</td><td>+36.20</td><td>+64.40</td><td>+33.89</td><td>+59.08</td><td>+59.74</td></tr><tr><td>CSJ Transformer</td><td>+15.56</td><td>+49.00</td><td>+70.42</td><td>+33.78</td><td>+58.96</td><td>+51.13</td></tr><tr><td>CSJ Conformer</td><td>+15.56</td><td>+49.00</td><td>+70.42</td><td>+33.78</td><td>+58.96</td><td>+51.13</td></tr><tr><td>LaboroTV Conformer</td><td>+15.56</td><td>+49.56</td><td>+70.42</td><td>+33.78</td><td>+58.96</td><td>+51.13</td></tr></tbody></table>

</details>

<details><summary>評価器 CSJ Conformer</summary>

<table><thead><tr><th scope="col">生成ASR</th><th scope="col">白色 −5</th><th scope="col">白色 0</th><th scope="col">白色 +10</th><th scope="col">交通 −5</th><th scope="col">交通 0</th><th scope="col">交通 +10</th></tr></thead><tbody><tr><td>Whisper large-v3</td><td>-3.50</td><td>-8.41</td><td>+53.64</td><td>-11.84</td><td>+32.88</td><td>+71.47</td></tr><tr><td>CSJ Transformer</td><td>-3.11</td><td>-7.10</td><td>+53.14</td><td>-11.39</td><td>+32.36</td><td>+71.83</td></tr><tr><td>CSJ Conformer</td><td>-3.11</td><td>-7.10</td><td>+53.14</td><td>-11.39</td><td>+32.36</td><td>+71.83</td></tr><tr><td>LaboroTV Conformer</td><td>-3.11</td><td>-7.14</td><td>+53.14</td><td>-11.39</td><td>+32.36</td><td>+71.83</td></tr></tbody></table>

</details>

<details><summary>評価器 LaboroTV Conformer</summary>

<table><thead><tr><th scope="col">生成ASR</th><th scope="col">白色 −5</th><th scope="col">白色 0</th><th scope="col">白色 +10</th><th scope="col">交通 −5</th><th scope="col">交通 0</th><th scope="col">交通 +10</th></tr></thead><tbody><tr><td>Whisper large-v3</td><td>+0.41</td><td>+6.64</td><td>+62.49</td><td>+45.65</td><td>+84.66</td><td>+29.24</td></tr><tr><td>CSJ Transformer</td><td>+0.13</td><td>+6.50</td><td>+63.81</td><td>+45.27</td><td>+84.47</td><td>+24.32</td></tr><tr><td>CSJ Conformer</td><td>+0.13</td><td>+6.50</td><td>+63.81</td><td>+45.27</td><td>+84.47</td><td>+24.32</td></tr><tr><td>LaboroTV Conformer</td><td>+0.13</td><td>+7.09</td><td>+63.81</td><td>+45.27</td><td>+84.47</td><td>+24.32</td></tr></tbody></table>

</details>

</details>

<details><summary>ランダム</summary>

<table><thead><tr><th scope="col">生成ASR</th><th scope="col">白色 −5</th><th scope="col">白色 0</th><th scope="col">白色 +10</th><th scope="col">交通 −5</th><th scope="col">交通 0</th><th scope="col">交通 +10</th></tr></thead><tbody><tr><td>Whisper large-v3</td><td>+27.52（60）</td><td>+50.55（60）</td><td>+63.27（60）</td><td>+57.72（60）</td><td>+57.22（60）</td><td>+32.56（60）</td></tr><tr><td>CSJ Transformer</td><td>+28.18（60）</td><td>+52.58（60）</td><td>+70.43（60）</td><td>+61.09（60）</td><td>+68.49（60）</td><td>+47.35（60）</td></tr><tr><td>CSJ Conformer</td><td>+28.18（60）</td><td>+52.58（60）</td><td>+70.43（60）</td><td>+61.09（60）</td><td>+68.49（60）</td><td>+47.35（60）</td></tr><tr><td>LaboroTV Conformer</td><td>+28.18（60）</td><td>+52.75（55）</td><td>+70.43（60）</td><td>+61.09（60）</td><td>+68.49（60）</td><td>+47.35（60）</td></tr></tbody></table>

<details><summary>評価器 Whisper large-v3</summary>

<table><thead><tr><th scope="col">生成ASR</th><th scope="col">白色 −5</th><th scope="col">白色 0</th><th scope="col">白色 +10</th><th scope="col">交通 −5</th><th scope="col">交通 0</th><th scope="col">交通 +10</th></tr></thead><tbody><tr><td>Whisper large-v3</td><td>+58.00</td><td>+77.37</td><td>+64.33</td><td>+72.68</td><td>+55.18</td><td>+15.98</td></tr><tr><td>CSJ Transformer</td><td>+58.00</td><td>+79.54</td><td>+71.94</td><td>+74.13</td><td>+67.43</td><td>+21.25</td></tr><tr><td>CSJ Conformer</td><td>+58.00</td><td>+79.54</td><td>+71.94</td><td>+74.13</td><td>+67.43</td><td>+21.25</td></tr><tr><td>LaboroTV Conformer</td><td>+58.00</td><td>+80.33</td><td>+71.94</td><td>+74.13</td><td>+67.43</td><td>+21.25</td></tr></tbody></table>

</details>

<details><summary>評価器 CSJ Transformer</summary>

<table><thead><tr><th scope="col">生成ASR</th><th scope="col">白色 −5</th><th scope="col">白色 0</th><th scope="col">白色 +10</th><th scope="col">交通 −5</th><th scope="col">交通 0</th><th scope="col">交通 +10</th></tr></thead><tbody><tr><td>Whisper large-v3</td><td>+3.96</td><td>+38.07</td><td>+77.32</td><td>+38.53</td><td>+65.72</td><td>+84.00</td></tr><tr><td>CSJ Transformer</td><td>+17.19</td><td>+49.34</td><td>+83.54</td><td>+47.30</td><td>+69.31</td><td>+85.55</td></tr><tr><td>CSJ Conformer</td><td>+17.19</td><td>+49.34</td><td>+83.54</td><td>+47.30</td><td>+69.31</td><td>+85.55</td></tr><tr><td>LaboroTV Conformer</td><td>+17.19</td><td>+50.00</td><td>+83.54</td><td>+47.30</td><td>+69.31</td><td>+85.55</td></tr></tbody></table>

</details>

<details><summary>評価器 CSJ Conformer</summary>

<table><thead><tr><th scope="col">生成ASR</th><th scope="col">白色 −5</th><th scope="col">白色 0</th><th scope="col">白色 +10</th><th scope="col">交通 −5</th><th scope="col">交通 0</th><th scope="col">交通 +10</th></tr></thead><tbody><tr><td>Whisper large-v3</td><td>-4.13</td><td>-7.77</td><td>+56.75</td><td>-11.98</td><td>+32.76</td><td>+77.42</td></tr><tr><td>CSJ Transformer</td><td>-4.23</td><td>-7.79</td><td>+56.83</td><td>-10.86</td><td>+32.45</td><td>+77.49</td></tr><tr><td>CSJ Conformer</td><td>-4.23</td><td>-7.79</td><td>+56.83</td><td>-10.86</td><td>+32.45</td><td>+77.49</td></tr><tr><td>LaboroTV Conformer</td><td>-4.23</td><td>-8.08</td><td>+56.83</td><td>-10.86</td><td>+32.45</td><td>+77.49</td></tr></tbody></table>

</details>

<details><summary>評価器 LaboroTV Conformer</summary>

<table><thead><tr><th scope="col">生成ASR</th><th scope="col">白色 −5</th><th scope="col">白色 0</th><th scope="col">白色 +10</th><th scope="col">交通 −5</th><th scope="col">交通 0</th><th scope="col">交通 +10</th></tr></thead><tbody><tr><td>Whisper large-v3</td><td>+0.14</td><td>+6.87</td><td>+87.10</td><td>+45.44</td><td>+86.88</td><td>+85.75</td></tr><tr><td>CSJ Transformer</td><td>+0.28</td><td>+6.89</td><td>+87.17</td><td>+45.43</td><td>+87.14</td><td>+87.98</td></tr><tr><td>CSJ Conformer</td><td>+0.28</td><td>+6.89</td><td>+87.17</td><td>+45.43</td><td>+87.14</td><td>+87.98</td></tr><tr><td>LaboroTV Conformer</td><td>+0.28</td><td>+7.52</td><td>+87.17</td><td>+45.43</td><td>+87.14</td><td>+87.98</td></tr></tbody></table>

</details>

</details>











<h2 id="dominance">案③　声の優勢度と寄与・再構成</h2>

ASRが役立つと判定した箇所には、実際に声が多く含まれているでしょうか。混ぜる前の声と雑音が分かっているので、時間と音の高さごとに「声のパワー÷（声＋雑音のパワー）」を計算できます。この値が0.5を超えると声の方が強くなります。**出力利得**は再構成後にその箇所の音がどれだけ残ったか、**保持差J**は雑音より声をどれだけ多い割合で残したかを表します。

### 既存1000件の観察

1つの混合音の中で、声の割合の順位とWhisperの絶対IGの順位を比べました。**順位相関ρ**は、順位の並びが似ると正、逆になると負になります。1000件の平均は**+0.308**で、声の割合が高い箇所ほどIGも高い傾向がありました。ここでは、雑音の種類によって設定SNRも異なります。[音響指標と対照の詳細](../../../../../ASR/whisper_ig_reconstruction/notes/research_hub/source-dominance.html)

<table><thead><tr><th scope="col">雑音</th><th scope="col">n</th><th scope="col">優勢度↔絶対IG ρ</th><th scope="col">優勢度↔出力利得 ρ</th><th scope="col">IGの声・雑音保持差 J (pp)</th></tr></thead><tbody><tr><td>全体</td><td>1000</td><td>0.308</td><td>0.318</td><td>14.29</td></tr><tr><td>白色</td><td>200</td><td>0.321</td><td>0.329</td><td>28.71</td></tr><tr><td>交通</td><td>200</td><td>0.273</td><td>0.271</td><td>10.73</td></tr><tr><td>ピンク</td><td>200</td><td>0.314</td><td>0.318</td><td>16.07</td></tr><tr><td>流水</td><td>200</td><td>0.313</td><td>0.302</td><td>12.87</td></tr><tr><td>台所</td><td>200</td><td>0.319</td><td>0.371</td><td>3.05</td></tr></tbody></table>



### 同じ5組を4段階に混ぜ直した操作実験

同じ声と同じ雑音で、雑音の音量だけを変えて−10、0、+10、+20 dBに混ぜ直しました。Whisperで「全体の寄与の95%に達するまで上位から残す」絶対IG95・正IG95を比較しています。下表は各SNRで5組を平均した値です。プラスの相関は、そのSNRの音の中で声が優勢な箇所に高い寄与がつく傾向を示します。[同じ位置を追った結果と検算](../../../../../ASR/whisper_ig_reconstruction/notes/research_hub/controlled-snr.html)

<table><thead><tr><th scope="col">SNR (dB)</th><th scope="col">ρ 優勢度↔絶対IG</th><th scope="col">ρ 優勢度↔正IG</th><th scope="col">ΔCER 絶対IG (pp)</th><th scope="col">ΔCER 正IG (pp)</th></tr></thead><tbody><tr><td>-10</td><td>0.208</td><td>0.110</td><td>+0.46</td><td>+6.38</td></tr><tr><td>0</td><td>0.265</td><td>0.125</td><td>+5.36</td><td>+14.73</td></tr><tr><td>10</td><td>0.278</td><td>0.119</td><td>+0.80</td><td>+2.96</td></tr><tr><td>20</td><td>0.326</td><td>0.140</td><td>-0.54</td><td>-0.54</td></tr></tbody></table>





### 追加③　4モデル・5手法で声の優勢度に追従するか

4モデル・5手法に広げ、既存1000件と、4段階に混ぜた旧5組・新規30組を調べました。表の「混合音内の相関」は、1つの音の中で異なる箇所を比べた値です。「追従」では、たとえば発話の0.5秒付近の同じ高さの音に注目します。雑音の音量を変えて、その箇所が雑音優勢から声優勢に変わるとき、全体の寄与のうちそこに割り当てられる割合（寄与シェア）も上がるかを見ます。

新規30組では、3つの非IG手法とも、同じ箇所の声の割合が高くなるほど、そこに割り当てられる寄与シェアは下がる傾向でした（98.33%区間も負）。その箇所の**実際の再構成音がどれだけ残ったか**は「出力利得の追従」の列で確かめられます。

<table><thead><tr><th scope="col">手法</th><th scope="col">対応n</th><th scope="col">平均差・相関</th><th scope="col">98.33%区間</th></tr></thead><tbody><tr><td>入力勾配</td><td>30</td><td>-0.126</td><td>-0.154 ～ -0.100</td></tr><tr><td>入力×勾配</td><td>30</td><td>-0.176</td><td>-0.204 ～ -0.150</td></tr><tr><td>遮蔽</td><td>30</td><td>-0.134</td><td>-0.159 ～ -0.110</td></tr></tbody></table>

<details open><summary>Whisper large-v3</summary>

<table><thead><tr><th scope="col">手法</th><th scope="col">既存1000件 優勢度↔寄与</th><th scope="col">既存1000件 優勢度↔出力利得</th><th scope="col">旧5組 寄与の追従</th><th scope="col">新規30組 寄与の追従</th><th scope="col">新規30組 出力利得の追従</th></tr></thead><tbody><tr><td>絶対IG</td><td>0.550</td><td>0.566</td><td>0.008</td><td>0.048</td><td>0.204</td></tr><tr><td>正IG</td><td>0.502</td><td>0.534</td><td>0.065</td><td>0.063</td><td>0.207</td></tr><tr><td>入力勾配</td><td>0.186</td><td>0.273</td><td>-0.116</td><td>-0.048</td><td>0.030</td></tr><tr><td>入力×勾配</td><td>0.450</td><td>0.484</td><td>-0.167</td><td>-0.120</td><td>0.065</td></tr><tr><td>遮蔽</td><td>0.053</td><td>0.103</td><td>-0.090</td><td>-0.006</td><td>-0.033</td></tr><tr><td>エネルギー</td><td>0.607</td><td>0.489</td><td>-0.597</td><td>-0.588</td><td>0.388</td></tr><tr><td>ランダム</td><td>-0.001</td><td>0.049</td><td>0.003</td><td>0.003</td><td>0.016</td></tr><tr><td>全保持</td><td>—</td><td>0.252</td><td>—</td><td>—</td><td>0.113</td></tr></tbody></table>

<table><thead><tr><th scope="col">新規30組・手法</th><th scope="col">−10 dB</th><th scope="col">0 dB</th><th scope="col">+10 dB</th><th scope="col">+20 dB</th></tr></thead><tbody><tr><td>絶対IG</td><td>0.501</td><td>0.538</td><td>0.591</td><td>0.624</td></tr><tr><td>正IG</td><td>0.450</td><td>0.476</td><td>0.533</td><td>0.572</td></tr><tr><td>入力勾配</td><td>0.483</td><td>0.372</td><td>0.226</td><td>0.166</td></tr><tr><td>入力×勾配</td><td>0.486</td><td>0.500</td><td>0.455</td><td>0.423</td></tr><tr><td>遮蔽</td><td>0.183</td><td>0.170</td><td>0.016</td><td>-0.131</td></tr></tbody></table>

<table><thead><tr><th scope="col">新規30組・手法</th><th scope="col">J (pp)</th><th scope="col">ΔSI-SDR (dB)</th><th scope="col">ΔCER −10</th><th scope="col">ΔCER 0</th><th scope="col">ΔCER +10</th><th scope="col">ΔCER +20</th></tr></thead><tbody><tr><td>絶対IG</td><td>+15.39</td><td>+1.11</td><td>+7.18</td><td>+29.78</td><td>+16.35</td><td>+9.54</td></tr><tr><td>正IG</td><td>+14.40</td><td>+0.74</td><td>+5.93</td><td>+21.29</td><td>+8.66</td><td>+5.15</td></tr><tr><td>入力勾配</td><td>+25.80</td><td>-1.04</td><td>+7.54</td><td>+29.53</td><td>+24.36</td><td>+20.78</td></tr><tr><td>入力×勾配</td><td>+16.48</td><td>+0.68</td><td>+8.53</td><td>+18.29</td><td>+7.61</td><td>+9.78</td></tr><tr><td>遮蔽</td><td>+11.97</td><td>-5.32</td><td>+12.11</td><td>+43.00</td><td>+43.64</td><td>+43.00</td></tr><tr><td>全保持</td><td>-0.00</td><td>+0.89</td><td>-7.18</td><td>-0.56</td><td>-0.49</td><td>+0.25</td></tr><tr><td>エネルギー</td><td>+9.36</td><td>+1.42</td><td>+7.57</td><td>+20.01</td><td>+8.81</td><td>+2.21</td></tr><tr><td>ランダム</td><td>-1.72</td><td>-7.08</td><td>+17.50</td><td>+50.88</td><td>+44.70</td><td>+29.56</td></tr></tbody></table>

</details>

<details open><summary>CSJ Transformer</summary>

<table><thead><tr><th scope="col">手法</th><th scope="col">既存1000件 優勢度↔寄与</th><th scope="col">既存1000件 優勢度↔出力利得</th><th scope="col">旧5組 寄与の追従</th><th scope="col">新規30組 寄与の追従</th><th scope="col">新規30組 出力利得の追従</th></tr></thead><tbody><tr><td>絶対IG</td><td>0.310</td><td>0.397</td><td>0.141</td><td>0.135</td><td>0.224</td></tr><tr><td>正IG</td><td>0.360</td><td>0.456</td><td>0.105</td><td>0.099</td><td>0.246</td></tr><tr><td>入力勾配</td><td>-0.050</td><td>0.046</td><td>-0.263</td><td>-0.229</td><td>0.026</td></tr><tr><td>入力×勾配</td><td>-0.265</td><td>-0.226</td><td>-0.316</td><td>-0.300</td><td>-0.061</td></tr><tr><td>遮蔽</td><td>0.077</td><td>0.180</td><td>-0.266</td><td>-0.228</td><td>-0.037</td></tr><tr><td>エネルギー</td><td>0.611</td><td>0.541</td><td>-0.574</td><td>-0.559</td><td>0.552</td></tr><tr><td>ランダム</td><td>-0.001</td><td>0.063</td><td>-0.005</td><td>-0.001</td><td>0.039</td></tr><tr><td>全保持</td><td>—</td><td>0.363</td><td>—</td><td>—</td><td>0.265</td></tr></tbody></table>

<table><thead><tr><th scope="col">新規30組・手法</th><th scope="col">−10 dB</th><th scope="col">0 dB</th><th scope="col">+10 dB</th><th scope="col">+20 dB</th></tr></thead><tbody><tr><td>絶対IG</td><td>0.064</td><td>0.306</td><td>0.308</td><td>0.352</td></tr><tr><td>正IG</td><td>0.089</td><td>0.343</td><td>0.355</td><td>0.394</td></tr><tr><td>入力勾配</td><td>0.174</td><td>0.116</td><td>-0.129</td><td>-0.166</td></tr><tr><td>入力×勾配</td><td>0.003</td><td>-0.087</td><td>-0.374</td><td>-0.484</td></tr><tr><td>遮蔽</td><td>0.085</td><td>0.110</td><td>-0.066</td><td>-0.240</td></tr></tbody></table>

<table><thead><tr><th scope="col">新規30組・手法</th><th scope="col">J (pp)</th><th scope="col">ΔSI-SDR (dB)</th><th scope="col">ΔCER −10</th><th scope="col">ΔCER 0</th><th scope="col">ΔCER +10</th><th scope="col">ΔCER +20</th></tr></thead><tbody><tr><td>絶対IG</td><td>+11.16</td><td>-4.87</td><td>+10.78</td><td>+36.30</td><td>+36.45</td><td>+24.55</td></tr><tr><td>正IG</td><td>+15.30</td><td>-3.98</td><td>+9.21</td><td>+28.20</td><td>+26.39</td><td>+11.50</td></tr><tr><td>入力勾配</td><td>+3.07</td><td>-5.92</td><td>+13.93</td><td>+47.62</td><td>+55.97</td><td>+51.33</td></tr><tr><td>入力×勾配</td><td>-7.97</td><td>-12.29</td><td>+17.77</td><td>+64.02</td><td>+79.21</td><td>+81.49</td></tr><tr><td>遮蔽</td><td>+2.23</td><td>-6.34</td><td>+16.11</td><td>+53.14</td><td>+55.73</td><td>+60.71</td></tr><tr><td>全保持</td><td>+0.00</td><td>+0.66</td><td>-6.33</td><td>-1.74</td><td>-0.28</td><td>+0.25</td></tr><tr><td>エネルギー</td><td>+9.47</td><td>+1.19</td><td>+8.00</td><td>+24.97</td><td>+9.94</td><td>+2.23</td></tr><tr><td>ランダム</td><td>+0.35</td><td>-7.22</td><td>+17.06</td><td>+59.93</td><td>+61.66</td><td>+45.61</td></tr></tbody></table>

</details>

<details open><summary>CSJ Conformer</summary>

<table><thead><tr><th scope="col">手法</th><th scope="col">既存1000件 優勢度↔寄与</th><th scope="col">既存1000件 優勢度↔出力利得</th><th scope="col">旧5組 寄与の追従</th><th scope="col">新規30組 寄与の追従</th><th scope="col">新規30組 出力利得の追従</th></tr></thead><tbody><tr><td>絶対IG</td><td>0.366</td><td>0.491</td><td>0.038</td><td>0.035</td><td>0.252</td></tr><tr><td>正IG</td><td>0.425</td><td>0.550</td><td>0.014</td><td>0.013</td><td>0.296</td></tr><tr><td>入力勾配</td><td>0.079</td><td>0.175</td><td>-0.219</td><td>-0.257</td><td>0.049</td></tr><tr><td>入力×勾配</td><td>-0.136</td><td>-0.086</td><td>-0.251</td><td>-0.292</td><td>-0.038</td></tr><tr><td>遮蔽</td><td>0.174</td><td>0.272</td><td>-0.295</td><td>-0.262</td><td>-0.013</td></tr><tr><td>エネルギー</td><td>0.611</td><td>0.541</td><td>-0.574</td><td>-0.559</td><td>0.552</td></tr><tr><td>ランダム</td><td>-0.001</td><td>0.063</td><td>-0.005</td><td>-0.001</td><td>0.039</td></tr><tr><td>全保持</td><td>—</td><td>0.363</td><td>—</td><td>—</td><td>0.265</td></tr></tbody></table>

<table><thead><tr><th scope="col">新規30組・手法</th><th scope="col">−10 dB</th><th scope="col">0 dB</th><th scope="col">+10 dB</th><th scope="col">+20 dB</th></tr></thead><tbody><tr><td>絶対IG</td><td>0.044</td><td>0.274</td><td>0.364</td><td>0.403</td></tr><tr><td>正IG</td><td>0.073</td><td>0.309</td><td>0.417</td><td>0.453</td></tr><tr><td>入力勾配</td><td>0.093</td><td>0.213</td><td>0.022</td><td>-0.107</td></tr><tr><td>入力×勾配</td><td>-0.074</td><td>-0.021</td><td>-0.217</td><td>-0.413</td></tr><tr><td>遮蔽</td><td>0.093</td><td>0.143</td><td>0.037</td><td>-0.191</td></tr></tbody></table>

<table><thead><tr><th scope="col">新規30組・手法</th><th scope="col">J (pp)</th><th scope="col">ΔSI-SDR (dB)</th><th scope="col">ΔCER −10</th><th scope="col">ΔCER 0</th><th scope="col">ΔCER +10</th><th scope="col">ΔCER +20</th></tr></thead><tbody><tr><td>絶対IG</td><td>+12.06</td><td>-3.26</td><td>+10.48</td><td>+32.87</td><td>+23.10</td><td>+14.57</td></tr><tr><td>正IG</td><td>+16.36</td><td>-2.00</td><td>+8.95</td><td>+28.51</td><td>+11.72</td><td>+8.90</td></tr><tr><td>入力勾配</td><td>+5.11</td><td>-5.62</td><td>+13.07</td><td>+44.88</td><td>+50.26</td><td>+52.62</td></tr><tr><td>入力×勾配</td><td>-6.93</td><td>-12.38</td><td>+17.26</td><td>+58.80</td><td>+73.37</td><td>+81.15</td></tr><tr><td>遮蔽</td><td>+4.43</td><td>-5.97</td><td>+12.55</td><td>+48.93</td><td>+49.95</td><td>+54.42</td></tr><tr><td>全保持</td><td>+0.00</td><td>+0.66</td><td>-6.33</td><td>-1.74</td><td>-0.28</td><td>+0.25</td></tr><tr><td>エネルギー</td><td>+9.47</td><td>+1.19</td><td>+8.00</td><td>+24.97</td><td>+9.94</td><td>+2.23</td></tr><tr><td>ランダム</td><td>+0.35</td><td>-7.22</td><td>+17.06</td><td>+59.93</td><td>+61.66</td><td>+45.61</td></tr></tbody></table>

</details>

<details open><summary>LaboroTV Conformer</summary>

<table><thead><tr><th scope="col">手法</th><th scope="col">既存1000件 優勢度↔寄与</th><th scope="col">既存1000件 優勢度↔出力利得</th><th scope="col">旧5組 寄与の追従</th><th scope="col">新規30組 寄与の追従</th><th scope="col">新規30組 出力利得の追従</th></tr></thead><tbody><tr><td>絶対IG</td><td>0.679</td><td>0.726</td><td>0.066</td><td>0.096</td><td>0.352</td></tr><tr><td>正IG</td><td>0.683</td><td>0.735</td><td>0.035</td><td>0.078</td><td>0.360</td></tr><tr><td>入力勾配</td><td>0.212</td><td>0.320</td><td>-0.047</td><td>0.029</td><td>0.159</td></tr><tr><td>入力×勾配</td><td>-0.061</td><td>-0.028</td><td>-0.085</td><td>0.009</td><td>0.034</td></tr><tr><td>遮蔽</td><td>0.265</td><td>0.363</td><td>-0.065</td><td>-0.040</td><td>0.051</td></tr><tr><td>エネルギー</td><td>0.611</td><td>0.541</td><td>-0.574</td><td>-0.559</td><td>0.552</td></tr><tr><td>ランダム</td><td>-0.001</td><td>0.063</td><td>-0.005</td><td>-0.001</td><td>0.039</td></tr><tr><td>全保持</td><td>—</td><td>0.363</td><td>—</td><td>—</td><td>0.265</td></tr></tbody></table>

<table><thead><tr><th scope="col">新規30組・手法</th><th scope="col">−10 dB</th><th scope="col">0 dB</th><th scope="col">+10 dB</th><th scope="col">+20 dB</th></tr></thead><tbody><tr><td>絶対IG</td><td>0.362</td><td>0.618</td><td>0.690</td><td>0.724</td></tr><tr><td>正IG</td><td>0.372</td><td>0.628</td><td>0.690</td><td>0.719</td></tr><tr><td>入力勾配</td><td>0.280</td><td>0.288</td><td>0.259</td><td>0.283</td></tr><tr><td>入力×勾配</td><td>0.124</td><td>0.056</td><td>-0.073</td><td>-0.149</td></tr><tr><td>遮蔽</td><td>0.221</td><td>0.272</td><td>0.187</td><td>0.015</td></tr></tbody></table>

<table><thead><tr><th scope="col">新規30組・手法</th><th scope="col">J (pp)</th><th scope="col">ΔSI-SDR (dB)</th><th scope="col">ΔCER −10</th><th scope="col">ΔCER 0</th><th scope="col">ΔCER +10</th><th scope="col">ΔCER +20</th></tr></thead><tbody><tr><td>絶対IG</td><td>+25.96</td><td>-0.11</td><td>+6.64</td><td>+26.02</td><td>+14.53</td><td>+7.64</td></tr><tr><td>正IG</td><td>+25.40</td><td>+0.10</td><td>+3.02</td><td>+17.84</td><td>+9.21</td><td>+4.59</td></tr><tr><td>入力勾配</td><td>+15.20</td><td>-2.92</td><td>+12.81</td><td>+37.15</td><td>+33.28</td><td>+23.39</td></tr><tr><td>入力×勾配</td><td>-1.21</td><td>-10.52</td><td>+15.20</td><td>+56.75</td><td>+70.27</td><td>+67.00</td></tr><tr><td>遮蔽</td><td>+11.50</td><td>-4.25</td><td>+12.53</td><td>+39.86</td><td>+42.24</td><td>+42.77</td></tr><tr><td>全保持</td><td>+0.00</td><td>+0.66</td><td>-6.33</td><td>-1.74</td><td>-0.28</td><td>+0.25</td></tr><tr><td>エネルギー</td><td>+9.47</td><td>+1.19</td><td>+8.00</td><td>+24.97</td><td>+9.94</td><td>+2.23</td></tr><tr><td>ランダム</td><td>+0.35</td><td>-7.22</td><td>+17.06</td><td>+59.93</td><td>+61.66</td><td>+45.61</td></tr></tbody></table>

</details>













IGは、基準から混合音へ近づく途中の複数の点で認識モデルを調べて近似します。既存1000件では、64点で計算したLaboroTVとWhisperの品質未達率が4割以上だったため、128点で再計算しました。最終未達率は全モデルで4割未満です。上の集計には基準未達の結果も含まれ、発話はJSUTの同一話者です。

<table><thead><tr><th scope="col">生成ASR</th><th scope="col">IG点数</th><th scope="col">未達／分母</th></tr></thead><tbody><tr><td>Whisper large-v3</td><td>128</td><td>394/1000</td></tr><tr><td>CSJ Transformer</td><td>64</td><td>90/1000</td></tr><tr><td>CSJ Conformer</td><td>64</td><td>78/1000</td></tr><tr><td>LaboroTV Conformer</td><td>128</td><td>105/1000</td></tr></tbody></table>
