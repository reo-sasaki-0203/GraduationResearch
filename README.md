# 音声認識・Whisper研究資料（軽量公開版）

GitHub Pagesの入口は [`index.html`](index.html)。手引き18章、研究計画、助言集、関連する過去実験の説明を収録します。

画像・音声・動画・データセット・モデル・個別発話の実験出力・個人用メモ・会話ログ・認証情報は収録しません。元の研究フォルダは変更・削除しません。数式表示に必要なKaTeXとフォントだけを同梱します。

## 公開

GitHubの Settings → Pages → Deploy from a branch → `main` / `/(root)` を指定します。

## HTML更新の継続方針

ユーザーの継続指示（2026-11-03）：この研究資料のHTMLを編集・更新するときは、1文字の修正や見た目・リンクだけの変更も含め、毎回このREADMEの最新版を確認し、公開用軽量版の再生成・検査・commit・push・GitHub Pagesの公開確認まで行います。元のMarkdown/JSON、CSS/JavaScriptを通じた変更も対象です。ローカル更新だけで完了にせず、通常の反映について再承認を求めません。

公開版に差分が出ないHTML変更でも、余計な公開内容を足さず、空コミット等で更新を記録してpushします。個人メモ・会話ログ・認証情報・大容量ファイル等の除外は維持します。pushや公開ができなかった場合は未反映の範囲と理由を報告し、完了と扱いません。

公開サイト：<https://reo-sasaki-0203.github.io/GraduationResearch/>

## 更新

元資料があるPCで、公開リポジトリ内から実行します。

```sh
python -m pip install -r .publication/requirements.txt
python .publication/build.py --source ../GraduationResearch --output .
python .publication/check.py .
git add -A
git commit --allow-empty -m "Update public research documents"
git push origin main
```

収録元と容量は [manifest.json](manifest.json) を参照。ローカルでの表示確認は `python -m http.server 8787`。

GitHubの制限は、通常ファイル100MiB、GitHub Pagesサイト1GBです。公開前にファイル別・合計サイズを検査します。

- [ファイルの容量制限（GitHub公式）](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github)
- [GitHub Pagesの制限（GitHub公式）](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits)

公開版の文章には、保存済み結果・過去の説明・未実施の提案が含まれます。各ページの確認日と記述を参照してください。
