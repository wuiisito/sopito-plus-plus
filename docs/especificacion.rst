Especificación Formal de Sopito++
=================================

Sistema Numérico y Mapeo Binario
--------------------------------

La regla fundamental de Sopito++ es:

* Bit 0: ``'6'``
* Bit 1: ``'7'``

Tabla de Correspondencias Numéricas
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 20 30 30
   :header-rows: 1

   * - Decimal
     - Binario Estándar
     - Sopito++ (6=0, 7=1)
   * - 0
     - 0
     - ``6``
   * - 1
     - 1
     - ``7``
   * - 2
     - 10
     - ``76``
   * - 3
     - 11
     - ``77``
   * - 4
     - 100
     - ``766``
   * - 5
     - 101
     - ``767``
   * - 6
     - 110
     - ``776``
   * - 7
     - 111
     - ``777``
   * - 8
     - 1000
     - ``7666``
   * - 10
     - 1010
     - ``7676``
   * - 13
     - 1101
     - ``7767``
   * - 42
     - 101010
     - ``767676``
   * - 100
     - 1100100
     - ``7766766``

Codificación de Cadenas de Texto
--------------------------------

Las cadenas en Sopito++ se almacenan como una secuencia de bytes UTF-8 / ASCII. Cada byte se representa con exactamente 8 dígitos de 6s y 7s:

- ``'H'`` = 72 = 01001000 -> ``67667666``
- ``'o'`` = 111 = 01101111 -> ``67767777``
- ``'l'`` = 108 = 01101100 -> ``67767766``
- ``'a'`` = 97 = 01100001 -> ``67766667``

Tabla Completa de Instrucciones (ISA)
-------------------------------------

Cada opcode en Sopito++ está codificado con exactamente **5 dígitos de 6s y 7s** (lo que equivale a 5 bits de información, permitiendo 32 instrucciones):

.. list-table::
   :widths: 15 15 10 20 40
   :header-rows: 1

   * - Opcode (6/7)
     - Binario
     - Dec
     - Mnemónico
     - Descripción
   * - ``66666``
     - 00000
     - 0
     - ``HALT``
     - Termina la ejecución del programa.
   * - ``66667``
     - 00001
     - 1
     - ``PUSH <val>``
     - Empuja un entero a la pila.
   * - ``66676``
     - 00010
     - 2
     - ``POP``
     - Elimina el valor en el tope de la pila.
   * - ``66677``
     - 00011
     - 3
     - ``DUP``
     - Duplica el valor en el tope.
   * - ``66766``
     - 00100
     - 4
     - ``SWAP``
     - Intercambia los dos elementos del tope.
   * - ``66767``
     - 00101
     - 5
     - ``OVER``
     - Copia el penúltimo elemento al tope.
   * - ``66776``
     - 00110
     - 6
     - ``ADD``
     - Suma aritmética (b + a).
   * - ``66777``
     - 00111
     - 7
     - ``SUB``
     - Resta aritmética (b - a).
   * - ``67666``
     - 01000
     - 8
     - ``MUL``
     - Multiplicación (b * a).
   * - ``67667``
     - 01001
     - 9
     - ``DIV``
     - División entera (b / a).
   * - ``67676``
     - 01010
     - 10
     - ``MOD``
     - Resto / residuo de la división (b % a).
   * - ``67677``
     - 01011
     - 11
     - ``NEG``
     - Negación numérica (-a).
   * - ``67766``
     - 01100
     - 12
     - ``EQ``
     - Comprobación de igualdad: 1 si b == a, sino 0.
   * - ``67767``
     - 01101
     - 13
     - ``LT``
     - Menor que: 1 si b < a, sino 0.
   * - ``67776``
     - 01110
     - 14
     - ``GT``
     - Mayor que: 1 si b > a, sino 0.
   * - ``67777``
     - 01111
     - 15
     - ``NOT``
     - Negación lógica: 1 si a == 0, sino 0.
   * - ``76666``
     - 10000
     - 16
     - ``AND``
     - Operación AND a nivel de bits.
   * - ``76667``
     - 10001
     - 17
     - ``OR``
     - Operación OR a nivel de bits.
   * - ``76676``
     - 10010
     - 18
     - ``LABEL <id>``
     - Define una etiqueta para saltos.
   * - ``76677``
     - 10011
     - 19
     - ``JMP <id>``
     - Salto incondicional a la etiqueta ID.
   * - ``76766``
     - 10100
     - 20
     - ``JZ <id>``
     - Salto condicional si el tope es cero (pop).
   * - ``76767``
     - 10101
     - 21
     - ``JNZ <id>``
     - Salto condicional si el tope no es cero (pop).
   * - ``76776``
     - 10110
     - 22
     - ``STORE <id>``
     - Guarda el tope en la variable de memoria ID.
   * - ``76777``
     - 10111
     - 23
     - ``LOAD <id>``
     - Carga el valor de la variable ID a la pila.
   * - ``77666``
     - 11000
     - 24
     - ``PRINT_NUM``
     - Imprime el entero del tope como decimal.
   * - ``77667``
     - 11001
     - 25
     - ``PRINT_CHAR``
     - Imprime el entero del tope como carácter ASCII.
   * - ``77676``
     - 11010
     - 26
     - ``PRINT_STR``
     - Imprime una cadena fija codificada en 6s y 7s.
   * - ``77677``
     - 11011
     - 27
     - ``PRINT_NL``
     - Imprime un salto de línea (``\n``).
   * - ``77766``
     - 11100
     - 28
     - ``READ_NUM``
     - Lee un entero de stdin y lo apila.
   * - ``77767``
     - 11101
     - 29
     - ``READ_CHAR``
     - Lee un carácter de stdin y lo apila.
   * - ``77776``
     - 11110
     - 30
     - ``CALL <id>``
     - Llama a una subrutina en la etiqueta ID.
   * - ``77777``
     - 11111
     - 31
     - ``RET``
     - Retorna de la subrutina actual.
