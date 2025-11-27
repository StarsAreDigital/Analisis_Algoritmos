def buscar(patron: str, texto: str):
    m = len(patron)
    n = len(texto)
    i = 0
    while i <= n - m:
        j = 0
        while j < m:
            if texto[i + j] != patron[j]:
                break
            j = j + 1
        if j == m:
            yield i
        i = i + 1


patron = "AABA"
texto = "AABAACAADAABAABA"
#        ^^^^
found = False
for i in buscar(patron, texto):
    found = True
    j = i + len(patron)
    print("%s\033[91m%s\033[00m%s" % (texto[:i], texto[i:j], texto[j:]))
if not found:
    print("No se encontró el texto")