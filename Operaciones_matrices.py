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
    """Realiza la operación seleccionada sobre las matrices A y B y devuelve el paso a paso."""
    matriz_A = Matrix(A)
    matriz_B = Matrix(B)
    pasos = []  # Para almacenar los pasos

    if operacion == "Suma":
        pasos.append(f"Paso 1: Sumar los elementos correspondientes de las matrices A y B.")
        resultado = matriz_A + matriz_B
    elif operacion == "Resta":
        pasos.append(f"Paso 1: Restar los elementos correspondientes de las matrices A y B.")
        resultado = matriz_A - matriz_B
    elif operacion == "Multiplicación":
        pasos.append(f"Paso 1: Multiplicar las filas de la matriz A por las columnas de la matriz B.")
        resultado = matriz_A * matriz_B
    else:
        return None, pasos

    # Agregar los pasos de la operación (simplificación si corresponde)
    pasos.append(f"Paso 2: Mostrar el resultado de la operación: {resultado}")
    
    return formatear_resultado(resultado), pasos

def formatear_resultado(matriz):
    """Combina los coeficientes y simplifica expresiones como 2a + 2a = 4a."""
    def combinar_coeficientes(expr):
        if expr.is_Add:
            # Si la expresión es una suma, buscamos los coeficientes
            terms = expr.as_ordered_terms()
            coef_dict = {}
            for term in terms:
                if term.has(symbols('a')):  # Si tiene la variable 'a'
                    coef = term.coeff(symbols('a'))
                    coef_dict[symbols('a')] = coef_dict.get(symbols('a'), 0) + coef
                else:
                    coef_dict[term] = coef_dict.get(term, 0) + 1

            # Devuelve el nuevo término con los coeficientes combinados
            return sum([coef * var if var != 1 else coef for var, coef in coef_dict.items()])
        return expr

    # Aplicamos la combinación de coeficientes a todo el resultado
    return matriz.applyfunc(lambda x: combinar_coeficientes(x))

def matriz_a_dataframe(matriz):
    """Convierte una matriz de SymPy en DataFrame para mostrar en Streamlit."""
    return pd.DataFrame(matriz.tolist())

# --- Explicaciones por operación ---
def mostrar_explicacion_operacion(operacion):
    if operacion == "Suma":
        st.subheader("🟢 ¿Cómo se suma una matriz?")
        st.write("""
            Para sumar dos matrices, deben tener el mismo tamaño.
            Se suman sus elementos posición por posición, como sigue:

            Matriz A:
            
[ a11  a12 ]
            [ a21  a22 ]
            
            Matriz B:
            
[ b11  b12 ]
            [ b21  b22 ]
            
            Resultado de A + B:
            
[ a11 + b11  a12 + b12 ]
            [ a21 + b21  a22 + b22 ]
        """)
    elif operacion == "Resta":
        st.subheader("🔵 ¿Cómo se resta una matriz?")
        st.write("""
            Para restar dos matrices, deben tener el mismo tamaño.
            Se restan sus elementos posición por posición, como sigue:

            Matriz A:
            
[ a11  a12 ]
            [ a21  a22 ]
            
            Matriz B:
            
[ b11  b12 ]
            [ b21  b22 ]
            
            Resultado de A - B:
            
[ a11 - b11  a12 - b12 ]
            [ a21 - b21  a22 - b22 ]
        """)
    elif operacion == "Multiplicación":
        st.subheader("🔴 ¿Cómo se multiplican matrices?")
        st.write("""
            Para multiplicar matrices, el número de **columnas de la primera matriz** debe ser igual al número de **filas de la segunda matriz**.

            Matriz A:
            
[ a11  a12 ]
            [ a21  a22 ]
            
            Matriz B:
            
[ b11  b12 ]
            [ b21  b22 ]
            
            Resultado de A * B:
            
[ (a11*b11 + a12*b21)  (a11*b12 + a12*b22) ]
            [ (a21*b11 + a22*b21)  (a21*b12 + a22*b22) ]
        """)

# --- Main: Streamlit Web App ---
def main():
    st.title("🧮 Calculadora de Operaciones Matriciales con Letras y Fracciones")

    mostrar_introduccion()  # Mostrar explicación inicial

    operacion = st.selectbox("Selecciona una operación", ["Suma", "Resta", "Multiplicación"])

    mostrar_explicacion_operacion(operacion)  # Mostrar explicación específica

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
            resultado, pasos = realizar_operacion(A, B, operacion)
            if resultado is not None:
                st.subheader("✅ Resultado")
                st.dataframe(matriz_a_dataframe(resultado))

                st.subheader("🔍 Paso a paso")
                for paso in pasos:
                    st.write(paso)
            else:
                st.error("¡Error! Las matrices no son compatibles para esta operación.")
        except Exception as e:
            st.error(f"Error en el cálculo: {e}")

if __name__ == "__main__":
    main()
