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