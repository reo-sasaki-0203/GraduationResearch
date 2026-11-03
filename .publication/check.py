#!/usr/bin/env python3
"""Validate text-only export links, payload size, and publication exclusions."""
import hashlib,json,re,sys
from pathlib import Path
from urllib.parse import unquote,urlsplit
from bs4 import BeautifulSoup

def check(root):
 root=Path(root).resolve();manifest=json.loads((root/'manifest.json').read_text());errors=[];links=0;soups={}
 def soup(path):
  if path not in soups:soups[path]=BeautifulSoup(path.read_text(),'html.parser')
  return soups[path]
 for name,meta in manifest['files'].items():
  p=root/name
  if not p.is_file():errors.append('Missing '+name);continue
  if hashlib.sha256(p.read_bytes()).hexdigest()!=meta['sha256']:errors.append('Unexpected change '+name)
  if p.stat().st_size>=100*1024*1024:errors.append('File exceeds GitHub limit '+name)
  if p.suffix in {'.png','.jpg','.jpeg','.gif','.svg','.mp3','.wav','.mp4','.pdf','.npy','.npz','.bin','.safetensors'}:errors.append('Disallowed media/data '+name)
  if p.suffix not in {'.html','.md'}:continue
  text=p.read_text()
  for pattern in [r'data:(?:image|audio|video)/',r'/home/(?:data|lab)/',r'-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----',r'\bgh[pousr]_[A-Za-z0-9]{25,}',r'github_pat_[A-Za-z0-9_]{25,}',r'\bhf_[A-Za-z0-9]{25,}']:
   if re.search(pattern,text):errors.append('Excluded information in '+name+' ('+pattern+')')
  if p.suffix!='.html':continue
  s=soup(p)
  if s.select('audio,video,img,iframe,object,embed,canvas,svg'):errors.append('Media/UI remains '+name)
  if not s.find('meta',attrs={'name':'viewport'}):errors.append('Missing viewport '+name)
  for tag in s.select('[href],[src]'):
   raw=tag.get('href',tag.get('src'));u=urlsplit(raw)
   if u.scheme or raw.startswith('//'):continue
   target=(p.parent/unquote(u.path)).resolve() if u.path else p
   links+=1
   if not target.is_relative_to(root) or not target.is_file():errors.append('Missing local link '+name+': '+raw);continue
   if u.fragment and target.suffix=='.html' and not soup(target).find(id=unquote(u.fragment)):errors.append('Missing anchor '+name+': '+raw)
 total=sum((root/n).stat().st_size for n in manifest['files'] if (root/n).is_file())
 if total>=1024**3:errors.append('Site exceeds GitHub Pages limit')
 report={'status':'passed' if not errors else 'failed','html_pages':len(soups),'local_links':links,'files':len(manifest['files']),'bytes':total,'max_file_bytes':manifest['max_file_bytes'],'errors':errors}
 print(json.dumps(report,ensure_ascii=False,indent=2));return not errors
if __name__=='__main__':sys.exit(0 if check(sys.argv[1]) else 1)
