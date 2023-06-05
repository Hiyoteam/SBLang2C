from uuid import uuid4

class CompileError(BaseException):
    pass
def _get_random_varname():
    return f"sblang_{str(uuid4()).replace('-','')}"
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
def loop(runtime,line):
    command=line[1].split(" ")
    if command[0] == "forever":
        return "while(1){"
    if len(command)==4 and (command[1] == "times" or command[1] == "time") and command[2] == "as":
        loopname=_get_random_varname()
        runtime.loops[command[3]]=loopname
        return f"for(int {loopname} = 0; {loopname} < {int(command[0])}; {loopname}++)"+"{"
    else:
        raise CompileError(f"Unknown loop statement: {command[0]}")
def loopindex(runtime,line):
    lid=line[1].split(" ")
    to=lid[1]
    lid=lid[0]
    if lid not in runtime.loops.keys():
        raise CompileError(f"LoopID doesnt exist")
    return f"int {to} = {runtime.loops[lid]};"
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
        "inputto":inputto,
        "loop":loop,
        "loopindex":loopindex
    }
)