#!/bin/bash
# render one episode: $1 = file stem
cd /home/claude/mimzi
f=$1
[ -f out/$f.mp4 ] && exit 0
python3 render.py episodes/$f.json out/$f.tmp.mp4 > logs/$f.log 2>&1 && mv out/$f.tmp.mp4 out/$f.mp4 && for x in srt; do mv -f out/$f.tmp.$x out/$f.$x 2>/dev/null; done; mv -f out/$f.tmp_thumb.jpg out/${f}_thumb.jpg 2>/dev/null
echo "$f done $(date +%T)" >> logs/progress.txt
