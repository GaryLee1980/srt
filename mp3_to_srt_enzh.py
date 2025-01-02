import whisper
import os
import datetime
from zhconv import convert  # 简繁体转换
from tqdm import tqdm
from pydub.utils import mediainfo


# 获取 mp3 文件列表
def find_files(path, suffix):
    """
    获取 path 下所有指定后缀的文件
    """
    audio_files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.' + suffix):
                audio_files.append(os.path.abspath(os.path.join(root, file)))
    return audio_files


# 秒转时分秒毫秒
def seconds_to_hmsm(seconds):
    """
    将秒数转换为 SRT 格式时间戳
    """
    hours = str(int(seconds // 3600))
    minutes = str(int((seconds % 3600) // 60))
    seconds = seconds % 60
    milliseconds = str(int((seconds - int(seconds)) * 1000))  # 毫秒
    # 补零
    hours = hours.zfill(2)
    minutes = minutes.zfill(2)
    seconds = str(int(seconds)).zfill(2)
    milliseconds = milliseconds.zfill(3)
    return f"{hours}:{minutes}:{seconds},{milliseconds}"


# 获取音频时长
def get_audio_duration(file_path):
    """
    获取音频文件的时长（秒）
    """
    info = mediainfo(file_path)
    return float(info['duration'])


def main():
    # 主文件夹
    file_path = r'.'
    mp3_files = find_files(file_path, suffix='mp3')
    print('音频文件:', mp3_files)

    # 加载 Whisper 模型
    model = whisper.load_model('small')
    # wisper.load_model 参数 'small' 为小模型，'base' 为基础模型，'large' 为大模型, 'huge' 为巨大模型, 'giga' 为超大模型, 'tera' 为特大模型, 'peta' 为拟大模型, 'exa' 为艾克萨模型, 'zetta' 为泽塔模型, 'yotta' 为尧塔模型
    # 模型越大，识别效果越好，但速度越慢, 默认为 'base' base 与 small 的区别在于 base 模型支持更多语言，small 模型支持中英文， base 模型支持 100 多种语言， small 模型支持 2 种语言， base 模型体积大，small 模型体积小， base 模型速度慢，small 模型速度快。
    # 选择合适的模型，可以根据自己的需求选择，如果只需要中英文识别，可以选择 small 模型
    # 模型存放在 ~/.whisper/models/ 目录下，可以通过 whisper.list_models() 查看已下载的模型
    # 如何查看模型的大小，可以通过 whisper.model_size('small') 查看模型的大小
    # 如何下载模型，可以通过 whisper.download_model('small') 下载模型，直接load_model 会自动下载模型
    # 如何删除模型，可以通过 whisper.delete_model('small') 删除模型
    # 如何列出模型，可以通过 whisper.list_models() 列出模型

    for file in tqdm(mp3_files):
        save_file = file[:-3] + "srt"
        if os.path.exists(save_file):
            print(f"{save_file} 已存在，跳过处理。")
            continue

        # 打印音频信息
        duration = get_audio_duration(file)
        print(f"正在处理文件: {file} (时长: {seconds_to_hmsm(duration)})")

        # 获取中文转录
        res_zh = model.transcribe(file, task='transcribe', fp16=False, language='Chinese')
        # model.transcribe 参数 task='transcribe' 为中文转录，task='translate' 为英文翻译, language='Chinese' 为中文识别, language='English' 为英文识别, fp16=True 为使用 FP16 模型, fp16=False 为使用 FP32 模型
        # res_zh['segments'] 为返回的字幕列表，每个字幕为一个字典，包含 'start'（开始时间）、'end'（结束时间）、'text'（文本内容), 'confidence'（置信度）, 'speaker'（说话者）, 'language'（语言）, 'language_code'（语言代码） 等字段
    
        # 获取英文翻译
        res_en = model.transcribe(file, task='translate', fp16=False)

        # 写入双字幕到 SRT 文件
        with open(save_file, 'w', encoding='utf-8') as f:
            i = 1
            for r_zh, r_en in zip(res_zh['segments'], res_en['segments']):
                f.write(f"{i}\n")
                f.write(f"{seconds_to_hmsm(r_zh['start'])} --> {seconds_to_hmsm(r_zh['end'])}\n")
                f.write(f"{convert(r_zh['text'], 'zh-cn')}\n")  # 中文转简体
                f.write(f"{r_en['text']}\n\n")  # 英文翻译
                i += 1

        print(f"完成处理文件: {file}")


if __name__ == "__main__":
    main()
