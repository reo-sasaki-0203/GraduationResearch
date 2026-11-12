#!/usr/bin/env python3
"""Export an allowlisted, text-only research site; never modify source documents."""
from __future__ import annotations
import argparse, hashlib, html, json, os, re, shutil
from pathlib import Path
from urllib.parse import unquote, urlsplit
import markdown
from bs4 import BeautifulSoup, NavigableString

IG=Path('ASR/whisper_ig_reconstruction')
HUB=IG/'notes/research_hub'
GUIDE=IG/'guide'
HUB_PAGES=['token-word-ig','token-extraction-hypothesis','old100-cleanup','positive-fractions-pilot','utterances','results','positive-ig95','main1000-results','status','plan','advice-response','score','denoising-history','advice','advice/20261014','advice/undated','advice/questions']
RESULT_EXPORTS={'token-word-ig':IG/'results/comparisons/positive_ig_fractions/main1000_20261110_pos908580_pilot10_v1/token_ig/index.html','positive-fractions-pilot':IG/'results/comparisons/positive_ig_fractions/main1000_20261110_pos908580_pilot10_v1/index.html','utterances':IG/'results/views/by_utterance/index.html','results':IG/'results/experiments/index.html','positive-ig95':IG/'results/comparisons/positive_ig95/main1000_20261109_pos95_v1/index.html','main1000-results':IG/'results/experiments/main1000_20261010/index.html'}
GUIDE_PAGES=['index','audio','transformer','whisper','pipeline','xai/index','xai/ig','reconstruction','evaluation','xai/shap','xai/lime','xai/grad-cam','xai/occlusion','xai/saliency','xai/other','analysis','glossary','sources']
EXTRA_MD=['README.md','ASR/README.md','ASR/asr_prosody_probe/README.md','ASR/whisper_pause_attention/README.md','ASR/whisper_pause_attention/reports/internal_pause_experiment_report.md','SR/README.md']
LABELS={'token-word-ig':'トークン毎のIG計算の結果：10音声','token-extraction-hypothesis':'トークンIG抽出の仮説と先行研究','old100-cleanup':'旧100件の整理・記録保全','positive-fractions-pilot':'正IG90・85・80：10音声','utterances':'音声・メル比較（サーバ版）','results':'実験結果一覧','positive-ig95':'正のIG95・1000件比較','main1000-results':'1000件・IG＋DeepFilterNet3','status':'現在地・結果','plan':'研究計画','advice-response':'助言への対応','score':'Fとセル寄与','denoising-history':'ノイズ除去の歴史','advice':'助言集'}
CSS='''*{box-sizing:border-box}html{scroll-padding-top:20px}body{margin:0;color:#213445;background:#f5f7f8;font:16px/1.85 system-ui,-apple-system,sans-serif}a{color:#086e7e;overflow-wrap:anywhere}a:focus-visible,summary:focus-visible{outline:3px solid #dfaa42;outline-offset:3px}.public-header{display:flex;align-items:center;justify-content:space-between;gap:15px;flex-wrap:wrap;padding:18px max(20px,calc((100vw - 1280px)/2));background:white;border-bottom:1px solid #dce5e8}.public-header a{text-decoration:none;font-weight:700}.public-header small{color:#526777}.public-layout{display:grid;grid-template-columns:230px minmax(0,1fr);gap:24px;max-width:1280px;margin:24px auto;padding:0 20px}.public-side{position:sticky;top:16px;align-self:start;max-height:calc(100vh - 32px);overflow-y:auto}.public-side nav{display:grid;gap:5px}.public-side a{display:block;padding:5px 8px;font-size:13px;text-decoration:none}.public-side a[aria-current]{background:#e0efec;border-radius:5px;font-weight:700}.public-side summary{font-size:14px;padding:5px 8px;cursor:pointer}.public-side details details{margin-bottom:10px}.public-main{min-width:0;max-width:100%;padding:28px 34px;border:1px solid #dce5e8;border-radius:12px;background:white}.public-main h1{font-size:clamp(25px,3vw,34px);line-height:1.5}.public-main h2{font-size:22px}.public-main p,.public-main li{overflow-wrap:anywhere}.public-main img,.public-main audio,.public-main video{display:none}.public-main table{border-collapse:collapse;width:100%;font-size:14px}.public-main th,.public-main td{padding:10px;border-bottom:1px solid #dce5e8;text-align:left;min-width:65px}.public-main th{background:#edf4f5}.table-scroll,.table-wrap{max-width:100%;overflow-x:auto}.public-main pre{max-width:100%;overflow:auto;font-size:13px;padding:14px;background:#f0f4f6;border-radius:6px}.public-main code{font-size:.9em;overflow-wrap:anywhere}.public-main details{margin:12px 0}.public-main summary{cursor:pointer}.public-main blockquote{margin:18px 0;padding:12px 18px;border-left:3px solid #86b4ad;background:#f3f8f7}.public-footer{font-size:12px;color:#526777;margin-top:32px;padding-top:14px;border-top:1px solid #dce5e8}.public-main .search,.public-main .filters,.public-main .badge-row{display:none}.public-main .advice-card{padding:18px;margin:16px 0;border:1px solid #dce5e8;border-radius:8px}.public-main .badge{font-size:12px}.public-main .record-top{font-size:12px;color:#526777}.math-display,.katex-display{max-width:100%;overflow-x:auto;overflow-y:hidden}.public-cards{display:grid;grid-template-columns:1fr 1fr;gap:14px}.public-cards section{padding:16px;border:1px solid #dce5e8;border-radius:8px}.public-cards h2{margin:0 0 8px}.public-cards ul{padding-left:20px}.math-error{white-space:pre-wrap;color:#8e2424}@media(max-width:800px){.public-layout{display:block;margin:12px 0;padding:0 10px}.public-side{position:static;max-height:none;margin-bottom:12px}.public-side>.mobile-nav:not([open])>nav{display:none}.public-side nav{grid-template-columns:repeat(2,minmax(0,1fr))}.public-main{padding:20px 16px}.public-header{padding:14px 18px}.public-cards{grid-template-columns:1fr}.public-main h2{font-size:20px}}@media print{.public-side,.public-header{display:none}.public-layout{display:block}.public-main{border:0;padding:0}}
'''
NAV_JS="""'use strict';const nav=document.querySelector('.mobile-nav');if(matchMedia('(max-width:800px)').matches)nav.open=false;"""
PRIVATE_PARTS={'.personal','sources','verification','backups','data','datasets','models','checkpoints','logs','outputs','node_modules','.venv','espnet'}

def scrub(text,source):
    text=text.replace(str(source.resolve())+'/', '')
    text=re.sub(r'/home/(?:data|lab)/[^/\s<>`"\']+/', '[ローカルホーム]/',text)
    text=re.sub(r'https?://(?:127\.0\.0\.1|localhost)(?::\d+)?[^\s<>"\']*','[ローカル専用URL]',text)
    text=re.sub(r'[\w.+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', '[メールアドレス省略]',text)
    return text

def build(source,out):
    source=source.resolve();out=out.resolve()
    if out==source or out.is_relative_to(source):raise ValueError('Export must be separate from original research')
    out.mkdir(parents=True,exist_ok=True)
    mapping={}
    for slug in GUIDE_PAGES:mapping[(source/GUIDE/(slug+'.html')).resolve()]=GUIDE/(slug+'.html')
    for slug in HUB_PAGES:
        # Export the authored explanation, never the private per-utterance table.
        if slug in ['utterances','positive-fractions-pilot']:mapping[(source/HUB/(slug+'.md')).resolve()]=HUB/(slug+'.html')
        if slug in RESULT_EXPORTS:mapping[(source/RESULT_EXPORTS[slug]).resolve()]=HUB/(slug+'.html')
        mapping[(source/HUB/(slug+'.html')).resolve()]=HUB/(slug+'.html')
        if (source/HUB/(slug+'.md')).exists():mapping[(source/HUB/(slug+'.md')).resolve()]=HUB/(slug+'.html')
    mapping[(source/HUB/'README.md').resolve()]=HUB/'index.html';mapping[(source/HUB/'index.html').resolve()]=HUB/'index.html'
    mapping[(source/IG/'index.html').resolve()]=IG/'index.html'
    for name in EXTRA_MD:
        p=Path(name);target=Path('overview.html') if p==Path('README.md') else p.parent/'index.html' if p.name=='README.md' else p.with_suffix('.html')
        mapping[(source/p).resolve()]=target
    generated={};inputs={};removed=0
    def write(path,text):generated[str(path)]=text.encode('utf-8')
    def target_href(raw,original,target):
        u=urlsplit(html.unescape(raw))
        if u.scheme in {'https','http'}:return raw if u.hostname not in {'localhost','127.0.0.1'} else None
        if u.scheme or raw.startswith('//'):return None
        if not u.path:return '#'+u.fragment if u.fragment else None
        local=(original.parent/unquote(u.path)).resolve()
        dest=mapping.get(local)
        if dest is None:return None
        return os.path.relpath(dest,target.parent).replace(os.sep,'/')+(('#'+u.fragment) if u.fragment else '')
    def clean(body,original,target):
        nonlocal removed
        soup=BeautifulSoup(body,'html.parser')
        for node in list(soup.select('.private-token-results,.advice-answer')):
            node.decompose();removed+=1
        for node in list(soup.select('img,picture,audio,video,source,track,iframe,object,embed,canvas,svg,script,style,link,form,input,select,button,footer,.search,.filters,.rp-breadcrumb,.source-link,.status-line')):
            if node.parent is not None:node.decompose();removed+=1
        # Provenance links into private chat history are not part of the public edition.
        for a in list(soup.select('a[href]')):
            raw=a['href'];dest=target_href(raw,original,target)
            if dest:a['href']=dest
            else:a.unwrap()
        for node in soup.find_all(True):
            for attr in list(node.attrs):
                if attr.startswith('on') or attr in {'src','srcset','poster','action','formaction'} or (attr.startswith('data-') and attr!='data-tex'):del node[attr]
        for text in list(soup.find_all(string=True)):
            if not isinstance(text,NavigableString):continue
            new=scrub(str(text),source)
            if new!=str(text):text.replace_with(new)
        for table in soup.find_all('table'):
            if not table.parent.has_attr('class') or not ({'table-scroll','table-wrap'}&set(table.parent['class'])):
                wrap=soup.new_tag('div',attrs={'class':'table-scroll'});table.wrap(wrap)
        return str(soup)
    def title_of(body,fallback):
        s=BeautifulSoup(body,'html.parser');h=s.find('h1');return h.get_text(' ',strip=True) if h else fallback
    nav_groups=[('結果を見る',[(HUB/(s+'.html'),LABELS[s]) for s in ['results','token-word-ig','utterances','positive-fractions-pilot','positive-ig95','main1000-results']]),('研究を進める',[(HUB/(s+'.html'),LABELS[s]) for s in ['token-extraction-hypothesis','plan','advice','advice-response']]),('学ぶ',[(GUIDE/'index.html','手引き・全18章'),(HUB/'denoising-history.html','ノイズ除去の歴史'),(HUB/'score.html','Fとセル寄与')]),('過去の研究',[(Path('ASR/asr_prosody_probe/index.html'),'初期の解析基盤'),(Path('ASR/whisper_pause_attention/index.html'),'pause・attention'),(Path('ASR/whisper_pause_attention/reports/internal_pause_experiment_report.html'),'pause実験レポート'),(Path('SR/index.html'),'旧音声認識実験')])]
    def wrap(title,body,path):
        rel=lambda p:os.path.relpath(p,path.parent).replace(os.sep,'/')
        nav=''
        for label,entries in nav_groups:
            nav+='<details open><summary>'+label+'</summary>'+''.join('<a href="'+html.escape(rel(p))+'"'+(' aria-current="page"' if p==path else '')+'>'+html.escape(name)+'</a>' for p,name in entries)+'</details>'
        nav+='<details><summary>手引きの章一覧</summary>'+''.join('<a href="'+html.escape(rel(GUIDE/(slug+'.html')))+'">'+html.escape(guide_titles[slug])+'</a>' for slug in GUIDE_PAGES)+'</details>'
        assets='assets/'
        return '<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+html.escape(title)+' | 研究資料</title><meta http-equiv="Content-Security-Policy" content="default-src \'self\'; script-src \'self\'; style-src \'self\' \'unsafe-inline\'; font-src \'self\'; img-src \'none\'; media-src \'none\'; connect-src \'none\'; object-src \'none\'; frame-src \'none\'"><link rel="stylesheet" href="'+rel(Path('assets/guide.css'))+'"><link rel="stylesheet" href="'+rel(Path('assets/vendor/katex/katex.min.css'))+'"><link rel="stylesheet" href="'+rel(Path('assets/public.css'))+'"><script defer src="'+rel(Path('assets/vendor/katex/katex.min.js'))+'"></script><script defer src="'+rel(Path('assets/math.js'))+'"></script><script defer src="'+rel(Path('assets/navigation.js'))+'"></script></head><body><header class="public-header"><a href="'+rel(Path('index.html'))+'">研究資料</a><small>テキスト版</small></header><div class="public-layout"><aside class="public-side"><details class="mobile-nav" open><summary>目次・ページを選ぶ</summary><nav>'+nav+'</nav></details></aside><main class="public-main" id="main">'+body+'<footer class="public-footer"><a href="'+rel(Path('index.html'))+'">研究資料の入口</a> · 画像・音声を省いた公開用テキスト版</footer></main></div></body></html>'
    guide_titles={}
    for slug in GUIDE_PAGES:
        p=source/GUIDE/(slug+'.html');guide_titles[slug]=title_of(p.read_text(),slug)
    seen=set()
    for original,target in mapping.items():
        if target in seen or original.name=='README.md' and original.parent==source/HUB or original==source/IG/'index.html':continue
        seen.add(target)
        raw=original.read_text();inputs[str(original.relative_to(source))]=hashlib.sha256(raw.encode()).hexdigest()
        if original.suffix=='.html':
            soup=BeautifulSoup(raw,'html.parser');main=soup.find('main');body=main.decode_contents() if main else (soup.body.decode_contents() if soup.body else raw)
        else:body=markdown.markdown(raw,extensions=['tables','fenced_code','toc','sane_lists'])
        body=clean(body,original,target);title=title_of(body,original.stem)
        if original==source/HUB/'utterances.md':body='<p>この公開版は説明のみです。音声・個別発話の比較は、サーバ版の「実験結果一覧」から開いてください。</p>'+body
        write(target,wrap(title,body,target))
    write(HUB/'status.html','<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="research-redirect" content="results.html"><script defer src="../../../../assets/redirect.js"></script><noscript><meta http-equiv="refresh" content="0;url=results.html"></noscript><title>実験結果一覧へ</title></head><body><a href="results.html">実験結果一覧へ</a></body></html>')
    # The hub entry is rebuilt from its public topics; management and personal tools stay local.
    cards='<h1>研究記録</h1><ul>'+''.join('<li><a href="'+s+'.html">'+LABELS[s]+'</a></li>' for s in ['results','utterances','positive-fractions-pilot','positive-ig95','main1000-results','plan','advice','advice-response','score','denoising-history'])+'</ul>'
    write(HUB/'index.html',wrap('研究記録',cards,HUB/'index.html'))
    cards='<h1>音声の重要度と再構成</h1><ul><li><a href="notes/research_hub/results.html">実験結果一覧</a></li><li><a href="notes/research_hub/positive-ig95.html">正のIG95・1000件比較</a></li><li><a href="notes/research_hub/main1000-results.html">1000件・IG再構成＋DeepFilterNet3の統合比較</a></li><li><a href="notes/research_hub/plan.html">研究計画</a></li><li><a href="notes/research_hub/advice.html">助言集</a></li><li><a href="guide/index.html">研究の手引き・全18章</a></li></ul>'
    write(IG/'index.html',wrap('音声の重要度と再構成',cards,IG/'index.html'))
    groups=[('結果を見る',[(HUB/'results.html','実験結果一覧'),(HUB/'token-word-ig.html','トークン毎のIG計算の結果：10音声'),(HUB/'utterances.html','音声・メル比較（サーバ版）'),(HUB/'positive-fractions-pilot.html','正IG90・85・80：10音声'),(HUB/'positive-ig95.html','正のIG95・1000件比較'),(HUB/'main1000-results.html','1000件・IG再構成＋DeepFilterNet3の統合比較')]),('研究を進める',[(HUB/'token-extraction-hypothesis.html','トークンIG抽出の仮説と先行研究'),(HUB/'plan.html','研究計画'),(HUB/'advice.html','助言集'),(HUB/'advice-response.html','助言への対応')]),('学ぶ',[(GUIDE/'index.html','研究の手引き・全18章'),(HUB/'denoising-history.html','ノイズ除去の歴史'),(HUB/'score.html','Fとセル寄与')]),('過去の実験を読む',nav_groups[-1][1]),('フォルダの説明',[(Path('overview.html'),'研究フォルダ全体'),(Path('ASR/index.html'),'ASRの構成'),(Path('SR/index.html'),'SRの構成')])]
    body='<h1>音声認識・Whisper研究資料</h1><p>手引き・研究計画・助言と実験の説明を、スマホから文章で読めるようにまとめています。</p><div class="public-cards">'
    for name,entries in groups:body+='<section><h2>'+name+'</h2><ul>'+''.join('<li><a href="'+p.as_posix()+'">'+label+'</a></li>' for p,label in entries)+'</ul></section>'
    body+='</div>'
    write(Path('index.html'),wrap('音声認識・Whisper研究資料',body,Path('index.html')))
    write(Path('assets/public.css'),CSS);write(Path('assets/navigation.js'),NAV_JS)
    generated['assets/redirect.js']=(source/HUB/'assets/redirect.js').read_bytes()
    for name in ['guide.css','math.js']:
        generated['assets/'+name]=(source/GUIDE/'assets'/name).read_bytes()
    vendor=source/GUIDE/'assets/vendor/katex'
    for p in vendor.rglob('*'):
        if p.is_file() and (p.name in {'katex.min.js','katex.min.css','LICENSE','LICENSE.txt'} or p.suffix=='.woff2'):
            data=p.read_bytes()
            if p.name=='katex.min.css':data=re.sub(r'src:([^;]+)',lambda m:'src:'+m.group(1).split(',')[0],data.decode()).encode()
            generated['assets/vendor/katex/'+p.relative_to(vendor).as_posix()]=data
    # Approved Markdown sources only, with private/media/local-only links stripped.
    md_inputs=[source/Path(n) for n in EXTRA_MD]+[source/HUB/(s+'.md') for s in HUB_PAGES if (source/HUB/(s+'.md')).exists()]
    for original in md_inputs:
        path=Path('text-sources')/original.relative_to(source);text=scrub(original.read_text(),source)
        text=re.sub(r'<!-- private-token-results:start -->[\s\S]*?<!-- private-token-results:end -->','',text)
        text=re.sub(r'!\[[^\]]*\]\([^)]*\)','',text)
        def mdlink(m):
            dest=target_href(m.group(2),original,path)
            return '['+m.group(1)+']('+dest+')' if dest else m.group(1)
        text=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',mdlink,text)
        text=re.sub(r'<(?:img|audio|video|iframe|svg)\b[\s\S]*?</(?:audio|video|iframe|svg)>|<img\b[^>]*>','',text)
        write(path,text.rstrip()+'\n')
    write(Path('.nojekyll'),'')
    write(Path('.gitignore'),'''# Only the public text export belongs in this repository.\n.personal/\n**/.personal/\n**/sources/user-history*\n**/data/\n**/datasets/\n**/models/\n**/checkpoints/\n**/results/\n**/outputs/\n**/logs/\n**/backups/\n**/espnet/\n**/.venv/\n**/__pycache__/\n.env*\n*.pem\n*.key\n*.pt\n*.pth\n*.bin\n*.safetensors\n*.npy\n*.npz\n*.csv\n*.wav\n*.mp3\n*.m4a\n*.flac\n*.ogg\n*.mp4\n*.mov\n*.png\n*.jpg\n*.jpeg\n*.gif\n*.webp\n*.svg\n*.pdf\n*.zip\n*.tar*\n*.pyc\n''')
    write(Path('README.md'),'''# 音声認識・Whisper研究資料（軽量公開版）\n\nGitHub Pagesの入口は [`index.html`](index.html)。手引き18章、研究計画、助言集、関連する過去実験の説明を収録します。\n\n画像・音声・動画・データセット・モデル・個別発話の実験出力・個人用メモ・会話ログ・認証情報は収録しません。元の研究フォルダは変更・削除しません。数式表示に必要なKaTeXとフォントだけを同梱します。\n\n## 公開\n\nGitHubの Settings → Pages → Deploy from a branch → `main` / `/(root)` を指定します。\n\n## HTML更新の継続方針\n\nユーザーの継続指示（2026-11-03）：この研究資料のHTMLを編集・更新するときは、1文字の修正や見た目・リンクだけの変更も含め、毎回このREADMEの最新版を確認し、公開用軽量版の再生成・検査・commit・push・GitHub Pagesの公開確認まで行います。元のMarkdown/JSON、CSS/JavaScriptを通じた変更も対象です。ローカル更新だけで完了にせず、通常の反映について再承認を求めません。\n\n公開版に差分が出ないHTML変更でも、余計な公開内容を足さず、空コミット等で更新を記録してpushします。個人メモ・会話ログ・認証情報・大容量ファイル等の除外は維持します。pushや公開ができなかった場合は未反映の範囲と理由を報告し、完了と扱いません。\n\n公開サイト：<https://reo-sasaki-0203.github.io/GraduationResearch/>\n\n## 更新\n\n元資料があるPCで、公開リポジトリ内から実行します。\n\n```sh\npython -m pip install -r .publication/requirements.txt\npython .publication/build.py --source ../GraduationResearch --output .\npython .publication/check.py .\ngit add -A\ngit commit --allow-empty -m "Update public research documents"\ngit push origin main\n```\n\n収録元と容量は [manifest.json](manifest.json) を参照。ローカルでの表示確認は `python -m http.server 8787`。\n\nGitHubの制限は、通常ファイル100MiB、GitHub Pagesサイト1GBです。公開前にファイル別・合計サイズを検査します。\n\n- [ファイルの容量制限（GitHub公式）](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github)\n- [GitHub Pagesの制限（GitHub公式）](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits)\n\n公開版の文章には、保存済み結果・過去の説明・未実施の提案が含まれます。各ページの確認日と記述を参照してください。\n''')
    write(Path('AGENTS.md'),'# 公開研究資料の更新\n\nHTML・元のMarkdown/JSON・表示用CSS/JavaScriptを変更するときは、変更の大小にかかわらず毎回、作業前に公開リポジトリの最新のREADME.mdを読む。READMEに従い軽量公開版を生成・検査し、mainへcommit・pushし、GitHub Pagesのデプロイ成功と公開URLを確認する。ローカル更新だけで完了としない。通常の反映に再承認を求めない。\n\n公開差分がないHTML変更も空コミット等で反映作業を記録してpushする。個人メモ・会話ログ・認証情報・大容量データ等の除外は維持する。失敗した場合は未反映の範囲と理由を明示し、完了と報告しない。元資料がある環境では、元の正本を編集してからビルドし、生成HTMLだけの直接修正で終わらせない。\n\n公開先：reo-sasaki-0203/GraduationResearch\n公開URL：https://reo-sasaki-0203.github.io/GraduationResearch/\nユーザーの継続指示：2026-11-03\n')
    write(Path('.publication/requirements.txt'),'beautifulsoup4>=4.12,<5\nMarkdown>=3.5,<4\n')
    generated['.publication/build.py']=Path(__file__).read_bytes()
    checker=Path(__file__).with_name('check.py')
    if checker.exists():generated['.publication/check.py']=checker.read_bytes()
    # Refuse unexpected preexisting public files instead of silently deleting them.
    previous=out/'manifest.json'
    if previous.exists():
        old=json.loads(previous.read_text())
        for name in old.get('files',{}):
            if name not in generated and (out/name).is_file():(out/name).unlink()
    for name,data in generated.items():
        target=out/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
    manifest={'format':'research-text-publication-v1','html_pages':sum(n.endswith('.html') for n in generated),'file_count':len(generated),'bytes':sum(map(len,generated.values())),'max_file_bytes':max(map(len,generated.values())),'removed_media_and_controls':removed,'inputs':inputs,'files':{n:{'bytes':len(d),'sha256':hashlib.sha256(d).hexdigest()} for n,d in sorted(generated.items())},'excluded':['personal notes and check state','conversation history and operation logs','media and embedded media','datasets, model weights, caches and virtual environments','per-utterance result files','third-party ESPnet checkout']}
    (out/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in manifest.items() if k not in {'files','inputs'}},ensure_ascii=False))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--source',type=Path,required=True);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args();build(args.source,args.output)
