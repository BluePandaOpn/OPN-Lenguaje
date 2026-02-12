# Referencia de Sintaxis OPN

 [Volver al README](../README.md)

Guía completa de todas las características del lenguaje OPN.

---

##  Comentarios

````opn
// Comentario de una línea

/*
  Comentario de múltiples líneas
*/
````

---

##  Variables y Tipos

````opn
var nombre = "OPN";           // String
var edad = 25;                  // Number
var activo = true;              // Boolean
var lista = [1, 2, 3];          // Array
var mapa = {"a": 1};          // Object
````

---

##  Operadores

**Aritméticos:** +, -, *, /, %
**Comparación:** ==, !=, >, <, >=, <=
**Lógicos:** &&, ||, !

---

##  Condicionales

````opn
if (edad < 18) {
    print("Menor");
} else if (edad < 65) {
    print("Adulto");
} else {
    print("Jubilado");
}
````

---

##  Bucles

````opn
for (var i = 0; i < 5; i = i + 1) {
    print(i);
}

var contador = 0;
while (contador < 5) {
    contador = contador + 1;
}
````

---

##  Funciones

````opn
function suma(a, b) {
    return a + b;
}

func multiplicar(a, b) {
    return a * b;
}
````

---

##  Clases

````opn
class Persona {
    function init(nombre) {
        this.nombre = nombre;
    }
    
    function saludar() {
        return "Hola, " + this.nombre;
    }
}

var p = new Persona("Ana");
print(p.saludar());
````

---

##  Arrays y Diccionarios

````opn
var lista = [1, 2, 3, 4];
var persona = {"nombre": "Ana", "edad": 28};

print(lista[0]);
print(persona["nombre"]);
````

---

##  Más Información

- [Inicio Rápido](quickstart.md)
- [Rendimiento](performance.md)
- [CLI](compiler_cli.md)

**para más ejemplos, consulta la documentación** 
