# zhenxun_plugin_handle

zhenxun_bot 猜成语插件

移植自[nonebot-plugin-handle](https://github.com/noneplugin/nonebot-plugin-handle)

### 使用

```
@机器人 + 猜成语
```

你有十次的机会猜一个四字词语；

每次猜测后，汉字与拼音的颜色将会标识其与正确答案的区别；

青色 表示其出现在答案中且在正确的位置；

橙色 表示其出现在答案中但不在正确的位置；

当四个格子都为青色时，你便赢得了游戏！

可发送“结束”结束游戏；可发送“提示”查看提示。

### 更新

**2022/6/30**

1. 修改奖励金币，猜或提示的次数越多获得的金币越少，每次减半。
2. 增加词库校验成语：

   第1-47246行取[NLP民工的乐园/ChengYu_Corpus（5W）.txt](https://github.com/fighting41love/funNLP/blob/master/data/%E6%88%90%E8%AF%AD%E8%AF%8D%E5%BA%93/ChengYu_Corpus%EF%BC%885W%EF%BC%89.txt)
中四位成语

   第47247-47822行取[chinese-xinhua/idiom.json](https://github.com/pwxcoo/chinese-xinhua/blob/master/data/idiom.json)
中去重后的四位成语

   第47823-47830行取[汉兜 Handle/polyphones.json](https://github.com/antfu/handle/blob/main/src/data/polyphones.json)
中去重后的四位成语

   第47831-47939行取[汉兜 Handle/idioms.txt](https://github.com/antfu/handle/blob/main/src/data/idioms.txt)
中去重后的四位成语

   第47940-行使用中发现缺少后自行增加的成语
   
   默认只下载了[汉兜 Handle/idioms.txt](https://github.com/antfu/handle/blob/main/src/data/idioms.txt)
   ，请自行手动替换整理后的all_idioms.txt
   

**2022/5/26**[v0.1]

1. 对真寻进行了适配
