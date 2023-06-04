import converter
program="""
main
output "Hello,World!\\n\\n"
end
"""
runtime=converter.Runtime()
for i in program.splitlines():
    runtime.translate(i)
print(runtime.export_final())