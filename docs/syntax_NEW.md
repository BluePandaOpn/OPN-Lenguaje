# Referencia Completa de Sintaxis OPN

Guía exhaustiva de todas las características y construcciones del lenguaje OPN.

---

## 📝 Comentarios

```opn
// Comentario de una línea

/*
  Comentario de múltiples líneas
  puede ocupar varios renglones
*/
```

---

## 🔤 Variables y Tipos

### Declaración de Variables

```opn
var nombre = "OPN";
var edad = 25;
var precio = 19.99;
var activo = true;
var lista = [1, 2, 3];
var mapa = {"clave": "valor"};
```

### Tipos de Datos

| Tipo | Ejemplo | Descripción |
|------|---------|-------------|
| **String** | `"texto"` | Cadenas de caracteres |
| **Number** | `42`, `3.14` | Números enteros y decimales |
| **Boolean** | `true`, `false` | Valores booleanos |
| **Array** | `[1, 2, 3]` | Listas ordenadas |
| **Object** | `{"a": 1}` | Mapas de clave-valor |
| **null** | `null` | Valor nulo |

### Asignación y Operadores

```opn
var x = 10;
x = x + 5;              // 15
x = x - 3;              // 12
x = x * 2;              // 24
x = x / 4;              // 6
x = x % 3;              // 0 (módulo)

// Asignación compuesta
var contador = 0;
contador = contador + 1;
```

---

## 🧮 Operadores

### Aritméticos

```opn
var a = 10;
var b = 3;

print(a + b);   // 13 (suma)
print(a - b);   // 7  (resta)
print(a * b);   // 30 (multiplicación)
print(a / b);   // 3  (división)
print(a % b);   // 1  (módulo)
```

### Comparación

```opn
var x = 5;

x == 5;         // true (igual)
x != 5;         // false (no igual)
x > 3;          // true (mayor que)
x < 10;         // true (menor que)
x >= 5;         // true (mayor o igual)
x <= 5;         // true (menor o igual)
```

### Lógicos

```opn
var a = true;
var b = false;

a && b;         // false (AND)
a || b;         // true (OR)
!a;             // false (NOT)
```

### Concatenación de Strings

```opn
var nombre = "OPN";
var version = 1.0;

var mensaje = nombre + " versión " + version;
print(mensaje); // "OPN versión 1.0"
```

---

## 🎯 Condicionales

### If / Else

```opn
var edad = 25;

if (edad < 18) {
    print("Eres menor de edad");
} else if (edad >= 18 && edad < 65) {
    print("Eres adulto");
} else {
    print("Eres jubilado");
}
```

### If Anidado

```opn
var numero = 15;

if (numero > 0) {
    if (numero > 10) {
        print("Mayor a 10");
    } else {
        print("Entre 1 y 10");
    }
} else {
    print("No positivo");
}
```

---

## 🔄 Bucles

### Bucle For

```opn
// Bucle simple
for (var i = 0; i < 5; i = i + 1) {
    print(i);
}

// Bucle con paso diferente
for (var i = 0; i < 10; i = i + 2) {
    print(i);  // 0, 2, 4, 6, 8
}

// Bucle regresivo
for (var i = 5; i > 0; i = i - 1) {
    print(i);  // 5, 4, 3, 2, 1
}
```

### Bucle While

```opn
var contador = 0;
while (contador < 5) {
    print(contador);
    contador = contador + 1;
}

// Break y continue
var num = 0;
while (true) {
    if (num == 5) {
        break;     // Sale del bucle
    }
    if (num == 2) {
        num = num + 1;
        continue;  // Salta a siguiente iteración
    }
    print(num);
    num = num + 1;
}
```

### Bucle Do-While

```opn
var contador = 0;
do {
    print(contador);
    contador = contador + 1;
} while (contador < 3);
```

---

## 📦 Funciones

### Declaración Básica

```opn
function saludar() {
    print("¡Hola!");
}

saludar();
```

### Con Parámetros

```opn
function suma(a, b) {
    return a + b;
}

var resultado = suma(5, 3);
print(resultado);  // 8
```

### Con Múltiples Parámetros

```opn
function crear_perfil(nombre, edad, ciudad) {
    return nombre + " - " + edad + " años - " + ciudad;
}

print(crear_perfil("Carlos", 30, "Madrid"));
```

### Alias `func`

```opn
func multiplicar(a, b) {
    return a * b;
}

print(multiplicar(4, 5));  // 20
```

### Scope y Variables Locales

```opn
var global = "Soy global";

function demostrar() {
    var local = "Soy local";
    print(local);   // Funciona
    print(global);  // Accede a global
}

demostrar();
// print(local);  // Error: local no existe fuera de la función
```

---

## 🏛️ Clases y Objetos

### Definición Básica

```opn
class Persona {
    function init(nombre) {
        this.nombre = nombre;
    }
    
    function saludar() {
        print("Hola, soy " + this.nombre);
    }
}

var persona = new Persona("Ana");
persona.saludar();  // Hola, soy Ana
```

### Constructor `init`

```opn
class Coche {
    function init(marca, modelo, ano) {
        this.marca = marca;
        this.modelo = modelo;
        this.ano = ano;
        this.velocidad = 0;
    }
    
    function acelerar() {
        this.velocidad = this.velocidad + 10;
    }
    
    function info() {
        print(this.ano + " " + this.marca + " " + this.modelo);
    }
}

var auto = new Coche("Toyota", "Corolla", 2023);
auto.acelerar();
auto.info();  // 2023 Toyota Corolla
```

### Propiedades y Métodos

```opn
class Estudiante {
    function init(nombre, carrera) {
        this.nombre = nombre;
        this.carrera = carrera;
        this.calificacion = 0;
    }
    
    function estudiar(horas) {
        this.calificacion = this.calificacion + (horas * 10);
    }
    
    function resultado() {
        if (this.calificacion >= 70) {
            return "Aprobado";
        } else {
            return "Reprobado";
        }
    }
}

var est = new Estudiante("Carlos", "Informática");
est.estudiar(5);
print(est.resultado());  // Aprobado
```

---

## 📚 Arreglos (Arrays/Listas)

### Creación y Acceso

```opn
var numeros = [10, 20, 30, 40, 50];

print(numeros[0]);   // 10 (primer elemento)
print(numeros[2]);   // 30 (tercero)
print(numeros[4]);   // 50 (último)
```

### Modificación

```opn
var lista = [1, 2, 3];
lista[0] = 10;       // Cambiar primer elemento
lista[1] = 20;
print(lista);        // [10, 20, 3]
```

### Bucles sobre Arrays

```opn
var frutas = ["manzana", "plátano", "naranja"];

for (var i = 0; i < 3; i = i + 1) {
    print(frutas[i]);
}
```

### Métodos Útiles (cuando se compilan a Python)

```opn
var lista = [1, 2, 3, 4, 5];
// Al compilar, puedes usar métodos de Python:
var len = lista.length;  // Acceso a propiedades
```

---

## 🗝️ Diccionarios (Objetos/Mapas)

### Creación y Acceso

```opn
var persona = {
    "nombre": "Ana",
    "edad": 28,
    "ciudad": "Barcelona"
};

print(persona["nombre"]);  // Ana
print(persona["edad"]);    // 28
```

### Modificación

```opn
var config = {
    "tema": "oscuro",
    "idioma": "es"
};

config["tema"] = "claro";
config["nuevo_valor"] = 100;

print(config["tema"]);        // claro
print(config["nuevo_valor"]); // 100
```

### Diccionarios Anidados

```opn
var empresa = {
    "nombre": "TechCorp",
    "ubicacion": {
        "ciudad": "Madrid",
        "pais": "España"
    },
    "empleados": 50
};

print(empresa["ubicacion"]["ciudad"]);  // Madrid
```

---

## 🔥 Características Avanzadas

### Try-Catch (Manejo de Errores)

```opn
try {
    var resultado = 10 / 0;
    print(resultado);
} catch (error) {
    print("Error capturado: " + error);
}
```

### Return y Control de Flujo

```opn
function buscar(lista, objetivo) {
    for (var i = 0; i < 5; i = i + 1) {
        if (lista[i] == objetivo) {
            return i;      // Retorna el índice
        }
    }
    return -1;            // No encontrado
}

print(buscar([10, 20, 30], 20));  // 1
```

### Funciones Recursivas

```opn
function factorial(n) {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

print(factorial(5));  // 120
```

---

## 📌 Mejores Prácticas

1. **Nombres Descriptivos**: Usa nombres claros para variables y funciones
   ```opn
   var contador = 0;     // ✓ Bueno
   var c = 0;            // ✗ Confuso
   ```

2. **Comentarios**: Documenta código complejo
   ```opn
   // Calcula la suma de números del 1 al n
   var suma = 0;
   for (var i = 1; i <= 10; i = i + 1) {
       suma = suma + i;
   }
   ```

3. **Funciones Pequeñas**: Una responsabilidad por función
   ```opn
   function validar_email(email) {
       return email.contains("@");
   }
   ```

4. **Evita Duplicación**: Extrae código repetido en funciones
   ```opn
   // Malo: código duplicado
   print("Procesando: " + datos1);
   print("Procesando: " + datos2);
   
   // Mejor: extraer en función
   function procesar(datos) {
       print("Procesando: " + datos);
   }
   ```

---

## 📖 Referencia Rápida de Sintaxis

| Construcción | Sintaxis |
|---|---|
| Variable | `var nombre = valor;` |
| Comentario | `// línea` o `/* bloque */` |
| If/Else | `if (condición) { } else { }` |
| For Loop | `for (var i = 0; i < n; i = i + 1) { }` |
| While Loop | `while (condición) { }` |
| Función | `function nombre(param) { return valor; }` |
| Clase | `class Nombre { function init() { } }` |
| Array | `var arr = [1, 2, 3];` |
| Objeto | `var obj = {"clave": valor};` |
| Return | `return valor;` |
| Print | `print(expresión);` |

---

**¡Ahora dominas la sintaxis de OPN!** 🎉
