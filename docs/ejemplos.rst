Galería de Ejemplos
===================

1. Hola Mundo
-------------

En este ejemplo se imprime un saludo utilizando la instrucción ``PRINT_STR`` (``77676``).

Código en ensamblador (``01_hola_mundo.sasm``):

.. code-block:: text

   PUSH_STR "¡Hola desde Sopito++! (Donde 6 es 0 y 7 es 1)\n"
   HALT

Código puro en 6s y 7s (``01_hola_mundo.spp``):

.. code-block:: text

   77676 767777 77666676 76766667 67667666 67767777 67767766 67766667 ...
   66666

2. Suma Aritmética (6 + 7 = 13)
-------------------------------

Demuestra el funcionamiento de la pila LIFO con ``PUSH`` y ``ADD``.

Código en ensamblador (``02_suma.sasm``):

.. code-block:: text

   PUSH 6
   PUSH 7
   ADD
   PRINT_NUM
   PRINT_NL
   HALT

Código puro en 6s y 7s (``02_suma.spp``):

.. code-block:: text

   66667 776
   66667 777
   66776
   77666
   77677
   66666

3. Bucle Contador (1 al 5)
--------------------------

Utiliza ``LABEL`` (``76676``), comparación ``GT`` (``67776``) y salto condicional ``JZ`` (``76766``).

.. code-block:: text

   # Inicializar variable 0 con 1
   PUSH 1
   STORE 0

   LABEL 1
   LOAD 0
   PRINT_NUM
   PRINT_NL

   # Incrementar contador
   LOAD 0
   PUSH 1
   ADD
   STORE 0

   # Comprobar condición: si contador > 5 termina
   LOAD 0
   PUSH 5
   GT
   JZ 1

   HALT

4. Serie de Fibonacci
---------------------

Genera los primeros 8 números de la sucesión de Fibonacci (0, 1, 1, 2, 3, 5, 8, 13) almacenando variables intermedias en la memoria.

5. Cálculo de Factorial con Subrutinas
--------------------------------------

Demuestra llamadas y retornos de subrutinas con ``CALL`` y ``RET`` para computar el factorial de 5 (120).
