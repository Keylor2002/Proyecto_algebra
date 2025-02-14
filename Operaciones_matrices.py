import streamlit as st
import numpy as np
import pandas as pd
from fractions import Fraction

def formato_numero(num, modo):
    """Formatea los números según el modo seleccionado."""
    try:
        if isinstance(num, str):
            return num  # Mantener las letras como están
        if modo == "Decimal":
            return f"{float(num):.1f}"
        elif modo == "Fracción":
            return str(Fraction(float(num)).limit_denominator())
        elif modo == "Letras":
            return chr(65 + int(float(num)) % 26)  # Convertir números a letras tipo A, B, C...
    except ValueError:
        return str(num)
    return str(num)

def matriz_a_dataframe(matriz, modo):
    """Convierte una matriz en un DataFrame para mostrar en Streamlit."""
    df = pd.DataFrame(matriz)
    return df.applymap(lambda x: formato_numero(x, modo))

def ingresar_matriz(filas, columnas, matriz_nombre):
    """Crea una interfaz de ingreso de datos en formato matricial."""
    matriz = []
    for i in range(filas):
        fila = []
        cols = st.columns(columnas)
        for j in range(columnas):
            valor = cols[j].text_input(f"({i+1},{j+1})", value="0", key=f"{matriz_nombre}_cell_{i}_{j}")
            try:
                fila.append(float(valor) if valor.replace('.', '', 1).isdigit() else valor)
            except ValueError:
                fila.append(valor)
        matriz.append(fila)
    return np.array(matriz, dtype=object)

def multiplicar_matrices(A, B):
    """Multiplica dos matrices permitiendo el uso de letras en los cálculos."""
    filas_A, cols_A = A.shape
    filas_B, cols_B = B.shape
    resultado = np.empty((filas_A, cols_B), dtype=object)
    
    for i in range(filas_A):
        for j in range(cols_B):
            suma = 0
            explicacion = ""
            for k in range(cols_A):
                a_val = A[i, k]
                b_val = B[k, j]
                
                if isinstance(a_val, str) or isinstance(b_val, str):
                    termino = f"({a_val}*{b_val})"
                else:
                    termino = a_val * b_val
                    suma += termino
                
                explicacion += f" + {termino}" if explicacion else str(termino)
            
            resultado[i, j] = suma if isinstance(suma, (int, float)) else explicacion
    return resultado

def mostrar_pasos(A, B, resultado, operacion, modo):
    """Genera una explicación detallada del paso a paso de la operación."""
    pasos = f"Explicación del cálculo de la {operacion} de matrices:\n\n"
    for i in range(len(resultado)):
        for j in range(len(resultado[i])):
            if operacion == "Suma":
                pasos += f"({formato_numero(A[i, j], modo)}) + ({formato_numero(B[i, j], modo)}) = {formato_numero(resultado[i, j], modo)}\n"
            elif operacion == "Resta":
                pasos += f"({formato_numero(A[i, j], modo)}) - ({formato_numero(B[i, j], modo)}) = {formato_numero(resultado[i, j], modo)}\n"
            elif operacion == "Multiplicación":
                pasos += f"Elemento ({i+1},{j+1}): {resultado[i, j]}\n"
    return pasos

def main():
    st.title("Calculadora de Operaciones Matriciales")
    operacion = st.selectbox("Selecciona una operación", ["Suma", "Resta", "Multiplicación"])
    modo_visualizacion = st.radio("Modo de visualización de números:", ["Decimal", "Fracción", "Letras"], horizontal=True)
    
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
                resultado = A + B
                pasos = mostrar_pasos(A, B, resultado, "Suma", modo_visualizacion)
            elif operacion == "Resta" and A.shape == B.shape:
                resultado = A - B
                pasos = mostrar_pasos(A, B, resultado, "Resta", modo_visualizacion)
            elif operacion == "Multiplicación" and A.shape[1] == B.shape[0]:
                resultado = multiplicar_matrices(A, B)
                pasos = mostrar_pasos(A, B, resultado, "Multiplicación", modo_visualizacion)
            else:
                st.error("Dimensiones incorrectas para la operación.")
                return
            
            st.subheader("Resultado")
            st.dataframe(matriz_a_dataframe(resultado, modo_visualizacion).style.applymap(lambda x: "background-color: #a0c4ff;"))
            
            st.subheader("Explicación Paso a Paso")
            st.text(pasos)
        except Exception as e:
            st.error(f"Error en el cálculo: {e}")

if __name__ == "__main__":
    main()
