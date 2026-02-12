# CLI y Compilación — OPN

Guía completa sobre las herramientas de línea de comandos de OPN.

---

## 🛠️ Comandos Básicos

### Ejecutar un Programa

```bash
python opn2.py programa.opn
```

Interpreta y ejecuta el archivo `.opn` directamente.

**Ejemplo:**
```bash
python opn2.py hola.opn
```

**Salida:**
```
¡Hola, OPN!
```

---

### Ejecutar con Modo Explícito

```bash
python opn2.py run programa.opn
```

Equivalente a la forma anterior. Útil para claridad.

**Opciones:**
- `--verbose` o `-v`: Muestra detalles de transpilación
- `--debug`: Modo debug con información detallada

**Ejemplo:**
```bash
python opn2.py run programa.opn --verbose
```

---

## 🔨 Compilación a Python

### Compilar a Archivo Python

```bash
python opn2.py compile programa.opn -o programa.py
```

Transpila el código OPN a Python puro `.py`.

**Ejemplo:**
```bash
python opn2.py compile calculadora.opn -o calculadora.py
python calculadora.py
```

### Ver Código Transpilado

```bash
python opn2.py compile programa.opn --print
```

Muestra el código Python transpilado sin guardar archivo.

---

## 📊 Análisis y Validación

### Validar Sintaxis

```bash
python opn2.py check programa.opn
```

Valida la sintaxis sin ejecutar el programa.

**Salida si hay errores:**
```
Error en línea 5, columna 12:
    var x = ;
            ^
Esperado expresión después de '='
```

### Ver Estadísticas del Código

```bash
python opn2.py stats programa.opn
```

Muestra información sobre el código:
- Líneas totales
- Funciones definidas
- Clases definidas
- Variables globales
- Tamaño transpilado

**Ejemplo de salida:**
```
=== Estadísticas de programa.opn ===
Líneas:              45
Funciones:           5
Clases:              2
Variables globales:  8
Tamaño transpilado:  1250 bytes
Tiempo transpilación: 2ms
```

---

## ⚙️ Opciones Avanzadas

### Especificar Versión de Python Target

```bash
python opn2.py compile programa.opn -o programa.py --python 3.8
```

Genera código compatible con Python 3.8+.

**Versiones soportadas:** 3.7+

### Optimizar Código Transpilado

```bash
python opn2.py compile programa.opn -o programa.py --optimize
```

Aplica optimizaciones adicionales al código Python.

**Optimizaciones incluidas:**
- Eliminación de código muerto
- Simplificación de expresiones constantes
- Inlining de funciones pequeñas

### Minificar Salida

```bash
python opn2.py compile programa.opn -o programa.py --minify
```

Reduce el tamaño del archivo eliminando espacios y renombrando variables.

---

## 📦 Empaquetado y Distribución

### Crear Ejecutable Vía PyInstaller

Después de compilar a Python:

```bash
# 1. Compilar
python opn2.py compile programa.opn -o programa.py

# 2. Instalar pyinstaller
pip install pyinstaller

# 3. Crear ejecutable
pyinstaller --onefile programa.py
```

El ejecutable estará en `dist/programa.exe` (Windows) o `dist/programa` (Linux/Mac).

### Incluir Dependencias Python

Si tu código OPN usa librerías:

```bash
# En una carpeta limpia
pip install -r requirements.txt
pyinstaller --onefile programa.py
```

---

## 🚀 Herramientas Interactivas

### REPL (Intérprete Interactivo)

```bash
python opn2.py repl
```

Inicia un shell interactivo donde puedes escribir código OPN línea por línea.

**Ejemplo:**
```
OPN REPL v1.0
> var x = 10;
> var y = 20;
> print(x + y);
30
> function suma(a, b) { return a + b; }
> suma(5, 3);
8
>
```

**Comandos especiales:**
- `.help` - Muestra ayuda
- `.clear` - Limpia variables
- `.exit` - Sale del REPL

### Modo Watch (Desarrollo)

```bash
python opn2.py watch programa.opn
```

Monitorea cambios en el archivo y ejecuta automáticamente.

**Ejemplo:**
```bash
python opn2.py watch mi_programa.opn
Esperando cambios en mi_programa.opn...
[2024-01-15 10:30:45] Cambios detectados, ejecutando...
Cambios detectados automáticamente, ejecutando...
```

Útil durante desarrollo para iteración rápida.

---

## 📝 Configuración del Compilador

### Archivo de Configuración `.opnrc`

Crea un archivo `.opnrc` en el directorio del proyecto:

```json
{
  "python_version": "3.8",
  "optimize": true,
  "cache_size": 256,
  "timeout": 30,
  "strict_mode": false
}
```

**Opciones:**
- `python_version`: Versión mínima de Python
- `optimize`: Optimizar código generado
- `cache_size`: Tamaño del cache LRU
- `timeout`: Timeout de ejecución en segundos
- `strict_mode`: Realizar análisis estricto

### Usar Configuración

```bash
python opn2.py compile programa.opn --config .opnrc -o programa.py
```

---

## 🔍 Debugging

### Modo Debug

```bash
python opn2.py debug programa.opn
```

Ejecuta con información de debugging detallada.

**Salida:**
```
[DEBUG] Leyendo archivo: programa.opn
[DEBUG] Parseando tokens...
[DEBUG] Construyendo AST...
[DEBUG] Transpilando...
[DEBUG] Ejecutando...
Resultados...
```

### Ver AST (Abstract Syntax Tree)

```bash
python opn2.py debug programa.opn --ast
```

Muestra el árbol de sintaxis abstracta.

### Trace de Ejecución

```bash
python opn2.py debug programa.opn --trace
```

Rastrea cada paso de la ejecución.

---

## 🧪 Testing

### Framework de Testing (Planificado)

OPN incluirá pronto:

```opn
// test_calculadora.opn
test "suma 2 + 2" {
    assert suma(2, 2) == 4;
}

test "multiplicación 3 * 4" {
    assert multiplicar(3, 4) == 12;
}
```

Ejecuta con:
```bash
python opn2.py test test_calculadora.opn
```

---

## 📊 Benchmarking

### Medir Rendimiento

```bash
python opn2.py benchmark programa.opn --iterations 1000
```

Ejecuta el programa 1000 veces y reporta estadísticas.

**Salida:**
```
=== Benchmark: programa.opn ===
Iteraciones:     1000
Tiempo total:    2500ms
Promedio:        2.5ms
Min:             2.1ms
Max:             3.8ms
Estadística:     Stdev: 0.65ms
```

### Comparar Rendimiento

```bash
python opn2.py benchmark programa.opn programa_optimizado.opn
```

Compara el rendimiento de dos programas lado a lado.

---

## 🆘 Mensajes de Error

### Error de Sintaxis

```
Error en línea 3, columna 7:
    for (i = 0; i < 5; i++) {
          ^
Esperado declaración de variable. Usa 'var' antes de la variable.
Sugerencia: for (var i = 0; i < 5; i = i + 1) {
```

### Error de Runtime

```
Runtime Error:
    Division por cero en línea 8
    var resultado = 10 / 0;
                       ^
Sugerencia: Valida que el divisor no sea cero.
```

### Error de Tipo (modo strict)

```
Type Error:
    No puedes asignar string a variable numérica
    En línea 12: var edad = "25";
```

---

## 📚 Ejemplos de Workflow

### Desarrollo Rápido

```bash
# 1. Usar watch mode
python opn2.py watch programa.opn

# 2. Editar el archivo en otro terminal
# 3. Los cambios se ejecutan automáticamente
```

### Distribución

```bash
# 1. Desarrollar y probar
python opn2.py programa.opn

# 2. Compilar a Python
python opn2.py compile programa.opn -o programa.py

# 3. Crear ejecutable
pyinstaller --onefile programa.py

# 4. Distribuir el ejecutable
# Los usuarios ejecutan sin Python ni OPN
```

### Integración Continua (CI)

```bash
# En tu CI/CD pipeline:
python opn2.py check programa.opn  # Validar sintaxis
python opn2.py test test_programa.opn  # Ejecutar tests
python opn2.py compile programa.opn -o dist/programa.py  # Compilar
```

---

## 🔧 Solución de Problemas

### "Command not found: opn2.py"

Asegúrate de:
1. Está en el PATH correcto
2. Python está instalado
3. Usa `python opn2.py` en lugar de solo `opn2.py`

### "Memory error" durante compilación

Para archivos muy grandes:
```bash
python opn2.py compile grande.opn --chunk-size 10000 -o salida.py
```

### Código transpilado muy grande

Usa minificación:
```bash
python opn2.py compile programa.opn -o programa.py --minify
```

---

## 💡 Tips y Trucos

1. **Guarda siempre código compilado:** Puedes distribuirlo sin OPN
2. **Usa --verbose durante debug:** Ver qué hace el compilador
3. **REPL para prototipar:** Prueba código rápidamente
4. **watch para desarrollo:** Iteración rápida automática
5. **Benchmark antes de optimizar:** Mide, no adivines

---

**¡Domina el CLI de OPN!** 🚀
