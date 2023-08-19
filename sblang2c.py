import converter,sys,os,time,logging
logging.basicConfig(level=logging.DEBUG)
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
nocomp= args[1] == "nocompile"
name_executeable=".".join(filename.split(".")[:-1])
if len(args) < 2:
    print(f"usage: {name} [filename]")
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
try:
    for i in code.splitlines():
        runtime.translate(i)
except BaseException as e:
    print(f"\n! Error when converting: {e}")
    from traceback import print_exc
    print_exc()
    exit(1)
print(f" {timer.end()} ms")
print("- -| Writing to temp file",end="",flush=True)
timer.start()
with open("_sblang_temp.cpp","w+",encoding="utf-8") as f:
    f.write(runtime.export_final())
print(f" {timer.end()} ms")
if nocomp:
    print("-| Exiting.")
    exit(0)
print("-| Compiling with g++")
command=f"g++ _sblang_temp.cpp -finput-charset=UTF-8 -std=c++20 -o {name_executeable}"
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