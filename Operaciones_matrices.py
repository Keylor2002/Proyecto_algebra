import streamlit as st
import pandas as pd
from sympy import symbols, Matrix, simplify, sympify

# --- Introducción sobre matrices ---
def mostrar_introduccion():
    # Muestra una explicación inicial sobre las matrices y sus usos
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
        - **Multiplicación**: Se obtiene multiplicando filas de la primera matriz por columnas de la segunda, asegurando 
            que el número de columnas de la primera matriz sea igual al número de filas de la segunda matriz.

        A continuación, podrás realizar estas operaciones ingresando matrices con números, fracciones o letras. 🚀
    """)

# --- Funciones para manejar matrices ---
def ingresar_matriz(filas, columnas, matriz_nombre):
    """Crea una interfaz de ingreso de datos en formato matricial."""
    matriz = []
    # Recorre el número de filas
    for i in range(filas):
        fila = []
        cols = st.columns(columnas)  # Crea columnas para los valores de la matriz
        # Recorre el número de columnas
        for j in range(columnas):
            # Permite ingresar el valor de cada celda como texto
            valor = cols[j].text_input(f"({i+1},{j+1})", value="0", key=f"{matriz_nombre}_cell_{i}_{j}")
            try:
                # Si el valor puede ser convertido a número o fracción, lo hace
                fila.append(sympify(valor))
            except:
                # Si no, lo trata como una letra (símbolo algebraico)
                fila.append(symbols(valor))
        matriz.append(fila)
    return matriz  # Retorna la matriz ingresada por el usuario

def realizar_operacion(A, B, operacion):
    """Realiza la operación seleccionada sobre las matrices A y B."""
    matriz_A = Matrix(A)  # Convierte la lista de listas en una matriz de SymPy
    matriz_B = Matrix(B)
    
    if operacion == "Suma":
        resultado = matriz_A + matriz_B  # Realiza la suma de matrices
    elif operacion == "Resta":
        resultado = matriz_A - matriz_B  # Realiza la resta de matrices
    elif operacion == "Multiplicación":
        resultado = matriz_A * matriz_B  # Realiza la multiplicación de matrices
    else:
        return None  # Si la operación no es válida, retorna None

    return formatear_resultado(resultado)  # Formatea el resultado para simplificar términos algebraicos

def formatear_resultado(matriz):
    """Combina los coeficientes y simplifica expresiones como 2a + 2a = 4a."""
    def combinar_coeficientes(expr):
        """Combina términos semejantes en expresiones algebraicas."""
        if expr.is_Add:  # Si la expresión es una suma
            terms = expr.as_ordered_terms()  # Obtiene los términos ordenados de la expresión
            coef_dict = {}
            for term in terms:
                if term.has(symbols('a')):  # Si el término contiene la variable 'a'
                    coef = term.coeff(symbols('a'))  # Obtiene el coeficiente de 'a'
                    coef_dict[symbols('a')] = coef_dict.get(symbols('a'), 0) + coef
                else:
                    coef_dict[term] = coef_dict.get(term, 0) + 1

            # Devuelve el nuevo término con los coeficientes combinados
            return sum([coef * var if var != 1 else coef for var, coef in coef_dict.items()])
        return expr  # Si no es una suma, retorna la expresión original

    # Aplica la combinación de coeficientes a cada elemento de la matriz
    return matriz.applyfunc(lambda x: combinar_coeficientes(x))

def matriz_a_dataframe(matriz):
    """Convierte una matriz de SymPy en DataFrame para mostrar en Streamlit."""
    # Convierte la matriz de SymPy en un DataFrame de Pandas para facilitar su visualización
    return pd.DataFrame(matriz.tolist())

def mostrar_pasos(matriz_A, matriz_B, operacion):
    """Muestra los pasos intermedios de la operación."""
    st.subheader("🔄 Pasos realizados")
    if operacion == "Suma":
        # Muestra las matrices A y B y luego el resultado de la suma
        st.write("### Paso 1: Sumar las matrices A y B")
        st.write("Matriz A:")
        st.dataframe(matriz_a_dataframe(matriz_A))
        st.write("Matriz B:")
        st.dataframe(matriz_a_dataframe(matriz_B))
        st.write("Resultado de A + B:")
        resultado = matriz_A + matriz_B
        st.dataframe(matriz_a_dataframe(resultado))
        
    elif operacion == "Resta":
        # Muestra las matrices A y B y luego el resultado de la resta
        st.write("### Paso 1: Restar las matrices A y B")
        st.write("Matriz A:")
        st.dataframe(matriz_a_dataframe(matriz_A))
        st.write("Matriz B:")
        st.dataframe(matriz_a_dataframe(matriz_B))
        st.write("Resultado de A - B:")
        resultado = matriz_A - matriz_B
        st.dataframe(matriz_a_dataframe(resultado))
        
    elif operacion == "Multiplicación":
        # Muestra las matrices A y B y luego el resultado de la multiplicación
        st.write("### Paso 1: Multiplicar las matrices A y B")
        st.write("Matriz A:")
        st.dataframe(matriz_a_dataframe(matriz_A))
        st.write("Matriz B:")
        st.dataframe(matriz_a_dataframe(matriz_B))
        st.write("Resultado de A * B:")
        resultado = matriz_A * matriz_B
        st.dataframe(matriz_a_dataframe(resultado))

# --- Explicaciones por operación ---
def mostrar_explicacion_operacion(operacion):
    """Muestra la explicación de cómo realizar la operación seleccionada."""
    if operacion == "Suma":
        # Explicación de cómo sumar matrices
        st.subheader("🟢 ¿Cómo se suma una matriz?")
        st.write("""
            Para sumar dos matrices, deben tener el mismo tamaño.
            Se suman sus elementos posición por posición, como sigue:

            Matriz A:
            ```
            [ a11  a12 ]
            [ a21  a22 ]
            ```

            Matriz B:
            ```
            [ b11  b12 ]
            [ b21  b22 ]
            ```

            Resultado de A + B:
            ```
            [ a11 + b11  a12 + b12 ]
            [ a21 + b21  a22 + b22 ]
            ```
        """)
    elif operacion == "Resta":
        # Explicación de cómo restar matrices
        st.subheader("🔵 ¿Cómo se resta una matriz?")
        st.write("""
            Para restar dos matrices, deben tener el mismo tamaño.
            Se restan sus elementos posición por posición, como sigue:

            Matriz A:
            ```
            [ a11  a12 ]
            [ a21  a22 ]
            ```

            Matriz B:
            ```
            [ b11  b12 ]
            [ b21  b22 ]
            ```

            Resultado de A - B:
            ```
            [ a11 - b11  a12 - b12 ]
            [ a21 - b21  a22 - b22 ]
            ```
        """)
    elif operacion == "Multiplicación":
        # Explicación de cómo multiplicar matrices
        st.subheader("🔴 ¿Cómo se multiplican matrices?")
        st.write("""
            Para multiplicar matrices, el número de **columnas de la primera matriz** debe ser igual al número de **filas de la segunda matriz**.

            Matriz A:
            ```
            [ a11  a12 ]
            [ a21  a22 ]
            ```

            Matriz B:
            ```
            [ b11  b12 ]
            [ b21  b22 ]
            ```

            Resultado de A * B:
            ```
            [ (a11*b11 + a12*b21)  (a11*b12 + a12*b22) ]
            [ (a21*b11 + a22*b21)  (a21*b12 + a22*b22) ]
            ```
        """)

# --- Main: Streamlit Web App --- 
def main():
    # Título de la aplicación
    st.title("🧮 Calculadora de Operaciones Matriciales con Letras y Fracciones")

    # Muestra la introducción sobre matrices
    mostrar_introduccion()  

    # Selección de operación
    operacion = st.selectbox("Selecciona una operación", ["Suma", "Resta", "Multiplicación"])

    # Muestra la explicación de la operación seleccionada
    mostrar_explicacion_operacion(operacion)

    # Configuración de las dimensiones de la matriz A
    filas = st.number_input("Número de filas de la primera matriz", min_value=1, step=1, value=2)
    columnas = st.number_input("Número de columnas de la primera matriz", min_value=1, step=1, value=2)
    
    st.subheader("Matriz A")
    # Ingreso de los valores para la matriz A
    A = ingresar_matriz(filas, columnas, "A")
    
    if operacion in ["Suma", "Resta"]:
        st.subheader("Matriz B (mismo tamaño que A)")
        # Ingreso de los valores para la matriz B
        B = ingresar_matriz(filas, columnas, "B")
    else:
        # Si la operación es multiplicación, se permite que la matriz B tenga diferente número de columnas
        columnas_B = st.number_input("Número de columnas de la segunda matriz", min_value=1, step=1, value=2)
        st.subheader("Matriz B")
        B = ingresar_matriz(columnas, columnas_B, "B")
    
    # Botón para realizar el cálculo
    if st.button("Calcular"):
        try:
            # Muestra los pasos realizados antes del resultado final
            mostrar_pasos(Matrix(A), Matrix(B), operacion)
            
            # Realiza la operación final y muestra el resultado
            resultado = realizar_operacion(A, B, operacion)
            if resultado is not None:
                st.subheader("✅ Resultado Final")
                st.dataframe(matriz_a_dataframe(resultado))
            else:
                st.error("¡Error! Las matrices no son compatibles para esta operación.")
        except Exception as e:
            st.error(f"Error en el cálculo: {e}")

# Ejecuta la aplicación
if __name__ == "__main__":
    main()
