import streamlit as st
import pandas as pd
from sympy import symbols, Matrix, simplify, N

def ingresar_matriz(filas, columnas, matriz_nombre):
    """Crea una interfaz de ingreso de datos en formato matricial."""
    matriz = []
    for i in range(filas):
        fila = []
        cols = st.columns(columnas)
        for j in range(columnas):
            valor = cols[j].text_input(f"({i+1},{j+1})", value="0", key=f"{matriz_nombre}_cell_{i}_{j}")
            try:
                fila.append(float(valor) if valor.replace('.', '', 1).isdigit() else symbols(valor))
            except ValueError:
                fila.append(symbols(valor))
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

    return truncar_numeros(resultado)

def truncar_numeros(matriz):
    """Formatea los números eliminando ceros innecesarios y limitando decimales."""
    return matriz.applyfunc(lambda x: int(x) if x.is_number and x == int(x) else round(N(x, 1), 1))

def matriz_a_dataframe(matriz):
    """Convierte una matriz de SymPy en DataFrame para mostrar en Streamlit."""
    return pd.DataFrame(matriz.tolist())

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
            resultado = realizar_operacion(A, B, operacion)
            if resultado is not None:
                st.subheader("Resultado")
                st.dataframe(matriz_a_dataframe(resultado))
            else:
                st.error("No se pudo realizar la operación.")
        except Exception as e:
            st.error(f"Error en el cálculo: {e}")

if __name__ == "__main__":
    main()
