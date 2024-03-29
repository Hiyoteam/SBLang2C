from uuid import uuid4
from logging import debug
from os import path,getcwd

class Function:
    def __init__(self):
        self.lines=[]
    def export(self):
        return "\n".join(self.lines)
class CompileError(BaseException):
    pass
def _get_random_varname():
    return f"sblang_{str(uuid4()).replace('-','')}"
def output(runtime,line):
    return f"cout << {line[1]};\n"
def main(runtime,line):
    runtime.head+=["using namespace std;"]
    runtime.main+=["int main(int argc,char **argv,char **envp){"]
def _if(runtime,line):
    data=line[1]
    runtime.main+=["if("+data+"){"]
def _set(runtime,line):
    data=line[1]
    runtime.main+=[data+";"]
def inputto(runtime,line):
    tos=line[1].split(' ')
    reslt=f"cin "
    for i in tos:
        reslt+=f">> {i}"
    return reslt+";"
def loop(runtime,line):
    command=line[1].split(" ")
    if command[0] == "forever":
        return "while(1){"
    if len(command)==4 and (command[1] == "times" or command[1] == "time") and command[2] == "as":
        loopname=command[3]
        return f"for(int {loopname} = 0; {loopname} < {int(command[0])}; {loopname}++)"+"{"
    else:
        raise CompileError(f"Unknown loop statement: {command[0]}")
def define(runtime,line):
    if runtime.cache.get("DEFINEING") == True:
        raise CompileError(f"Cannot compile function in function.")
    #LOCK
    runtime.cache["DEFINEING"]=True
    #Generate info
    info={"name":line[1].split(" ")[0],"args":[],"lines":[]}
    debug("Function Info:",info)
    #Generate global checker
    def checker(runtime,line):
        line.replace("  ","  ")
        line=line.lstrip(" ")
        if line.startswith("#"):
            return False
        if not line:
            return False
        debug(f"Running Checker:{line}")
        if line == "define end":
            runtime.cache["DEFINEING"] = False
            #load data
            data=runtime.cache["DEFINE_DATA"]
            del runtime.cache["DEFINE_DATA"]
            #export final
            program=f"auto {data['name']}({','.join(data['args'])})"
            program+="{\n"
            program+="\n".join(data["lines"])
            program+="}"
            runtime.functions.append(program)
            runtime.global_checker.remove(checker)
            debug(f"Generated Program:{program}")
            return True
        debug(runtime.cache)
        runtime.cache["DEFINE_DATA"]["lines"].append(runtime.translate(line,False,True))
        #ok lets add
        debug(f"Added: {runtime.cache['DEFINE_DATA']}")
        return True
    # parse args
    args=line[1].split(" ")[1:]
    for arg in args:
        info["args"].append(f"auto {arg}")
    #FUCK YOU START!!!
    runtime.global_checker.append(checker)
    runtime.cache["DEFINE_DATA"]=info
def returns(runtime,line):
    return f"return {line[1]};"
def var(runtime,line):
    line = line[1].split("=")
    if len(line) == 1:
        return f"auto {line[0]};"
    else:
        return f"auto {line[0]} = {'='.join(line[1:])};"
def let(runtime,line):
    typeof=" ".join(line[1].split(" ")[:-1])
    name=line[1].split(" ")[-1]
    return f"{typeof} {name};"
def fromimport(runtime,line):
    runtime.externs.add(line[1])
def export(runtime,line):
    line=line[1].split(" ")
    return "extern \"C\" {"+f"{line[0]} {line[1]}"+";}"
def callfunc(runtime,line):
    cmdname=line[1].split(" ")
    args=" ".join(cmdname[1:]).split(",")
    cmdname=cmdname[0]
    reslt=cmdname+"("+",".join(args)+");"
    return reslt
def switch(runtime,line):
    return f"switch({line[1]})"+"{"
def case(runtime,line):
    if line[1] != "default":
        return f"case {line[1]}:"
    else:
        return f"default:"
def use(runtime,line):
    # Use SBLang2C builtin methods
    for i in line[1].split(","):
        if path.exists(f"{getcwd()}/sblang_builtin_funcs/{i}.h"):
            runtime.heads.add(f"{getcwd()}/sblang_builtin_funcs/{i}.h")
        else:
            raise CompileError(f"SBlang2C Builtin method not found: {i}")
        if i in ["requests"]:
            runtime.options["USE_LIBCURL"]=True
def string(runtime,line):
    res=f"string {line[1].split('=')[0]}"
    if len(line[1].split('=')) > 1:
        res+='='+line[1].split('=',1)[1]
    return res+";"
def exitprog(runtime,line):
    return f"exit({line[1]});"
def elseif(runtime,line):
    return "}else if("+line[1]+"){"

bulitins=(
    {
        "end":"}",
        "else":"}else{",
        "break":"break;"
    },
    {
        "output":output,
        "main":main,
        "if":_if,
        "set":_set,
        "inputto":inputto,
        "loop":loop,
        "var":var,
        "let":let,
        "define":define,
        "return":returns,
        "import":fromimport,
        "export":export,
        "call":callfunc,
        "switch":switch,
        "case":case,
        "use":use,
        "string":string,
        "exit":exitprog,
        "elif":elseif
    }
)
COMMENT="""
/*
    Generated By SBLang2C.
*/
"""
class CompileError(BaseException):
    pass
class NameSpace:
    def __init__(self,static:dict,dynamic:dict):
        self.static,self.dynamic=static,dynamic
        self.names=list(static.keys())+list(dynamic.keys())

    def _topure(self,line:str):
        line.replace("  ","  ")
        line=line.lstrip(" ")
        if line.startswith("#"):
            return False
        if not line:
            return False
        return line
    def translate(self,runtime,line):
        line=self._topure(line)
        if not line:
            return False
        command=line.split(" ")[0]
        if command not in self.names:
            return 1
        #go ahead!
        if command in self.static.keys():
            cmdtype=0 #STATIC
        else:
            cmdtype=1 #DYNAMIC
        if cmdtype:
            debug(f"Running Dynamic Command: {command}")
            return self.dynamic[command](runtime,line.split(" ",1))
        else:
            return self.static[command]

bulitins=NameSpace(
    bulitins[0],
    bulitins[1]
)
class Runtime:
    def __init__(self):
        self.heads,self.head,self.externs,self.functions,self.main,self.global_checker,self.cache=set(),[],set(),[],[],[],{}
        self.options={
            "USE_LIBCURL":False
        }
        self.type_detector={}
        self.loops={}
    def translate(self,line,run_checkers=True,return_code=False):
        if run_checkers:
            for checker in self.global_checker:
                data=checker(self,line)
                if data == None:
                    #keep going
                    pass
                else:
                    #stop!
                    debug(f"Stopped by Global-Checker")
                    return True
        translated=bulitins.translate(self,line)
        if translated == False:
            return True
        if translated == 1:
            raise CompileError(f"Command Not Found: in line: {line}")
        if translated == None:
            return True
        if not return_code:
            self.main+=[translated]
        return translated
    def export_final(self):
        final=COMMENT+"\n"
        debug("Exporting....")
        debug(f"Headers: {self.heads}")
        final+=f"#include <bits/stdc++.h>\n"
        for i in self.heads:
            final+=f"#include <{i}>\n"
        final+="\n\n".join(self.head+self.functions+self.main)
        self.externs=list(self.externs)
        return final

    
