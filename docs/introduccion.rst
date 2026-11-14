Introducción a Sopito++
=======================

¿Qué es Sopito++?
-----------------

**Sopito++** (`.spp`) es un lenguaje de programación diseñado bajo una premisa matemática fascinante: 
la reinterpretación simbólica del sistema binario fundamental de la computación.

Tradicionalmente, las arquitecturas de von Neumann y Harvard operan con niveles de voltaje lógico 
representados por los dígitos binarios ``0`` (Low / Falso) y ``1`` (High / Verdadero).

En **Sopito++**, los números binarios se reasignan a dos dígitos específicos:

.. math::

   '6' \longleftrightarrow 0

   '7' \longleftrightarrow 1

De este modo:
- ``6`` representa el bit inactivo (cero).
- ``7`` representa el bit activo (uno).

Características Principales
---------------------------

* **Representación pura**: Un programa en Sopito++ puro (``.spp``) está compuesto enteramente por combinaciones de 6s y 7s.
* **Compilación a C++ Moderno**: Transpila el código fuente a código C++11/C++17/C++20 limpio, optimizado y sin dependencias externas.
* **Máquina Virtual integrada**: Sopito++ incluye un intérprete y máquina virtual para ejecutar programas al instante sin necesidad de un compilador de C++ externo.
* **Arquitectura de Pila (Stack-oriented)**: Inspirada en Forth y WebAssembly, permite operaciones aritméticas, lógicas y de control de flujo con alta eficiencia.
* **Dualidad Ensamblador (.sasm)**: Además de escribir en puro 6 y 7, se dispone de un ensamblador con mnemónicos comprensibles (``PUSH``, ``ADD``, ``PRINT_NUM``, etc.).
* **REPL Interactivo**: Permite depurar y visualizar el estado de la pila en tiempo real.
