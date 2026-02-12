# Optimización y Rendimiento OPN

 [Volver al README](../README.md)

Guía sobre optimización y mejor rendimiento en OPN.

---

##  Optimizaciones Integradas

- **Cache LRU** de transpilación automático
- **Reutilización de intérprete** para múltiples ejecuciones
- **Python nativo** (CPython performance)

---

##  Mejores Prácticas

###  DO: Cachea valores
````opn
var len = lista.length;
for (var i = 0; i < len; i = i + 1) {
    // usar len, no lista.length
}
````

###  DON'T: Operaciones en bucles
````opn
for (var i = 0; i < lista.length; i = i + 1) {
    // Evita calcular lista.length en cada iteración
}
````

###  DO: Usa diccionarios para búsquedas
Acceso O(1) en lugar de O(n)

###  DON'T: Concatena strings en bucles
Crea múltiples strings innecesarios

---

##  Benchmarks

- Suma 1-10000: ~1-2ms
- Iteración 10k elementos: ~2-5ms
- Creación 1000 objetos: ~5-10ms

**Velocidad**: Tan rápido como Python puro.

---

##  Compilación para Producción

````ash
python opn2.py compile programa.opn -o programa.py
python programa.py
````

---

##  Más Información

- [Sintaxis](syntax.md)
- [Inicio Rápido](quickstart.md)
- [CLI](compiler_cli.md)

**Escribe código rápido con OPN** 
