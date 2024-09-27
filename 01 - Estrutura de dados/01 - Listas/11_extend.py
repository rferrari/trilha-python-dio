linguagens = ["python", "js", "c"]
linguagens2 = ["php", "go", ".net"]

print(linguagens)  # ["python", "js", "c"]

linguagens.extend(["java", "csharp"])
linguagens.extend(linguagens2)

print(linguagens)  # ["python", "js", "c", "java", "csharp"]

