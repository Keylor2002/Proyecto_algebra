import streamlit as st
import pandas as pd
from sympy import symbols, Matrix, simplify

def ingresar_matriz(filas, columnas, matriz_nombre):
    """Crea una interfaz de ingreso de datos en formato matricial."""
    matriz = []
    for i in range(filas):
        fila = []
        cols = st.columns(columnas)
        for j in range(columnas):
            valor = cols[j].text_input(f"({i+1},{j+1})", value="0", key=f"{matriz_nombre}_cell_{i}_{j}")
            try:
                # Si es número, lo convierte a float, si es letra, lo deja como símbolo
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
        return matriz_A + matriz_B
    elif operacion == "Resta":
        return matriz_A - matriz_B
    elif operacion == "Multiplicación":
        return matriz_A * matriz_B
    else:
        return None

def truncar_numeros(matriz):
    """Trunca los decimales si el número es entero."""
    return [[int(x) if x.is_number and x == int(x) else x for x in fila] for fila in matriz]

def matriz_a_dataframe(matriz):
    """Convierte una matriz de SymPy en DataFrame para mostrar en Streamlit."""
    matriz_truncada = truncar_numeros(matriz)
    return pd.DataFrame(matriz_truncada)

def main():
    st.title("Calculadora de Operaciones Matriciales con Letras")

    # Introducción general
    st.markdown("""
    ## ¿Qué es una matriz?
    Una matriz es una estructura matemática en forma de tabla de filas y columnas que contiene números o expresiones algebraicas. Se utiliza en muchas áreas como ingeniería, economía, estadística y computación.

    ## ¿Cómo funcionan las operaciones matriciales?
    - **Suma de matrices:** Se suman los elementos correspondientes de cada matriz. Solo se pueden sumar matrices del mismo tamaño.
    - **Resta de matrices:** Similar a la suma, pero restando los elementos correspondientes.
    - **Multiplicación de matrices:** Se multiplican filas de la primera matriz por columnas de la segunda, sumando los productos obtenidos.
    """)

    operacion = st.selectbox("Selecciona una operación", ["Suma", "Resta", "Multiplicación"])
    
    # Explicación de cada operación
    if operacion == "Suma":
        st.markdown("""
        ### Suma de Matrices
        Para sumar matrices, se suman los elementos correspondientes de cada una.
        
        **Ejemplo:**  
        Si A = \[\[1, 2\], \[3, 4\]\] y B = \[\[5, 6\], \[7, 8\]\],  
        entonces A + B = \[\[1+5, 2+6\], \[3+7, 4+8\]\] = \[\[6, 8\], \[10, 12\]\].
        """)
    elif operacion == "Resta":
        st.markdown("""
        ### Resta de Matrices
        Se restan los elementos correspondientes de cada matriz.

        **Ejemplo:**  
        Si A = \[\[5, 6\], \[7, 8\]\] y B = \[\[1, 2\], \[3, 4\]\],  
        entonces A - B = \[\[5-1, 6-2\], \[7-3, 8-4\]\] = \[\[4, 4\], \[4, 4\]\].
        """)
    elif operacion == "Multiplicación":
        st.markdown("""
        ### Multiplicación de Matrices
        Se multiplica cada fila de la primera matriz por cada columna de la segunda.

        **Ejemplo:**  
        Si A = \[\[1, 2\], \[3, 4\]\] y B = \[\[5, 6\], \[7, 8\]\],  
        entonces el resultado se obtiene sumando los productos:  
        A × B = \[\[1×5 + 2×7, 1×6 + 2×8\], \[3×5 + 4×7, 3×6 + 4×8\]\].
        """)

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
