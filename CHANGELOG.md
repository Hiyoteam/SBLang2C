# 0.0.1
基本功能完成
(函数，变量，循环，条件判断，导入)

# 0.0.2-dev-1
语法改变：
inputto支持多参数  
示例：
```sblang2c
main
    let int a,b
    inputto a,b
    output a
    output "\n"
    output b
end
```
输入`123 321`  
输出
```
123
321
```

# 0.0.2-dev-2
添加 call 语法
用法:`call [funcname] [...args]`
示例见tests/callfunc.sbl

# 0.0.2-dev-3
更新 let 语法：
 - 去除同时赋值功能（你应该使用var）
 - 修复一个可能导致语法错误的bug  
同时更新2numplus.sbl的演示。

# 0.0.3-dev-1
添加 switch-case 语法：
见`tests/switch-case.sbl`

# 0.0.3-dev-2
添加 use 语法：
用于声明使用了SBLang2C内置函数。

添加 randint 内置函数：
randint(int min, int max): 获得从min到max的随机数。

见`tests/random.sbl`

# 0.0.4-dev-1
添加 requests 和 json built-in库。  
使用方式：见`tests/test_web.sbl`  
实现使用了 libcurl 和 nlohmann 的 json 头文件。

# 0.0.4-dev-2
添加 shell built-in 方法。
使用方式：见`tests/test_popen.sbl`

# 0.0.4-dev-3
添加 sleep 方法。
使用方式：`use sleep`,`call sleep (milliseconds)`

# 0.0.4-dev-4
添加 elif syntax.
使用方式：见`tests/guessnum.sbl`

# 0.0.4-dev-5
添加 typing.h 和 is_integer 函数。
更新guessnum.sbl演示。