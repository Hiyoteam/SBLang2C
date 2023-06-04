class CompileError(BaseException):
    pass
def output(runtime,line):
    return f"cout << {line[1]};\n"
def main(runtime,line):
    runtime.heads+=["bits/stdc++.h"]
    runtime.head+=["using namespace std;"]
    runtime.main+=["int main(int argc,char **argv,char **envp){"]
def _if(runtime,line):
    data=line[1]
    runtime.main+=["if("+data+"){"]
def makeString(runtime,line):
    #set the typedetector
    runtime.type_detector[line[1].split("=")[0]]="string"
    runtime.main+=["string "+line[1]+";"]
def _set(runtime,line):
    data=line[1]
    runtime.main+=[data+";"]
def inputto(runtime,line):
    to=line[1]
    return f"getline(cin,{to});"
bulitins=(
    {
        "end":"}",
        "else":"}else{"
    },
    {
        "output":output,
        "main":main,
        "if":_if,
        "string":makeString,
        "set":_set,
        "inputto":inputto
    }
)