# video/audio to srt converter
## MP4和MP3转字幕SRT文件

Feel free to use and enjoy

step1.py        convert mp3 to srt
step2.py        convert srt to srt with 5s min_length and 15s max length to avoid too short/long sentences

Below is the version of software
I have CUDA 12.6
use cmd and nvidia-smi to check your cuda version.
refer to requirements.txt for other versions in case compatability.

python version 3.9.0
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124

Whisper is a general-purpose speech recognition model
pip install -U openai-whisper
ref: https://github.com/openai/whisper

pip install imageio
pip install imageio[pyav]
pip install imageio[ffmpeg]


There is a warning say 'weights_only=False' is not recommended. Below can fix.
replace venvwhisper/Lib/site-packages/whisper/__init__.py
with checkpoint = torch.load(fp, map_location=device, weights_only=True)


