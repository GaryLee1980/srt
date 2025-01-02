# -*- encoding: utf-8 -*-
from gtts import gTTS

text = """
从前，有一座美丽的大森林，森林里住着许多小动物，它们每天过着无忧无虑的生活。有一天，森林里来了几个伐木工人，
他们拿着斧头和锯子，把一棵棵树给砍倒了。几天下来，裸露的土地不断扩大，森林里的树木不断减少。大象看了之后非常生气，
他和几个好朋友决定把这些伐木工人抓起来，送到动物法庭上。第二天，大象他们就把伐木工人给抓了起来，送到了动物法庭上。
许多旁观者都纷纷议论起来，猴法官说：“安静，安静，大象你们把这些人抓来是怎么回事?”大象说：“这些人乱砍树木，破坏我们的家园。
大象的好朋友小猴说：“对呀，他们把树给砍光了，我们就不能在树上荡秋千了。”小鸟也说：”猴法官，要是没有树木，我们就不能筑巢了。
长颈鹿说：“要是没有树木，我们就吃不到树叶了，我们会饿死的。”听到这里，猴法官对伐木工人说：“你们乱砍树木是不对的，
没有了树木，我们动物就无法生存，同样也会给你们人类带来灾难的。”听了这些话，伐木工人觉得很惭愧，知道自己错了，
他们保证以后不再乱砍树木破坏森林了，还在森林入口立了一块告示牌，上面写着：“保护森林，人人有责。”从此以后，人们不再破坏森林，
动物和人类和平相处，大家都过着幸福、快乐的生活。
"""

tts = gTTS(text=text, lang='zh-CN')
tts.save("XXX.mp3")
tts = gTTS(text=text, lang='zh-CN', slow=True, lang_check=True, tld='cn',)