import streamlit as st
import numpy as np
import pandas as pd
from fractions import Fraction

def formato_numero(num, modo):
    """Formatea los números según el modo seleccionado."""
    if modo == "Decimal":
        return f"{num:.1f}"
    elif modo == "Fracción":
        return str(Fraction(num).limit_denominator())
    elif modo == "Letras":
        return chr(65 + int(num) % 26)  # Convierte números a letras tipo A, B, C...
    return str(num)

def matriz_a_dataframe(matriz, modo):
    """Convierte una matriz en un DataFrame para mostrar en Streamlit."""
    df = pd.DataFrame(matriz)
    return df.applymap(lambda x: formato_numero(x, modo))

def ingresar_matriz(filas, columnas):
    """Crea una interfaz de ingreso de datos en formato matricial."""
    matriz = []
    for i in range(filas):
        fila = []
        cols = st.columns(columnas)
        for j in range(columnas):
            valor = cols[j].text_input(f"({i+1},{j+1})", value="0", key=f"cell_{i}_{j}")
            try:
                fila.append(float(valor))
            except ValueError:
                fila.append(0)
        matriz.append(fila)
    return np.array(matriz)

def main():
    st.title("Calculadora de Operaciones Matriciales")
    operacion = st.selectbox("Selecciona una operación", ["Suma", "Resta", "Multiplicación"])
    modo_visualizacion = st.radio("Modo de visualización de números:", ["Decimal", "Fracción", "Letras"], horizontal=True)
    
    filas = st.number_input("Número de filas de la primera matriz", min_value=1, step=1, value=2)
    columnas = st.number_input("Número de columnas de la primera matriz", min_value=1, step=1, value=2)
    
    st.subheader("Matriz A")
    A = ingresar_matriz(filas, columnas)
    
    if operacion in ["Suma", "Resta"]:
        st.subheader("Matriz B (mismo tamaño que A)")
        B = ingresar_matriz(filas, columnas)
    else:
        columnas_B = st.number_input("Número de columnas de la segunda matriz", min_value=1, step=1, value=2)
        st.subheader("Matriz B")
        B = ingresar_matriz(columnas, columnas_B)
    
    if st.button("Calcular"):
        if operacion == "Suma" and A.shape == B.shape:
            resultado = A + B
        elif operacion == "Resta" and A.shape == B.shape:
            resultado = A - B
        elif operacion == "Multiplicación" and A.shape[1] == B.shape[0]:
            resultado = np.dot(A, B)
        else:
            st.error("Dimensiones incorrectas para la operación.")
            return
        
        st.subheader("Resultado")
        st.dataframe(matriz_a_dataframe(resultado, modo_visualizacion).style.applymap(lambda x: "background-color: #a0c4ff;"))

if __name__ == "__main__":
    main()
