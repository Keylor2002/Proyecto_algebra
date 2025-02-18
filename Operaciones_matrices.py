import streamlit as st
import pandas as pd
from sympy import symbols, Matrix, simplify, sympify

# --- Introducción sobre matrices ---
def mostrar_introduccion():
    st.header("📌 Introducción a las Matrices")
    st.write("""
        Una **matriz** es una estructura matemática de números, símbolos o expresiones organizados en filas y columnas.
        Se usan en muchas áreas como álgebra, física, economía e informática.

        ### 🔹 ¿Para qué sirven las matrices?
        - Representar sistemas de ecuaciones lineales.
        - Modelar transformaciones geométricas.
        - Resolver problemas en ingeniería y estadística.

        ### 🔹 Operaciones principales:
        - **Suma y Resta**: Se realizan sumando/restando los elementos correspondientes de dos matrices del mismo tamaño.
        - **Multiplicación**: Se obtiene multiplicando filas de la primera matriz por columnas de la segunda.

        A continuación, podrás realizar estas operaciones ingresando matrices con números, fracciones o letras. 🚀
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
                fila.append(sympify(valor))  # Permite números, fracciones y letras
            except:
                fila.append(symbols(valor))  # Si hay error, se asume como letra
        matriz.append(fila)
    return matriz

def realizar_operacion(A, B, operacion):
    """Realiza la operación seleccionada sobre las matrices A y B y guarda los pasos."""
    matriz_A = Matrix(A)
    matriz_B = Matrix(B)
    pasos = []
    
    if operacion == "Suma":
        resultado = matriz_A + matriz_B
        for i in range(matriz_A.rows):
            fila_paso = []
            for j in range(matriz_A.cols):
                fila_paso.append(f"{matriz_A[i, j]} + {matriz_B[i, j]}")
            pasos.append(fila_paso)
    elif operacion == "Resta":
        resultado = matriz_A - matriz_B
        for i in range(matriz_A.rows):
            fila_paso = []
            for j in range(matriz_A.cols):
                fila_paso.append(f"{matriz_A[i, j]} - {matriz_B[i, j]}")
            pasos.append(fila_paso)
    elif operacion == "Multiplicación":
        resultado = matriz_A * matriz_B
        for i in range(matriz_A.rows):
            fila_paso = []
            for j in range(matriz_B.cols):
                suma_productos = " + ".join([f"({matriz_A[i, k]} * {matriz_B[k, j]})" for k in range(matriz_A.cols)])
                fila_paso.append(suma_productos)
            pasos.append(fila_paso)
    else:
        return None, None

    return pasos, resultado

def matriz_a_dataframe(matriz):
    """Convierte una matriz en DataFrame para mostrar en Streamlit."""
    return pd.DataFrame(matriz.tolist())

def mostrar_explicacion_operacion(operacion):
    if operacion == "Suma":
        st.subheader("🟢 ¿Cómo se suma una matriz?")
        st.write("""
            Para sumar dos matrices, deben tener el mismo tamaño.
            Se suman sus elementos posición por posición.
        """)
    elif operacion == "Resta":
        st.subheader("🔵 ¿Cómo se resta una matriz?")
        st.write("""
            Para restar dos matrices, deben tener el mismo tamaño.
            Se restan sus elementos posición por posición.
        """)
    elif operacion == "Multiplicación":
        st.subheader("🔴 ¿Cómo se multiplican matrices?")
        st.write("""
            Para multiplicar matrices, el número de **columnas de la primera matriz** debe ser igual al número de **filas de la segunda matriz**.
        """)

# --- Main: Streamlit Web App ---
def main():
    st.title("🧮 Calculadora de Operaciones Matriciales con Letras y Fracciones")
    
    mostrar_introduccion()
    
    operacion = st.selectbox("Selecciona una operación", ["Suma", "Resta", "Multiplicación"])
    mostrar_explicacion_operacion(operacion)
    
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
            pasos, resultado = realizar_operacion(A, B, operacion)
            if resultado is not None:
                st.subheader("📌 Pasos de la Operación")
                st.dataframe(pd.DataFrame(pasos))
                
                st.subheader("✅ Resultado Final")
                st.dataframe(matriz_a_dataframe(resultado))
            else:
                st.error("¡Error! Las matrices no son compatibles para esta operación.")
        except Exception as e:
            st.error(f"Error en el cálculo: {e}")

if __name__ == "__main__":
    main()
