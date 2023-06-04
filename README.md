# SBLang2C技术说明书

## 一、基本原理
&emsp;本程序通过将SBLang程序转换为C/C++代码并使用GCC编译来使SBLang程序可以编译为可执行文件，且运行效率更好。
## 二、执行标准
&emsp;使用SBLang-Syntax-V4标准。
## 三、程序组成
 - HEADS (保存在编译Runtime内) 需要引入的头文件
 - HEAD 动态生成，用于声明命名空间
 - EXTERNS 导入由其他文件（或SBLang预定义函数头）定义的函数。
 - FUNCTIONS 用户预定义的函数，动态生成/分析.
 - MAIN 主程序，也就是int main.
## 四、目前进度
pass
## 五、待办事项
