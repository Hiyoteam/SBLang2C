<h1 align="center">✨SBLang2C✨</h1>
<p align="center">简单的SBLang编译器实现
<br><img src="https://wakatime.com/badge/user/446b98ad-62be-496b-bda1-7cec523e3316/project/c0644e57-360b-4f28-8e2f-2ea80eae01d0.svg"></p>


## 一、基本原理
&emsp;本程序通过将SBLang程序转换为C++代码并使用G++编译来使SBLang程序可以编译为可执行文件，且运行效率更好。
## 二、执行标准
&emsp;使用SBLang-Syntax-V4标准。
## 三、使用方式
`python3 sblang2c.py [...options] [filename]`  
&emsp;可用的Options:
 - --no-compile, 仅翻译为c++而不编译
 - --debug, 显示所有调试信息
 - --gcc-binary=xxx, 制定g++可执行文件位置

Examples:  
`python3 sblang2c.py --debug some_file.sbl`
编译some_file.sbl, 输出全部调试信息。  

`python3 sblang2c.py --no-compile some_file.sbl`
转换some_file.sbl, 不进行编译。

`python3 sblang2c.py --no-compile --debug some_file.sbl`
转换some_file.sbl, 不进行编译并打印所有调试信息。

`python3 sblang2c.py --gcc-binary=/opt/homebrew/bin/g++-13 --debug some_file.sbl`
转换some_file.sbl, 使用MacOS Homebrew安装的G++ 13进行编译并打印所有调试信息。

## 四、程序组成
 - HEADS (保存在编译Runtime内) 需要引入的头文件
 - HEAD 动态生成，用于声明命名空间
 - EXTERNS 导入由其他文件（或SBLang预定义函数头）定义的函数。
 - FUNCTIONS 用户预定义的函数，动态生成/分析.
 - MAIN 主程序，也就是int main.
## 五、目前进度
函数，变量，循环，条件判断
## 六、待办事项
去除let语句，自动检测目标值类型