from datetime import timedelta



def time_to_seconds(time_str):
    """将 SRT 时间格式（HH:MM:SS,MMM）转换为秒数"""
    time_part, ms_part = time_str.split(",")
    hours, minutes, seconds = map(int, time_part.split(":"))
    milliseconds = int(ms_part)
    total_seconds = hours * 3600 + minutes * 60 + seconds + milliseconds / 1000
    return total_seconds


def format_time(seconds):
    """格式化时间为 SRT 格式"""
    td = timedelta(seconds=seconds)
    time_str = str(td).split(".")[0].zfill(8)  # 格式化成 HH:MM:SS
    milliseconds = "000"  # 默认毫秒部分为零
    if "." in str(td):
        milliseconds = str(td).split(".")[1][:3]  # 补全毫秒为3位
    return f"{time_str},{milliseconds}"  # 返回正确的 SRT 格式时间

def adjust_srt_segments(input_file="output.srt", output_file="adjusted_output.srt", min_length=5, max_length=15):
    """
    调整 SRT 文件的片段长度，使每个片段的时长在 min_length 和 max_length 秒之间。
    
    :param input_file: 输入的 SRT 文件路径
    :param output_file: 输出的 SRT 文件路径
    :param min_length: 每段字幕的最小时长（秒）
    :param max_length: 每段字幕的最大时长（秒）
    """
    # 读取原始 SRT 文件
    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    adjusted_segments = []
    current_segment = None
    idx = 0

    # 解析 SRT 文件
    while idx < len(lines):
        if lines[idx].strip().isdigit():
            segment_idx = int(lines[idx].strip())
            time_range = lines[idx + 1].strip()
            text = lines[idx + 2].strip()

            # 提取时间
            start_time, end_time = time_range.split(" --> ")
            start_seconds = time_to_seconds(start_time)
            end_seconds = time_to_seconds(end_time)

            # 初始化当前段
            if current_segment is None:
                current_segment = {"start": start_seconds, "end": end_seconds, "text": text}
            else:
                # 合并小于最小长度的段
                if (current_segment["end"] - current_segment["start"]) < min_length:
                    current_segment["end"] = end_seconds
                    current_segment["text"] += " " + text
                else:
                    adjusted_segments.append(current_segment)
                    current_segment = {"start": start_seconds, "end": end_seconds, "text": text}

            # 拆分大于最大长度的段
            while (current_segment["end"] - current_segment["start"]) > max_length:
                split_end = current_segment["start"] + max_length
                adjusted_segments.append({
                    "start": current_segment["start"],
                    "end": split_end,
                    "text": current_segment["text"]
                })
                current_segment["start"] = split_end

            idx += 3  # 跳过当前段
        else:
            idx += 1  # 跳过无效行

    # 添加最后一个片段
    if current_segment:
        adjusted_segments.append(current_segment)

    # 保存调整后的 SRT 文件
    with open(output_file, "w", encoding="utf-8") as f:
        for segment in adjusted_segments:
            start_time = format_time(segment["start"])
            end_time = format_time(segment["end"])
            text = segment["text"]
            f.write(f"{segment_idx}\n{start_time} --> {end_time}\n{text}\n\n")



# 调整 SRT 文件中的每个片段长度
adjust_srt_segments("abc.srt", "adjusted_abc.srt", min_length=5, max_length=15)
