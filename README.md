# OPN — Lenguaje Simple, Poderoso, Intuitivo

**OPN** es un lenguaje de programación moderno diseñado para aprender, prototipar y construir herramientas eficientes que se transpilan a Python. Combina la claridad de lenguajes como JavaScript y C con la potencia del ecosistema Python.

---

## 🎯 ¿Por Qué OPN?

OPN fue creado con una filosofía simple: **programación sin fricción**. Ideal para:

- **Aprendices**: Sintaxis clara, coherente y amigable
- **Prototipos**: Iteración rápida sin compilación pesada
- **Profesionales**: Acceso directo al ecosistema Python mediante transpilación

---

## ✨ Características Principales

| Característica | Descripción |
|---|---|
| **Sintaxis Clara** | Inspirada en C y JavaScript, fácil de leer y escribir |
| **Sin Instalación** | Ejecuta directamente archivos `.opn` con Python |
| **Transpilación Inteligente** | Compila a código Python legible y optimizado |
| **Errores Útiles** | Reporta errores con línea, columna y sugerencias |
| **Cache de Compilación** | LRU cache para reutilización eficiente de código |
| **Interoperabilidad** | Integración seamless con librerías Python existentes |

---

## 🚀 Instalación y Uso Rápido

### Sistema Operativo: Linux/macOS

```bash
# Ejecutar un archivo OPN
python opn2.py programa.opn

# Ejecutar con comando explícito
python opn2.py run programa.opn

# Compilar a Python
python opn2.py compile programa.opn -o programa.py
```

### Sistema Operativo: Windows

```bash
# Usando el ejecutable compilado
.\opn.exe programa.opn
.\opn.exe run programa.opn
.\opn.exe compile programa.opn -o programa.py
```

---

## 📚 Documentación Completa

### Guías Principales
- **[Inicio Rápido](docs/quickstart.md)** — Primeros pasos en 5 minutos
- **[Sintaxis del Lenguaje](docs/syntax.md)** — Referencias completas de features
- **[CLI y Compilación](docs/compiler_cli.md)** — Herramientas de línea de comandos
- **[Optimización y Rendimiento](docs/performance.md)** — Mejores prácticas y benchmarks
- **[Prompt para IA](docs/ia_formulario.md)** — Instrucciones para modelos de IA

### Portales Web
- **[Documentación Web](docs/html/index.html)** — Portal interactivo completo
- **[Guía Interactiva](docs/html/quickstart.html)** — Tutorial paso a paso

---

## 💡 Primer Programa

```opn
// Variables simples
var nombre = "OPN";
var version = 1.0;

// Función básica
function saludar(persona) {
    return "Hola, " + persona + "!";
}

// Uso
print(saludar(nombre));
print("Versión: " + version);
```

**Salida:**
```
Hola, OPN!
Versión: 1.0
```

---

## 🏗️ Conceptos Clave

### 1. Variables y Tipos

```opn
var numero = 42;
var texto = "OPN";
var lista = [1, 2, 3, 4, 5];
var diccionario = {"clave": "valor", "edad": 25};
```

### 2. Control de Flujo

```opn
if (numero > 10) {
    print("Mayor a 10");
} else if (numero == 10) {
    print("Igual a 10");
} else {
    print("Menor a 10");
}
```

### 3. Funciones y Clases

```opn
class Persona {
    function init(nombre, edad) {
        this.nombre = nombre;
        this.edad = edad;
    }
    
    function saludar() {
        return "Hola, soy " + this.nombre;
    }
}

var persona = new Persona("Carlos", 30);
print(persona.saludar());
```

### 4. Iteración

```opn
// Bucle for
for (var i = 0; i < 5; i = i + 1) {
    print(i);
}

// Bucle while
var contador = 0;
while (contador < 3) {
    print(contador);
    contador = contador + 1;
}
```

---

## ⚡ Optimización y Rendimiento

OPN incluye varias optimizaciones para maximizar velocidad:

- **Cache LRU de Transpilación**: Reutiliza compilaciones previas
- **Instancia de Intérprete Reutilizable**: Una sola instancia para múltiples ejecuciones
- **Python Nativo**: Acceso directo al rendimiento de CPython

### Benchmark Simple
```opn
// Suma de números 1-1000
var total = 0;
for (var i = 1; i <= 1000; i = i + 1) {
    total = total + i;
}
print(total); // 500500
```

---

## 🔗 Ecosistema e Integración

### Uso con Librerías Python

OPN puede importar y usar librerías Python directamente:

```opn
// Acceso a módulos Python
var os = import("os");
var json = import("json");
var math = import("math");

// Uso
print(math.sqrt(16)); // 4.0
```

---

## 📋 Estructura del Proyecto

```
OpnScript/
├── README.md                    # Este archivo
├── src/
│   ├── opn_compiler.py         # Compilador principal
│   ├── opn.py                  # Intérprete
│   └── opn2.py                 # Versión mejorada
├── docs/
│   ├── quickstart.md           # Guía de inicio
│   ├── syntax.md               # Referencias de sintaxis
│   ├── compiler_cli.md         # Documentación CLI
│   ├── performance.md          # Guía de rendimiento
│   ├── ia_formulario.md        # Prompt para IA
│   └── html/                   # Portal web
│       ├── index.html
│       ├── quickstart.html
│       ├── syntax.html
│       ├── performance.html
│       ├── ia-form.html
│       └── styles.css
└── README.md
```

---

## 🤝 Contribuciones y Soporte

OPN es un proyecto en desarrollo activo. Las contribuciones son bienvenidas en áreas como:

- **Mejoras de Sintaxis**: Propuestas para features nuevas
- **Optimizaciones**: Mejoras de rendimiento
- **Documentación**: Ampliación de guías y ejemplos
- **Herramientas**: IDE plugins, linters, formatters

---

## 📄 Licencia

OPN está disponible bajo licencia MIT. Consulta el archivo LICENSE para más detalles.

---

## 🎓 ¿Dónde Empezar?

1. **Principiantes**: Dirígete a [Inicio Rápido](docs/quickstart.md)
2. **Explorar Sintaxis**: Lee [Sintaxis del Lenguaje](docs/syntax.md)
3. **Casos Avanzados**: Consulta [Rendimiento y Optimización](docs/performance.md)
4. **Entrenar a una IA**: Usa [Prompt para IA](docs/ia_formulario.md)

---

**OPN** — *Programación simple y poderosa*
