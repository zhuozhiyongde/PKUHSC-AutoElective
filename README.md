# PKUHSC AutoElective

北京大学医学部自动抢课机

## 致谢

* 灵感、项目结构和部分代码来自：[PKUElective2022Spring](https://github.com/Totoro-Li/PKUElective2022Spring)
* 前端登录 Bug 发现：[医学部选课网逆向之内鬼程序员 @Bigscience](https://bbs.pku.edu.cn/v2/post-read.php?bid=198&threadid=18303394)

## 已有功能

* 使用本部刷课机同款 TT 识图的 API，自动识别验证码并登录。
* 智能解析选课轮次信息，支持在选课开始的第一秒自动抢课。
* 支持多课程配置。
* 支持冲突课程配置，可以实现先退冲突课程，再抢新课的功能。

## 使用方法

该项目需要 Python 3。

在使用前，请确保你已经连接至校园网环境。

首先安装依赖：
```bash
pip install -r requirements.txt
```

进入项目根目录，运行：
```bash
python main.py
```

## TODO

* [ ] 使用 Bark 推送抢课结果。