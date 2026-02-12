# Inicio Rápido — OPN en 5 Minutos

Bienvenido a OPN. Esta guía te llevará desde cero hasta tu primer programa en minutos.

---

## 📦 Requisitos Previos

- **Python 3.7+** instalado en tu sistema
- **Editor de Texto** (VS Code, Sublime, etc.)
- El repositorio de OPN clonado o descargado

---

## 🚀 Paso 1: Tu Primer Programa

### Crear un archivo `hola.opn`

```opn
print("¡Hola, OPN!");
```

### Ejecutar en Linux/macOS

```bash
python opn2.py hola.opn
```

### Ejecutar en Windows

```bash
python opn2.py hola.opn
# o
.\opn.exe hola.opn
```

**Resultado:**
```
¡Hola, OPN!
```

✅ ¡Felicidades! Has ejecutado tu primer programa OPN.

---

## 💻 Paso 2: Trabajar con Variables

Crea un archivo `variables.opn`:

```opn
// Variables numéricas
var edad = 25;
var altura = 1.75;
var dinero = 100.50;

// Variables de texto
var nombre = "Carlos";
var ciudad = "Madrid";

// Mostrando los datos
print("Nombre: " + nombre);
print("Edad: " + edad);
print("Altura: " + altura + " metros");
print("Dinero disponible: " + dinero);
```

Ejecuta:
```bash
python opn2.py variables.opn
```

**Salida:**
```
Nombre: Carlos
Edad: 25
Altura: 1.75 metros
Dinero disponible: 100.5
```

---

## 🎯 Paso 3: Funciones Básicas

Crea `funciones.opn`:

```opn
// Función sin parámetros
function saludar() {
    print("¡Bienvenido a OPN!");
}

// Función con parámetros
function suma(a, b) {
    return a + b;
}

// Función con lógica
function es_par(numero) {
    if (numero % 2 == 0) {
        return "es par";
    } else {
        return "es impar";
    }
}

// Llamadas
saludar();
print(suma(10, 20));
print("El 7 " + es_par(7));
```

**Salida:**
```
¡Bienvenido a OPN!
30
El 7 es impar
```

---

## 🔄 Paso 4: Bucles e Iteración

Crea `bucles.opn`:

```opn
// Bucle for simple
print("Números del 1 al 5:");
for (var i = 1; i <= 5; i = i + 1) {
    print(i);
}

// Bucle while
print("\nConteo regresivo:");
var contador = 3;
while (contador > 0) {
    print(contador);
    contador = contador - 1;
}

// Suma de números
var suma = 0;
for (var i = 1; i <= 10; i = i + 1) {
    suma = suma + i;
}
print("\nSuma 1-10: " + suma);
```

**Salida:**
```
Números del 1 al 5:
1
2
3
4
5

Conteo regresivo:
3
2
1

Suma 1-10: 55
```

---

## 📚 Paso 5: Listas y Diccionarios

Crea `colecciones.opn`:

```opn
// Listas (arrays)
var numeros = [10, 20, 30, 40, 50];
print("Primer número: " + numeros[0]);
print("Último número: " + numeros[4]);

// Diccionarios (mapas)
var persona = {
    "nombre": "Ana",
    "edad": 28,
    "ciudad": "Barcelona"
};

print("Nombre: " + persona["nombre"]);
print("Edad: " + persona["edad"]);

// Iteración sobre listas
print("\nNúmeros en la lista:");
for (var i = 0; i < 5; i = i + 1) {
    print(numeros[i]);
}
```

---

## 🏛️ Paso 6: Clases y Objetos

Crea `clases.opn`:

```opn
// Definir una clase
class Coche {
    function init(marca, modelo) {
        this.marca = marca;
        this.modelo = modelo;
        this.velocidad = 0;
    }
    
    function acelerar() {
        this.velocidad = this.velocidad + 10;
    }
    
    function frenar() {
        if (this.velocidad > 0) {
            this.velocidad = this.velocidad - 10;
        }
    }
    
    function mostrar_estado() {
        print(this.marca + " " + this.modelo + " - Velocidad: " + this.velocidad + " km/h");
    }
}

// Usar la clase
var mi_coche = new Coche("Toyota", "Corolla");
mi_coche.mostrar_estado();

mi_coche.acelerar();
mi_coche.mostrar_estado();

mi_coche.acelerar();
mi_coche.mostrar_estado();
```

**Salida:**
```
Toyota Corolla - Velocidad: 0 km/h
Toyota Corolla - Velocidad: 10 km/h
Toyota Corolla - Velocidad: 20 km/h
```

---

## 🔨 Paso 7: Compilar a Python

Una vez que tu programa OPN funciona, puedes compilarlo a Python:

```bash
python opn2.py compile mi_programa.opn -o mi_programa.py
```

Esto genera un archivo Python que puedes:
- Distribuir independientemente
- Integrar con otras librerías Python
- Ejecutar directamente: `python mi_programa.py`

---

## 📊 Ejemplo Completo: Calculadora

Crea `calculadora.opn`:

```opn
// Calculadora simple
class Calculadora {
    function init() {
        this.resultado = 0;
    }
    
    function sumar(a, b) {
        this.resultado = a + b;
        return this.resultado;
    }
    
    function restar(a, b) {
        this.resultado = a - b;
        return this.resultado;
    }
    
    function multiplicar(a, b) {
        this.resultado = a * b;
        return this.resultado;
    }
    
    function dividir(a, b) {
        if (b == 0) {
            print("Error: No se puede dividir entre cero");
            return 0;
        }
        this.resultado = a / b;
        return this.resultado;
    }
}

// Uso
var calc = new Calculadora();

print("5 + 3 = " + calc.sumar(5, 3));
print("10 - 4 = " + calc.restar(10, 4));
print("6 * 7 = " + calc.multiplicar(6, 7));
print("20 / 4 = " + calc.dividir(20, 4));
```

---

## 🎓 Próximos Pasos

1. Lee [Sintaxis Completa](syntax.md) para todas las features
2. Explora [Rendimiento y Optimización](performance.md)
3. Usa [CLI y Compilación](compiler_cli.md) para herramientas avanzadas
4. Consulta [Prompt para IA](ia_formulario.md) si usas asistentes de IA

---

## ❓ Preguntas Frecuentes

**P: ¿Es OPN un lenguaje interpretado?**
R: OPN se transpila a Python, luego se interpreta. Tienes lo mejor de ambos: claridad de sintaxis + velocidad de Python.

**P: ¿Puedo usar librerías Python desde OPN?**
R: Sí, puedes importar módulos Python directamente en OPN.

**P: ¿Qué tan rápido es?**
R: OPN es tan rápido como Python, ya que al final se ejecuta sobre CPython.

**P: ¿Cómo reporto bugs?**
R: Abre un issue en el repositorio con detalles del problema.

---

**¡Ahora estás listo!** Comienza a escribir código OPN. 🚀
