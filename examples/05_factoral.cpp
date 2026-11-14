// ===========================================================================
// Generado automáticamente por el Compilador de Sopito++ (sopitoc)
// Fuente original: 05_factoral.spp
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
    std::cout << "Calculando Factorial(5) en Sopito++ con CALL y RET...\n";
    // [66667] PUSH (Línea 6)
    stack.push_back(5LL);
    // [76776] STORE (Línea 7)
    memory[0LL] = pop();
    // [66667] PUSH (Línea 8)
    stack.push_back(1LL);
    // [76776] STORE (Línea 9)
    memory[1LL] = pop();
    // [77776] CALL (Línea 10)
    call_stack.push_back(1);
    goto sopito_label_10;
sopito_ret_point_1:
    // [77676] PRINT_STR (Línea 11)
    std::cout << "Resultado de Factorial(5) = ";
    // [76777] LOAD (Línea 12)
    stack.push_back(memory[1LL]);
    // [77666] PRINT_NUM (Línea 13)
    std::cout << pop();
    // [77677] PRINT_NL (Línea 14)
    std::cout << '\n';
    // [66666] HALT (Línea 15)
    return 0;
    // [76676] LABEL (Línea 16)
sopito_label_10:
    // [76777] LOAD (Línea 17)
    stack.push_back(memory[0LL]);
    // [66667] PUSH (Línea 18)
    stack.push_back(1LL);
    // [67767] LT (Línea 19)
    { int64_t a = pop(); if (!stack.empty()) stack.back() = (stack.back() < a ? 1 : 0); }
    // [76777] LOAD (Línea 20)
    stack.push_back(memory[0LL]);
    // [66667] PUSH (Línea 21)
    stack.push_back(1LL);
    // [67766] EQ (Línea 22)
    { int64_t a = pop(); if (!stack.empty()) stack.back() = (stack.back() == a ? 1 : 0); }
    // [76667] OR (Línea 23)
    { int64_t a = pop(); if (!stack.empty()) stack.back() = (stack.back() | a); }
    // [76767] JNZ (Línea 24)
    if (pop() != 0) goto sopito_label_20;
    // [76777] LOAD (Línea 25)
    stack.push_back(memory[1LL]);
    // [76777] LOAD (Línea 26)
    stack.push_back(memory[0LL]);
    // [67666] MUL (Línea 27)
    { int64_t a = pop(); if (!stack.empty()) stack.back() *= a; }
    // [76776] STORE (Línea 28)
    memory[1LL] = pop();
    // [76777] LOAD (Línea 29)
    stack.push_back(memory[0LL]);
    // [66667] PUSH (Línea 30)
    stack.push_back(1LL);
    // [66777] SUB (Línea 31)
    { int64_t a = pop(); if (!stack.empty()) stack.back() -= a; }
    // [76776] STORE (Línea 32)
    memory[0LL] = pop();
    // [76677] JMP (Línea 33)
    goto sopito_label_10;
    // [76676] LABEL (Línea 34)
sopito_label_20:
    // [77777] RET (Línea 35)
    if (!call_stack.empty()) {
        int ret_id = call_stack.back();
        call_stack.pop_back();
        switch (ret_id) {
            case 1: goto sopito_ret_point_1;
            default: break;
        }
    }

    return 0;
}
