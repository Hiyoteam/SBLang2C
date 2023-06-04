import converter,sys,os,time
class Timer:
    def __init__(self) -> None:
        self.stt=0
    def yee(self):
        self.stt=time.time()
    def woo(self):
        return round(1000*(time.time()-self.stt),5)
timer=Timer()
args=sys.argv
name=args[0]
filename=args[-1]
name_executeable=".".join(filename.split(".")[:-1])+".exe"
if len(args) < 2:
    print(f"usage: {name} [filename]")
    exit(1)
print("Welcome to SBLang2C CLI!\n-| Reading File",end="",flush=True)
timer.yee()
try:
    with open(filename,"r",encoding="utf-8") as f:
        code=f.read()
except:
    print("\n! Cannot read file, Aborting.")
    exit(1)
print(f" {timer.woo()} ms")
print("-| Converting to C++\n- -| Creating Runtime",end="",flush=True)
timer.yee()
runtime=converter.Runtime()
print(f" {timer.woo()} ms")
print("- -| Converting",end="",flush=True)
try:
    for i in code.splitlines():
        runtime.translate(i)
except BaseException as e:
    print(f"\n! Error when converting: {e}")
    exit(1)
print(f" {timer.woo()} ms")
print("- -| Writing to temp file",end="",flush=True)
timer.yee()
with open("_sblang_temp.cpp","w+",encoding="utf-8") as f:
    f.write(runtime.export_final())
print(f" {timer.woo()} ms")
print("-| Compiling with gcc")
command=f"g++ _sblang_temp.cpp -o {name_executeable}"
try:
    os.remove(name_executeable)
except:
    pass
gcc=os.popen(command)
print("- -| Awaiting GCC execute",end="",flush=True)
timer.yee()
times=0
gcc.read()
print(f" {timer.woo()} ms")
print("-| Removeing Tempfile")
os.remove("_sblang_temp.cpp")
print("-| Exiting Compile.")