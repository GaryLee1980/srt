import whisper
from datetime import timedelta
from zhconv import convert  # 简繁体转换
import warnings
import os


os.system('cls')
warnings.filterwarnings("ignore", message=".*You are using `torch.load` with `weights_only=False`.*")


def transcribe_audio_to_srt(audio_file, output_file="output.srt"):
    """
    转录音频并保存为原始 SRT 文件。
    
    :param audio_file: 输入音频文件路径
    :param output_file: 输出 SRT 文件路径
    """
    # 加载 Whisper 模型
    model = whisper.load_model("small")
    result = model.transcribe(audio_file, fp16=True, language="Chinese")

    # 获取转录段落
    segments = result["segments"]
    for segment in segments:
        print(segment,'\n')

    # 保存为 SRT 文件
    with open(output_file, "w", encoding="utf-8") as f:
        for idx, segment in enumerate(segments, 1):
            start_time = format_time(segment["start"])
            end_time = format_time(segment["end"])
            text = convert(segment["text"], 'zh-cn')
            f.write(f"{idx}\n{start_time} --> {end_time}\n{text}\n\n")


def format_time(seconds):
    """格式化时间为 SRT 格式"""
    td = timedelta(seconds=seconds)
    time_str = str(td).split(".")[0].zfill(8)  # 格式化成 HH:MM:SS
    milliseconds = "000"
    if "." in str(td):
        milliseconds = str(td).split(".")[1][:3]  # 取字符中前三位用函数
    return f"{time_str},{milliseconds}"  # 返回正确的 SRT 格式时间


# 转录音频并生成初始的 SRT 文件
transcribe_audio_to_srt("abc.mp3", "abc.srt")
