#!/bin/bash
# push v2 episodes ($@ = file stems): video as <stem>_v2.mp4, thumbnail as <stem>_v2_thumb.jpg; drop the v1 files
cd /home/claude/mimzi
R=/home/claude/mimzi-media
for f in "$@"; do
  cp out/$f.mp4 $R/videos/${f}_v2.mp4; cp out/$f.srt $R/videos/${f}_v2.srt; cp out/${f}_thumb.jpg $R/thumbnails/${f}_v2_thumb.jpg
  cp episodes/$f.json $R/pipeline/episodes/
  git -C $R rm -q --ignore-unmatch videos/$f.mp4 videos/$f.srt thumbnails/${f}_thumb.jpg
done
cp mzart.py mzlib.py render.py tts.py thumbnail.py gen.py batch.sh push2.sh $R/pipeline/; cp episodes/schedule.json $R/pipeline/episodes/
cd $R && git add -A && git -c user.name="Claude" -c user.email="noreply@anthropic.com" commit -q -m "Mimzi v2 (longer, new voices): $*

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01SpcQDxdUSh5v9pDK714dKt" && git -c push.negotiate=true push -q origin main 2>&1 | tail -2; git log --oneline | head -1
