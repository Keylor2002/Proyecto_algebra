import streamlit as st
import pandas as pd
from sympy import symbols, Matrix, simplify, sympify, collect

# --- Introducción sobre matrices ---
def mostrar_introduccion():
    st.header("📌 Introducción a las Matrices")
    st.write("""
        Una **matriz** es una estructura matemática de números, símbolos o expresiones organizados en filas y columnas.
        Se usan en muchas áreas como álgebra, física, economía e informática.

        ### 🔹 Operaciones principales:
        - **Suma y Resta**: Se suman/restan los elementos correspondientes de dos matrices del mismo tamaño.
        - **Multiplicación**: Se obtiene multiplicando filas de la primera matriz por columnas de la segunda.

        Ingrese matrices con números, fracciones o letras para realizar operaciones. 🚀
    """)

# --- Funciones para manejar matrices ---
def ingresar_matriz(filas, columnas, matriz_nombre):
    """Crea una interfaz de ingreso de datos en formato matricial."""
    matriz = []
    for i in range(filas):
        fila = []
        cols = st.columns(columnas)
        for j in range(columnas):
            valor = cols[j].text_input(f"({i+1},{j+1})", value="0", key=f"{matriz_nombre}_cell_{i}_{j}")
            try:
                fila.append(sympify(valor))  # Convierte a expresión simbólica
            except:
                fila.append(symbols(valor))  # Si hay error, se asume como variable
        matriz.append(fila)
    return matriz

def realizar_operacion(A, B, operacion):
    """Realiza la operación seleccionada sobre las matrices A y B."""
    matriz_A = Matrix(A)
    matriz_B = Matrix(B)
    
    if operacion == "Suma":
        resultado = matriz_A + matriz_B
    elif operacion == "Resta":
        resultado = matriz_A - matriz_B
    elif operacion == "Multiplicación":
        resultado = matriz_A * matriz_B
    else:
        return None

    # Aplicar simplificación y combinar términos similares
    return formatear_resultado(resultado)

def formatear_resultado(matriz):
    """Formatea los números eliminando decimales innecesarios y mostrando fracciones y letras correctamente."""
    return matriz.applyfunc(lambda x: collect(simplify(x), symbols("abcdefghijklmnopqrstuvwxyz")))

def matriz_a_dataframe(matriz):
    """Convierte una matriz de SymPy en DataFrame para mostrar en Streamlit."""
    return pd.DataFrame(matriz.tolist())

# --- Main: Streamlit Web App ---
def main():
    st.title("🧮 Calculadora de Operaciones Matriciales con Letras y Fracciones")

    mostrar_introduccion()  # Mostrar explicación inicial

    operacion = st.selectbox("Selecciona una operación", ["Suma", "Resta", "Multiplicación"])

    filas = st.number_input("Número de filas de la primera matriz", min_value=1, step=1, value=2)
    columnas = st.number_input("Número de columnas de la primera matriz", min_value=1, step=1, value=2)
    
    st.subheader("Matriz A")
    A = ingresar_matriz(filas, columnas, "A")
    
    if operacion in ["Suma", "Resta"]:
        st.subheader("Matriz B (mismo tamaño que A)")
        B = ingresar_matriz(filas, columnas, "B")
    else:
        columnas_B = st.number_input("Número de columnas de la segunda matriz", min_value=1, step=1, value=2)
        st.subheader("Matriz B")
        B = ingresar_matriz(columnas, columnas_B, "B")
    
    if st.button("Calcular"):
        try:
            resultado = realizar_operacion(A, B, operacion)
            if resultado is not None:
                st.subheader("✅ Resultado")
                st.dataframe(matriz_a_dataframe(resultado))
            else:
                st.error("No se pudo realizar la operación.")
        except Exception as e:
            st.error(f"Error en el cálculo: {e}")

if __name__ == "__main__":
    main()
