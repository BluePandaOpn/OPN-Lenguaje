# CLI y Compilación OPN

 [Volver al README](../README.md)

Herramientas de línea de comandos para OPN.

---

##  Comandos Básicos

### Ejecutar un programa:
````ash
python opn2.py programa.opn
````

### Ejecutar con modo explícito:
````ash
python opn2.py run programa.opn --verbose
````

### Validar sintaxis:
````ash
python opn2.py check programa.opn
````

---

##  Compilación a Python

### Compilar a archivo:
````ash
python opn2.py compile programa.opn -o programa.py
python programa.py
````

### Ver código transpilado:
````ash
python opn2.py compile programa.opn --print
````

---

##  Análisis

### Ver estadísticas:
````ash
python opn2.py stats programa.opn
````

### Modo debug:
````ash
python opn2.py debug programa.opn
````

---

##  Opciones Avanzadas

- --optimize: Optimiza código transpilado
- --minify: Reduce tamaño del archivo
- --python 3.8: Especifica versión Python

---

##  Herramientas Interactivas

### REPL (intérprete interactivo):
````ash
python opn2.py repl
````

### Watch mode (desarrollo):
````ash
python opn2.py watch programa.opn
````

Monitorea cambios y ejecuta automáticamente.

---

##  Empaquetado

Después de compilar, crea ejecutable:
````ash
pip install pyinstaller
pyinstaller --onefile programa.py
````

---

##  Más Información

- [Sintaxis](syntax.md)
- [Inicio Rápido](quickstart.md)
- [Rendimiento](performance.md)

**¡Domina el CLI de OPN!** 
