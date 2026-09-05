# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
src = sys.argv[1]
t = open(src, encoding='utf-8-sig').read()
t = t.replace('TitleCaption\t\tPARQUET', 'TitleCaption\t\tLimelight * Lemonade Jam')
t = t.replace('ConfigPreviewText2\tPARQUET\\n(C)YUZUSOFT/JUNOS inc.',
              'ConfigPreviewText2\tLimelight * Lemonade Jam\\n(C)YUZUSOFT')
open(sys.argv[2], 'w', encoding='utf-8', newline='\n').write(t)
print('title/copyright fixed ->', sys.argv[2])
