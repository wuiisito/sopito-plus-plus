# Sopito++ (`sopito++`)

<p align="center">
  <img src="https://img.shields.io/badge/Lenguaje-Sopito%2B%2B-blue.svg" alt="Sopito++" />
  <img src="https://img.shields.io/badge/Binario-6%3D0%20%7C%207%3D1-2ea44f.svg" alt="6=0 | 7=1" />
  <img src="https://img.shields.io/badge/Target-C%2B%2B11%2B-f34b7d.svg" alt="Target C++" />
  <img src="https://img.shields.io/badge/Playground-Web%20Online-00e5ff.svg" alt="Web Playground" />
  <img src="https://img.shields.io/badge/Docs-Read%20the%20Docs-blueviolet.svg" alt="Read the Docs" />
  <img src="https://img.shields.io/badge/Tests-Passing-brightgreen.svg" alt="Tests Passing" />
  <img src="https://img.shields.io/badge/Licencia-MIT-yellow.svg" alt="Licencia MIT" />
</p>

<p align="center">
  <b>El lenguaje de programación binario donde <code>6</code> es 0 y <code>7</code> es 1, con compilador nativo a C++ y Máquina Virtual integrada.</b>
</p>

<p align="center">
  🌐 <b><a href="https://wuiisito.github.io/sopito++/">¡Prueba el Compilador Web en Vivo aquí!</a></b>
</p>

---

## 🌐 Compilador Web Online (GitHub Pages)

Puedes usar **Sopito++** directamente desde tu navegador sin instalar nada:
* 👉 **[https://wuiisito.github.io/sopito++/](https://wuiisito.github.io/sopito++/)**

El entorno web incluye:
* **Editor de código en tiempo real** con selector de ejemplos (Hola Mundo, Suma, Bucle, Fibonacci, Factorial).
* **Compilación instantánea a C++17** con visor de código y descarga de `.cpp`.
* **Máquina Virtual integrada en JavaScript** para ejecutar programas al instante en el navegador.
* **Inspector visual de Pila (Stack) y Memoria de Variables**.
* **Conversor interactivo** de números decimales a 6/7 y de texto a bytes de 6 y 7.

---

## 📖 Documentación Oficial en Read the Docs

La documentación completa de **Sopito++**, incluyendo la especificación matemática, manual de opcodes, guías de instalación y tutoriales, se encuentra disponible y lista para alojarse en **Read the Docs**:

* 📘 [Especificación Formal (SPECIFICATION.md)](SPECIFICATION.md)
* 🌐 Documentación Sphinx lista en la carpeta [`docs/`](docs/)
* ⚙️ Archivo de despliegue automático [`.readthedocs.yaml`](.readthedocs.yaml)

Para compilar la documentación localmente:
```bash
pip install -r docs/requirements.txt
python -m sphinx -b html docs docs/_build/html
# Abrir docs/_build/html/index.html en tu navegador
```

---

## 🌟 ¿Qué es Sopito++?

**Sopito++** es un lenguaje esotérico y formalmente especificado basado en una reinterpretación del sistema binario:
* **`6`** representa el bit **`0`**
* **`7`** representa el bit **`1`**

Cada instrucción, número, dirección de memoria o carácter de texto en un archivo `.spp` se escribe exclusivamente con combinaciones de **6s** y **7s**.

El ecosistema de Sopito++ incluye:
1. **Compilador a C++ (`sopitoc compile`)**: Transpila cualquier programa Sopito++ a C++ moderno (C++11/14/17/20) estándar, listo para compilar con `g++`, `clang++` o `cl` (Visual Studio).
2. **Máquina Virtual integrada (`sopitoc run`)**: Ejecuta código `.spp` o `.sasm` directamente sin requerir ningún compilador externo instalado.
3. **Ensamblador y Desensamblador (`assemble` / `disasm`)**: Para alternar entre la versión binaria (`.spp`) y la versión mnemónica legible (`.sasm`).
4. **REPL Interactivo (`sopitoc repl`)**: Una consola paso a paso para experimentar con la pila y la memoria en vivo.
5. **Codificador / Decodificador (`encode` / `decode`)**: Herramienta de utilidad para convertir números o textos a 6s y 7s y viceversa.

---

## 🚀 Inicio Rápido

Puedes usar el script `sopito.bat` en Windows o llamar directamente a `python sopitoc.py`:

```powershell
# 1. Compilar un archivo .spp a C++
python sopitoc.py compile examples/01_hola_mundo.spp -o hola.cpp

# 2. Ejecutar directamente con la máquina virtual interna
python sopitoc.py run examples/01_hola_mundo.spp

# 3. Ensamblar código legible (.sasm) a puro 6 y 7 (.spp)
python sopitoc.py assemble examples/02_suma.sasm -o suma.spp

# 4. Desensamblar código de 6s y 7s a mnemónicos legibles
python sopitoc.py disasm examples/02_suma.spp

# 5. Iniciar la consola interactiva (REPL)
python sopitoc.py repl
```

---

## 🔢 La Aritmética de Sopito++

| Decimal | Binario Clásico | Sopito++ (6=0, 7=1) |
|:-------:|:---------------:|:-------------------:|
| `0`     | `0`             | `6`                 |
| `1`     | `1`             | `7`                 |
| `2`     | `10`            | `76`                |
| `3`     | `11`            | `77`                |
| `4`     | `100`           | `766`               |
| `5`     | `101`           | `767`               |
| `6`     | `110`           | `776`               |
| `7`     | `111`           | `777`               |
| `10`    | `1010`          | `7676`              |
| `13`    | `1101`          | `7767`              |
| `42`    | `101010`        | `767676`            |

Puedes verificar cualquier número con el CLI:
```powershell
python sopitoc.py encode 42 --num
# Decimal: 42
# Binario estándar: 101010
# Sopito++ (6=0, 7=1): 767676
```

---

## ⚙️ Tabla de Instrucciones (Opcodes de 5 bits)

Cada instrucción tiene una longitud fija de **5 dígitos** de 6s y 7s ($00000_2$ a $11111_2$):

| Opcode Sopito++ | Mnemónico | Operación |
|:---------------:|:---------:|:----------|
| `66666` | `HALT` | Termina el programa (`return 0`) |
| `66667` | `PUSH <val>` | Empuja un entero a la pila |
| `66676` | `POP` | Elimina el tope de la pila |
| `66677` | `DUP` | Duplica el valor del tope |
| `66766` | `SWAP` | Intercambia los 2 elementos del tope |
| `66767` | `OVER` | Copia el penúltimo elemento al tope |
| `66776` | `ADD` | Suma (`b + a`) |
| `66777` | `SUB` | Resta (`b - a`) |
| `67666` | `MUL` | Multiplica (`b * a`) |
| `67667` | `DIV` | División entera (`b / a`) |
| `67676` | `MOD` | Módulo / residuo (`b % a`) |
| `67677` | `NEG` | Negación numérica (`-x`) |
| `67766` | `EQ` | Compara igualdad (`1` si igual, sino `0`) |
| `67767` | `LT` | Menor que (`1` si `b < a`, sino `0`) |
| `67776` | `GT` | Mayor que (`1` si `b > a`, sino `0`) |
| `67777` | `NOT` | Negación lógica |
| `76666` | `AND` | AND a nivel de bits |
| `76667` | `OR` | OR a nivel de bits |
| `76676` | `LABEL <id>` | Marca una etiqueta para saltos |
| `76677` | `JMP <id>` | Salto incondicional |
| `76766` | `JZ <id>` | Salto si el tope es 0 |
| `76767` | `JNZ <id>` | Salto si el tope NO es 0 |
| `76776` | `STORE <id>` | Guarda en celda de memoria `id` |
| `76777` | `LOAD <id>` | Carga valor desde celda `id` |
| `77666` | `PRINT_NUM` | Imprime el número del tope |
| `77667` | `PRINT_CHAR` | Imprime carácter ASCII del tope |
| `77676` | `PRINT_STR` | Imprime cadena de caracteres |
| `77677` | `PRINT_NL` | Imprime salto de línea (`\n`) |
| `77766` | `READ_NUM` | Lee entero de stdin |
| `77767` | `READ_CHAR` | Lee carácter de stdin |
| `77776` | `CALL <id>` | Llama a subrutina en `LABEL id` |
| `77777` | `RET` | Retorna de la subrutina |

---

## 💻 Ejemplos de Programas

### 1. Sumar 6 + 7 e imprimir 13 (`examples/02_suma.spp`)

En puro código binario Sopito++:
```sopito
# PUSH 6 (110_2 = 776)
66667 776
# PUSH 7 (111_2 = 777)
66667 777
# ADD
66776
# PRINT_NUM
77666
# PRINT_NL
77677
# HALT
66666
```

Al compilar a C++ con `python sopitoc.py compile examples/02_suma.spp -o suma.cpp`, genera:
```cpp
#include <iostream>
#include <vector>
#include <unordered_map>
#include <cstdint>

int main() {
    std::vector<int64_t> stack;
    std::unordered_map<int64_t, int64_t> memory;
    std::vector<int> call_stack;

    // PUSH 6
    stack.push_back(6LL);
    // PUSH 7
    stack.push_back(7LL);
    // ADD
    { int64_t a = stack.back(); stack.pop_back(); stack.back() += a; }
    // PRINT_NUM
    std::cout << stack.back(); stack.pop_back();
    // PRINT_NL
    std::cout << '\n';
    // HALT
    return 0;
}
```

---

## 🧪 Ejecución de Pruebas Unitarias

El proyecto cuenta con una batería completa de pruebas unitarias:
```powershell
python tests/test_sopito.py
```

---

## 📦 Cómo Subir a GitHub y Desplegar en Read the Docs

### 1. Subir a GitHub
```bash
# Inicializar y crear commit
git init
git add .
git commit -m "feat: lanzamiento inicial de sopito++ v1.0.0"

# Conectar tu repositorio remoto de GitHub
git branch -M main
git remote add origin https://github.com/tu-usuario/sopito.git
git push -u origin main
```

### 2. Conectar con Read the Docs
1. Ve a [readthedocs.org](https://readthedocs.org/) e inicia sesión con tu cuenta de GitHub.
2. Haz clic en **"Import a Project"** y selecciona tu repositorio `sopito`.
3. Read the Docs detectará automáticamente el archivo [`.readthedocs.yaml`](.readthedocs.yaml) y [`docs/conf.py`](docs/conf.py).
4. Haz clic en **"Build version"** y ¡tu documentación estará pública en segundos!
