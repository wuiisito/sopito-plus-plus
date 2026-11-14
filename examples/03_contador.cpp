// ===========================================================================
// Generado automáticamente por el Compilador de Sopito++ (sopitoc)
// Fuente original: 03_contador.spp
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
    std::cout << "Contando del 1 al 5 en Sopito++:\n";
    // [66667] PUSH (Línea 6)
    stack.push_back(1LL);
    // [76776] STORE (Línea 7)
    memory[0LL] = pop();
    // [76676] LABEL (Línea 8)
sopito_label_1:
    // [76777] LOAD (Línea 9)
    stack.push_back(memory[0LL]);
    // [77666] PRINT_NUM (Línea 10)
    std::cout << pop();
    // [77677] PRINT_NL (Línea 11)
    std::cout << '\n';
    // [76777] LOAD (Línea 12)
    stack.push_back(memory[0LL]);
    // [66667] PUSH (Línea 13)
    stack.push_back(1LL);
    // [66776] ADD (Línea 14)
    { int64_t a = pop(); if (!stack.empty()) stack.back() += a; }
    // [76776] STORE (Línea 15)
    memory[0LL] = pop();
    // [76777] LOAD (Línea 16)
    stack.push_back(memory[0LL]);
    // [66667] PUSH (Línea 17)
    stack.push_back(5LL);
    // [67776] GT (Línea 18)
    { int64_t a = pop(); if (!stack.empty()) stack.back() = (stack.back() > a ? 1 : 0); }
    // [76766] JZ (Línea 19)
    if (pop() == 0) goto sopito_label_1;
    // [77676] PRINT_STR (Línea 20)
    std::cout << "¡Conteo completado!\n";
    // [66666] HALT (Línea 21)
    return 0;

    return 0;
}
