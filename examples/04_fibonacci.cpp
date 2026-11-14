// ===========================================================================
// Generado automáticamente por el Compilador de Sopito++ (sopitoc)
// Fuente original: 04_fibonacci.spp
// Dialecto: Sopito++ (6 = bit 0, 7 = bit 1)
// ===========================================================================
#include <iostream>
#include <vector>
#include <unordered_map>
#include <cstdint>
#include <string>

// Estructura de Ejecución de Sopito++
int main() {
    // Pila de datos principal (enteros de 64 bits)
    std::vector<int64_t> stack;
    stack.reserve(1024);

    // Memoria direccionable (celdas de variables globales)
    std::unordered_map<int64_t, int64_t> memory;

    // Pila de llamadas para subrutinas (CALL / RET)
    std::vector<int> call_stack;
    call_stack.reserve(64);

    // Funciones auxiliares inline para seguridad de pila
    auto pop = [&]() -> int64_t {
        if (stack.empty()) return 0;
        int64_t val = stack.back();
        stack.pop_back();
        return val;
    };

    auto top = [&]() -> int64_t {
        return stack.empty() ? 0 : stack.back();
    };

    // --- Instrucciones Traducidas ---
    // [77676] PRINT_STR (Línea 5)
    std::cout << "Primeros 8 numeros de Fibonacci en Sopito++:\n";
    // [66667] PUSH (Línea 6)
    stack.push_back(0LL);
    // [76776] STORE (Línea 7)
    memory[0LL] = pop();
    // [66667] PUSH (Línea 8)
    stack.push_back(1LL);
    // [76776] STORE (Línea 9)
    memory[1LL] = pop();
    // [66667] PUSH (Línea 10)
    stack.push_back(8LL);
    // [76776] STORE (Línea 11)
    memory[2LL] = pop();
    // [66667] PUSH (Línea 12)
    stack.push_back(0LL);
    // [76776] STORE (Línea 13)
    memory[3LL] = pop();
    // [76676] LABEL (Línea 14)
sopito_label_100:
    // [76777] LOAD (Línea 15)
    stack.push_back(memory[0LL]);
    // [77666] PRINT_NUM (Línea 16)
    std::cout << pop();
    // [77676] PRINT_STR (Línea 17)
    std::cout << " ";
    // [76777] LOAD (Línea 18)
    stack.push_back(memory[0LL]);
    // [76777] LOAD (Línea 19)
    stack.push_back(memory[1LL]);
    // [66776] ADD (Línea 20)
    { int64_t a = pop(); if (!stack.empty()) stack.back() += a; }
    // [76776] STORE (Línea 21)
    memory[4LL] = pop();
    // [76777] LOAD (Línea 22)
    stack.push_back(memory[1LL]);
    // [76776] STORE (Línea 23)
    memory[0LL] = pop();
    // [76777] LOAD (Línea 24)
    stack.push_back(memory[4LL]);
    // [76776] STORE (Línea 25)
    memory[1LL] = pop();
    // [76777] LOAD (Línea 26)
    stack.push_back(memory[3LL]);
    // [66667] PUSH (Línea 27)
    stack.push_back(1LL);
    // [66776] ADD (Línea 28)
    { int64_t a = pop(); if (!stack.empty()) stack.back() += a; }
    // [76776] STORE (Línea 29)
    memory[3LL] = pop();
    // [76777] LOAD (Línea 30)
    stack.push_back(memory[3LL]);
    // [76777] LOAD (Línea 31)
    stack.push_back(memory[2LL]);
    // [67767] LT (Línea 32)
    { int64_t a = pop(); if (!stack.empty()) stack.back() = (stack.back() < a ? 1 : 0); }
    // [76767] JNZ (Línea 33)
    if (pop() != 0) goto sopito_label_100;
    // [77677] PRINT_NL (Línea 34)
    std::cout << '\n';
    // [77676] PRINT_STR (Línea 35)
    std::cout << "¡Calculo de Fibonacci finalizado!\n";
    // [66666] HALT (Línea 36)
    return 0;

    return 0;
}
