from src.codegen.file_writer import (
    FileWriter
)

path = (
    FileWriter.write(
        "generated",
        "hello.txt",
        "compiler works"
    )
)

print(path)