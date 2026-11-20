# Mimzi pipeline setup (fresh session)

Needs Python 3 with numpy, PIL, onnxruntime and ffmpeg. Voice = Kokoro ONNX + misaki dictionary (from GitHub).

```bash
git clone https://github.com/honey-bunny-kidz/mimzi-media /home/claude/mimzi-media
GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 https://github.com/hexgrad/misaki /home/claude/hexgrad/misaki
GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 https://github.com/thewh1teagle/kokoro-onnx /home/claude/thewh1teagle/kokoro-onnx
mkdir -p /home/claude/hb/models /home/claude/mimzi/out /home/claude/mimzi/episodes
B=https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0
curl -sL -o /home/claude/hb/models/kokoro.onnx $B/kokoro-v1.0.onnx
curl -sL -o /home/claude/hb/models/voices.bin  $B/voices-v1.0.bin
cp /home/claude/mimzi-media/pipeline/*.py /home/claude/mimzi/
cp /home/claude/mimzi-media/pipeline/episodes/*.json /home/claude/mimzi/episodes/
cd /home/claude/mimzi && python3 render.py episodes/mz001_abc.json out/mz001.mp4            # landscape
# python3 render.py episodes/X_short.json out/X_short.mp4 vertical                         # 9:16 Short
```

- Characters: `mimzi`, `mimzi_wave`, `teddy`; cards `card_A`..`card_Z`, `obj_A`..`obj_Z`; `abc_strip`.
- Backgrounds: `mz_playroom`, `mz_garden` (plus all shared ones in art.py).
- Voices: narrator `mz_narr` (warm), Mimzi `kid_mimzi`, Teddy `kid_teddy`.
- Cast option `"pop": true` = springy pop-in; scenes only fade when the background changes (or `"fade": true`).
- Captions are burned in and written as .srt. Every video ends with a share + subscribe line and a teaser.
- Keep each MP4 under 25 MB (Sonap import limit); use `HB_CRF=26` if bigger.
