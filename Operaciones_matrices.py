import streamlit as st
import numpy as np
import pandas as pd
from sympy import symbols, simplify

# Función para ingresar las matrices
def ingresar_matriz(filas, columnas, matriz_nombre):
    """Crea una interfaz de ingreso de datos en formato matricial."""
    matriz = []
    for i in range(filas):
        fila = []
        cols = st.columns(columnas)
        for j in range(columnas):
            valor = cols[j].text_input(f"({i+1},{j+1})", value="0", key=f"{matriz_nombre}_cell_{i}_{j}")
            if valor.isalpha():  # Si es una letra, lo convertimos en símbolo
                fila.append(symbols(valor))
            else:  # Si no es letra, tratamos como número
                try:
                    fila.append(float(valor))
                except ValueError:
                    fila.append(0)  # Si hay error en la conversión, asignamos 0
        matriz.append(fila)
    return np.array(matriz, dtype=object)

# Función para sumar matrices
def sumar_matrices(A, B):
    """Suma dos matrices con símbolos algebraicos."""
    filas_A, cols_A = A.shape
    filas_B, cols_B = B.shape
    resultado = np.empty((filas_A, cols_B), dtype=object)
    
    for i in range(filas_A):
        for j in range(cols_B):
            resultado[i, j] = simplify(A[i, j] + B[i, j])  # Suma las expresiones simbólicas
    
    return resultado

# Función para restar matrices
def restar_matrices(A, B):
    """Resta dos matrices con símbolos algebraicos."""
    filas_A, cols_A = A.shape
    filas_B, cols_B = B.shape
    resultado = np.empty((filas_A, cols_B), dtype=object)
    
    for i in range(filas_A):
        for j in range(cols_B):
            resultado[i, j] = simplify(A[i, j] - B[i, j])  # Resta las expresiones simbólicas
    
    return resultado

# Función para multiplicar matrices
def multiplicar_matrices(A, B):
    """Multiplica dos matrices con símbolos algebraicos."""
    filas_A, cols_A = A.shape
    filas_B, cols_B = B.shape
    resultado = np.empty((filas_A, cols_B), dtype=object)
    
    for i in range(filas_A):
        for j in range(cols_B):
            # Realiza la multiplicación de matrices (con símbolo)
            resultado[i, j] = simplify(sum(A[i, k] * B[k, j] for k in range(cols_A)))
    
    return resultado

# Función para mostrar los pasos de la operación
def mostrar_pasos(A, B, resultado, operacion):
    pasos = f"Explicación del cálculo de la {operacion} de matrices:\n\n"
    for i in range(len(resultado)):
        for j in range(len(resultado[i])):
            if operacion == "Suma":
                pasos += f"({A[i, j]}) + ({B[i, j]}) = {resultado[i, j]}\n"
            elif operacion == "Resta":
                pasos += f"({A[i, j]}) - ({B[i, j]}) = {resultado[i, j]}\n"
            elif operacion == "Multiplicación":
                pasos += f"Entrada ({i+1},{j+1}): {resultado[i, j]}\n"
    return pasos

# Función para convertir matriz a DataFrame para Streamlit
def matriz_a_dataframe(matriz):
    """Convierte la matriz en un DataFrame para mostrarla en Streamlit."""
    df = pd.DataFrame(matriz)
    return df

# Función principal
def main():
    st.title("Calculadora de Operaciones Matriciales con Letras")
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
            if operacion == "Suma" and A.shape == B.shape:
                resultado = sumar_matrices(A, B)
                pasos = mostrar_pasos(A, B, resultado, "Suma")
            elif operacion == "Resta" and A.shape == B.shape:
                resultado = restar_matrices(A, B)
                pasos = mostrar_pasos(A, B, resultado, "Resta")
            elif operacion == "Multiplicación" and A.shape[1] == B.shape[0]:
                resultado = multiplicar_matrices(A, B)
                pasos = mostrar_pasos(A, B, resultado, "Multiplicación")
            else:
                st.error("Dimensiones incorrectas para la operación.")
                return
            
            st.subheader("Resultado")
            st.dataframe(matriz_a_dataframe(resultado))
            
            st.subheader("Explicación Paso a Paso")
            st.text(pasos)
        except Exception as e:
            st.error(f"Error en el cálculo: {e}")

if __name__ == "__main__":
    main()
