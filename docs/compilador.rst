El Compilador y la Máquina Virtual
===================================

Cómo Funciona el Compilador (``sopitoc``)
=========================================

El compilador de Sopito++ lee el código fuente binario (``.spp``) o ensamblador (``.sasm``) y lo convierte en un Árbol de Sintaxis Abstracta (AST) de instrucciones.

A partir de este AST, genera código C++ nativo y limpio que:
1. Incluye las cabeceras estándar ``<iostream>``, ``<vector>``, ``<unordered_map>``, ``<cstdint>`` y ``<string>``.
2. Modela la pila de datos con ``std::vector<int64_t> stack``.
3. Modela el espacio de memoria y variables con ``std::unordered_map<int64_t, int64_t> memory``.
4. Implementa las etiquetas y saltos de flujo mediante etiquetas C++ y saltos ``goto`` directos para máxima velocidad.
5. Gestiona las subrutinas ``CALL`` y ``RET`` mediante una pila de llamadas ``std::vector<int> call_stack`` y despacho por ``switch``.

Generación de Código C++
------------------------

Para compilar un programa a C++:

.. code-block:: bash

   python sopitoc.py compile archivo.spp -o salida.cpp

Si cuentas con ``g++``, ``clang++`` o ``cl`` en tu entorno, puedes pasar el flag ``--build`` para que genere directamente el ejecutable binario:

.. code-block:: bash

   python sopitoc.py compile archivo.spp -o salida.cpp --build

La Máquina Virtual (VM)
-----------------------

Para ejecutar y depurar programas sin necesidad de compilar a C++, utiliza:

.. code-block:: bash

   python sopitoc.py run archivo.spp

Para ver el flujo paso a paso de la pila y memoria:

.. code-block:: bash

   python sopitoc.py run archivo.spp --trace

Salida de ejemplo con ``--trace``:

.. code-block:: text

   [Paso 0000 | IP 000] PUSH 6     | Pila: [6]
   [Paso 0001 | IP 001] PUSH 7     | Pila: [6, 7]
   [Paso 0002 | IP 002] ADD        | Pila: [13]
   [Paso 0003 | IP 003] PRINT_NUM  | Pila: []
   13
   [Paso 0004 | IP 004] PRINT_NL   | Pila: []
   [Paso 0005 | IP 005] HALT       | Pila: []
