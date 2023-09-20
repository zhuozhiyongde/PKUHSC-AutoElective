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
* 支持使用 Bark 为 iOS 设备推送通知。

## 使用方法

### 安装依赖
该项目需要 Python 3。


首先安装依赖：
```bash
pip install -r requirements.txt
```
### 配置信息
在使用前，请确保你已经连接至校园网环境。

复制 `config.sample.ini` ，重命名为`config.ini` ，然后根据 `config.sample.ini` 中的说明，创建 `config.ini` 文件，并填写相关信息。

获取 `batch_name` 轮次信息、 `class` 课程号，可以通过在全校课程查询页面中查找课程信息获得。

你所需要的选课课程号需要从全校课程查询中获得：

![查询操作](https://cdn.arthals.ink/bed/2023/09/d33a3d24070f6fb773b9e5102c486a25.png)

### 运行

请务必确保你已经链接至校园网环境。

进入项目根目录，运行：
```bash
python main.py
```
### 效果

![效果展示](https://cdn.arthals.ink/bed/2023/09/9712a071938088ed407947856a47a94d.png)

![选课结果](https://cdn.arthals.ink/bed/2023/09/dc200b786da649afe615557960cabd1d.png)