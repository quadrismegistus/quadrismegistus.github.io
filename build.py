#!/usr/bin/env python
import os
ROOT = os.path.dirname(__file__)
theme_fn=os.path.join(ROOT,'theme.html')
with open(theme_fn) as theme_f: theme=theme_f.read()

folders=[]
for root, dirs, files in os.walk(".", topdown=False):
    if 'README.md' in files:
        # print(root)
        folders.append(os.path.abspath(os.path.join(ROOT,root)))
        
# print(folders)
# exit()
for root in folders:
    os.chdir(root)
    os.system('pandoc README.md > content.html')

    with open('content.html') as content_f,open('index.html','w') as of:
        content = content_f.read() #.replace('\n  * ','</li>\n<li>')
        content=content.replace('&lt;','<').replace('&gt;','>')
        total = theme.replace('[[CONTENT]]',content)
        of.write(total)
    os.remove('content.html')
