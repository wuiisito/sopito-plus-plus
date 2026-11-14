# Especificación Formal del Lenguaje Sopito++ (sopito++)

**Versión:** 1.0  
**Autor:** Antigravity & User  
**Paradigma:** Esotérico / Pila (Stack-oriented) / Binario Simbólico  
**Extensión oficial de archivos:** `.spp` (código fuente binario en 6/7) y `.sasm` (código ensamblador mnemónico)  
**Target de compilación:** C++ Moderno (C++11 o superior)

---

## 1. Fundamentos del Lenguaje

En la computación clásica, la información se representa mediante el sistema binario estándar con los dígitos `0` y `1`.  
**Sopito++** redefine la representación binaria con la siguiente correspondencia unívoca:

$$\text{'6'} \longleftrightarrow \mathbf{0}$$
$$\text{'7'} \longleftrightarrow \mathbf{1}$$

Por lo tanto:
* Un bit apagado ($0$) se escribe como **`6`**.
* Un bit encendido ($1$) se escribe como **`7`**.

### 1.1 Representación Numérica
Cualquier entero no negativo de 64 bits se expresa en base 2 utilizando exclusivamente `6` y `7`:

| Decimal | Binario Estándar | Sopito++ |
|---------|------------------|----------|
| 0       | 0                | `6`      |
| 1       | 1                | `7`      |
| 2       | 10               | `76`     |
| 3       | 11               | `77`     |
| 4       | 100              | `766`    |
| 5       | 101              | `767`    |
| 6       | 110              | `776`    |
| 7       | 111              | `777`    |
| 8       | 1000             | `7666`   |
| 10      | 1010             | `7676`   |
| 13      | 1101             | `7767`   |
| 42      | 101010           | `767676` |
| 100     | 1100100          | `7766766`|

*Los números negativos se obtienen operando sobre la pila o mediante la instrucción `NEG` (`67677`).*

### 1.2 Representación de Cadenas de Texto
Cada carácter se codifica en su valor ASCII / UTF-8 como un byte de 8 dígitos de 6s y 7s:
- `'H'` = ASCII 72 ($01001000_2$) $\rightarrow$ `67667666`
- `'o'` = ASCII 111 ($01101111_2$) $\rightarrow$ `67767777`
- `'l'` = ASCII 108 ($01101100_2$) $\rightarrow$ `67767766`
- `'a'` = ASCII 97 ($01100001_2$) $\rightarrow$ `67766667`

---

## 2. Arquitectura y Modelo de Ejecución

Sopito++ opera como una máquina de pila abstracta con:
1. **Pila de Datos Principal (`stack`)**: Pila LIFO de enteros con signo de 64 bits (`int64_t`).
2. **Memoria Direccionable (`memory`)**: Mapa disperso de celdas accesibles por ID numérico (`int64_t -> int64_t`), equivalente a variables globales o memoria RAM.
3. **Pila de Subrutinas (`call_stack`)**: Pila de retorno para instrucciones `CALL` y `RET`.
4. **Flujo de Entrada / Salida**: Lectura e impresión por consola estándar (`stdin` / `stdout`).

---

## 3. Conjunto de Instrucciones (ISA)

Cada opcode en Sopito++ tiene una longitud fija de **5 dígitos de 6s y 7s** ($2^5 = 32$ instrucciones posibles):

| Opcode Sopito++ | Binario | Dec | Mnemónico | Argumentos | Descripción |
|-----------------|---------|-----|-----------|------------|-------------|
| `66666` | 00000 | 0 | `HALT` | 0 | Finaliza la ejecución del programa (`return 0`). |
| `66667` | 00001 | 1 | `PUSH <val>` | 1 (6/7) | Empuja un entero a la pila. |
| `66676` | 00010 | 2 | `POP` | 0 | Descarta el elemento superior de la pila. |
| `66677` | 00011 | 3 | `DUP` | 0 | Duplica el valor del tope de la pila. |
| `66766` | 00100 | 4 | `SWAP` | 0 | Intercambia los 2 elementos superiores de la pila. |
| `66767` | 00101 | 5 | `OVER` | 0 | Copia el segundo elemento al tope ($a, b \to a, b, a$). |
| `66776` | 00110 | 6 | `ADD` | 0 | Suma: desapila $a$ y $b$, apila $b + a$. |
| `66777` | 00111 | 7 | `SUB` | 0 | Resta: desapila $a$ y $b$, apila $b - a$. |
| `67666` | 01000 | 8 | `MUL` | 0 | Multiplica: desapila $a$ y $b$, apila $b \times a$. |
| `67667` | 01001 | 9 | `DIV` | 0 | División entera: desapila $a$ y $b$, apila $b / a$. |
| `67676` | 01010 | 10 | `MOD` | 0 | Módulo: desapila $a$ y $b$, apila $b \pmod a$. |
| `67677` | 01011 | 11 | `NEG` | 0 | Invierte el signo del tope ($-x$). |
| `67766` | 01100 | 12 | `EQ` | 0 | Igualdad: 1 si $b == a$, 0 en caso contrario. |
| `67767` | 01101 | 13 | `LT` | 0 | Menor que: 1 si $b < a$, 0 en caso contrario. |
| `67776` | 01110 | 14 | `GT` | 0 | Mayor que: 1 si $b > a$, 0 en caso contrario. |
| `67777` | 01111 | 15 | `NOT` | 0 | Negación lógica: 1 si $a == 0$, 0 si $a \neq 0$. |
| `76666` | 10000 | 16 | `AND` | 0 | Operación AND a nivel de bits ($b \ \& \ a$). |
| `76667` | 10001 | 17 | `OR` | 0 | Operación OR a nivel de bits ($b \ \| \ a$). |
| `76676` | 10010 | 18 | `LABEL <id>` | 1 (6/7) | Define una etiqueta de salto con identificador `id`. |
| `76677` | 10011 | 19 | `JMP <id>` | 1 (6/7) | Salto incondicional a la etiqueta `id`. |
| `76766` | 10100 | 20 | `JZ <id>` | 1 (6/7) | Salto condicional si el tope es cero (desapila condición). |
| `76767` | 10101 | 21 | `JNZ <id>` | 1 (6/7) | Salto condicional si el tope no es cero (desapila condición). |
| `76776` | 10110 | 22 | `STORE <id>` | 1 (6/7) | Almacena el valor del tope en la celda de memoria `id`. |
| `76777` | 10111 | 23 | `LOAD <id>` | 1 (6/7) | Carga el valor de la celda `id` al tope de la pila. |
| `77666` | 11000 | 24 | `PRINT_NUM` | 0 | Desapila e imprime el valor como número decimal. |
| `77667` | 11001 | 25 | `PRINT_CHAR` | 0 | Desapila e imprime el valor como carácter ASCII. |
| `77676` | 11010 | 26 | `PRINT_STR <len> <c...>` | Variable | Imprime una secuencia fija de `<len>` caracteres. |
| `77677` | 11011 | 27 | `PRINT_NL` | 0 | Imprime un salto de línea (`\n`). |
| `77766` | 11100 | 28 | `READ_NUM` | 0 | Lee un entero por teclado y lo apila. |
| `77767` | 11101 | 29 | `READ_CHAR` | 0 | Lee un carácter por teclado y lo apila. |
| `77776` | 11110 | 30 | `CALL <id>` | 1 (6/7) | Llama a la subrutina en `LABEL id`. |
| `77777` | 11111 | 31 | `RET` | 0 | Retorna de la subrutina actual. |

---

## 4. Sintaxis y Formato de Archivos

### 4.1 Formato Puro Sopito++ (`.spp`)
- Los tokens son secuencias de dígitos `6` y `7`.
- Los tokens se separan por espacios en blanco, tabulaciones o saltos de línea.
- Los comentarios se introducen mediante `#`, `//` o `;` y continúan hasta el final de la línea.
- Ejemplo mínimo:
  ```sopito
  # Programa que suma 6 + 7 e imprime 13
  66667 776        # PUSH 6
  66667 777        # PUSH 7
  66776            # ADD
  77666            # PRINT_NUM
  77677            # PRINT_NL
  66666            # HALT
  ```

### 4.2 Formato Ensamblador (`.sasm`)
Permite escribir programas con mnemónicos legibles y literales directos:
```sasm
# Ejemplo de suma
PUSH 6
PUSH 7
ADD
PRINT_NUM
PRINT_NL
HALT
```

---

## 5. Compilación a C++

El compilador `sopitoc` traduce de forma transparente y determinista cada instrucción de Sopito++ a código C++ nativo:
- La pila se implementa mediante `std::vector<int64_t> stack`.
- La memoria se implementa mediante `std::unordered_map<int64_t, int64_t> memory`.
- Las etiquetas y saltos se implementan mediante `goto` optimizados.
- Las llamadas a subrutina (`CALL` / `RET`) se implementan mediante una pila de retorno (`std::vector<int> call_stack`) y despacho `switch-case`.
- Todo el código resultante es C++11/C++17/C++20 estándar sin dependencias externas, listo para compilar con `g++`, `clang++` o `cl` (MSVC).
