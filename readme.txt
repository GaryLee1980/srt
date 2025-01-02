pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124


pip install -U openai-whisper

pip install imageio[pyav]
pip install imageio[ffmpeg]


replace venvwhisper/Lib/site-packages/whisper/__init__.py

with checkpoint = torch.load(fp, map_location=device, weights_only=True)


