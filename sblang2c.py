import converter,sys,os,time,logging
class Timer:
    def __init__(self) -> None:
        self.stt=0
    def start(self):
        self.stt=time.time()
    def end(self):
        return round(1000*(time.time()-self.stt),5)
timer=Timer()
args=sys.argv
name=args[0]
filename=args[-1]
argss= args[1:-1]
nocomp="--no-compile" in argss
debug="--debug" in argss
gcc_executable="g++"
gcc_extra_args=[]
name_executeable=".".join(filename.split(".")[:-1])
for arg in argss:
    arg=arg.split("=",1)
    if len(arg) == 1:
        continue
    if arg[0] == "--gcc-binary":
        gcc_executable=arg[1]
    if arg[0] == "--gcc-arg":
        gcc_extra_args.append("-"+arg[1])
    if arg[0] == "--output":
        name_executeable=arg[1]

if debug:
    logging.basicConfig(level=logging.DEBUG)
if len(args) < 2:
    print(f"usage: {name} [options] [filename]")
    exit(1)
print("Welcome to SBLang2C CLI!\n-| Reading File",end="",flush=True)
timer.start()
try:
    with open(filename,"r",encoding="utf-8") as f:
        code=f.read()
except:
    print("\n! Cannot read file, Aborting.")
    exit(1)
print(f" {timer.end()} ms")
print("-| Converting to C++\n- -| Creating Runtime",end="",flush=True)
timer.start()
runtime=converter.Runtime()
print(f" {timer.end()} ms")
print("- -| Converting",end="",flush=True)
if debug:
    print()
try:
    for i in code.splitlines():
        runtime.translate(i)
except BaseException as e:
    print(f"\n! Error when converting: {e}")
    from traceback import print_exc
    print_exc()
    exit(1)
if debug:
    print()
print(f" {timer.end()} ms")
print("- -| Writing to temp file",end="",flush=True)
timer.start()
if debug:
    print()
with open("_sblang_temp.cpp","w+",encoding="utf-8") as f:
    f.write(runtime.export_final())
if debug:
    print()
print(f" {timer.end()} ms")
if nocomp:
    print("-| Exiting.")
    exit(0)
print("-| Compiling with g++")
command=f"{gcc_executable} _sblang_temp.cpp -finput-charset=UTF-8 -std=c++20 -o {name_executeable}"
if gcc_extra_args != []:
    for i in gcc_extra_args:
        command+=" "+i
try:
    os.remove(name_executeable)
except:
    pass
gcc=os.popen(command)
print("- -| Awaiting G++ execute",end="",flush=True)
timer.start()
times=0
gcc.read()
print(f" {timer.end()} ms")
print("-| Removeing Tempfile")
os.remove("_sblang_temp.cpp")
print("-| Exiting Compile.")