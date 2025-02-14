import streamlit as st
import numpy as np
import pandas as pd

# Mapa para convertir letras a números (A=0, B=1, C=2, ...)
def letra_a_numero(letra):
    if letra.isalpha():
        return ord(letra.upper()) - ord('A')
    return 0  # Si no es letra, devolver 0

# Función para convertir números a letras o mostrar coeficientes como 2A, 3B, etc.
def numero_a_letra_o_coeficiente(num, letra):
    """Convierte un número a una letra o expresión con coeficiente si es mayor a 1."""
    if num == 1:
        return letra  # Si es 1, solo devuelve la letra (A, B, C, ...)
    elif num == 0:
        return '0'  # Si es 0, devuelve 0
    else:
        return f"{num}{letra}"  # Si es mayor a 1, devuelve el coeficiente (2A, 3B, ...)

# Formatear número o letra de acuerdo al modo
def formato_numero(num, modo):
    """Formatea los números según el modo seleccionado."""
    try:
        if isinstance(num, str):
            return num  # Mantener las letras como están
        if modo == "Decimal":
            return f"{int(num)}" if num.is_integer() else f"{num:.1f}"
        elif modo == "Fracción":
            return str(num)  # Usar str directamente para simplificar
        elif modo == "Letras":
            return chr(int(num) + ord('A'))  # Convertir números a letras tipo A, B, C...
    except ValueError:
        return str(num)
    return str(num)

# Función para multiplicar matrices con letras
def multiplicar_matrices_con_letras(A, B):
    """Multiplica dos matrices con letras representadas como números, manteniendo coeficientes."""
    filas_A, cols_A = A.shape
    filas_B, cols_B = B.shape
    resultado = np.empty((filas_A, cols_B), dtype=object)
    
    for i in range(filas_A):
        for j in range(cols_B):
            # Suma de multiplicaciones y uso de coeficientes
            coeficiente = sum(letra_a_numero(str(A[i, k])) * letra_a_numero(str(B[k, j])) for k in range(cols_A))
            letra_resultado = chr(ord('A') + (coeficiente % 26))  # Asigna una letra basada en el coeficiente
            resultado[i, j] = numero_a_letra_o_coeficiente(coeficiente, letra_resultado)
    
    return resultado

# Función para mostrar los pasos de la operación
def mostrar_pasos(A, B, resultado, operacion, modo):
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

# Función para ingresar las matrices
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

# Función principal
def main():
    st.title("Calculadora de Operaciones Matriciales con Letras")
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
                resultado = multiplicar_matrices_con_letras(A, B)
                pasos = mostrar_pasos(A, B, resultado, "Multiplicación", modo_visualizacion)
            else:
                st.error("Dimensiones incorrectas para la operación.")
                return
            
            st.subheader("Resultado")
            st.dataframe(pd.DataFrame(resultado).style.applymap(lambda x: "background-color: #a0c4ff;"))
            
            st.subheader("Explicación Paso a Paso")
            st.text(pasos)
        except Exception as e:
            st.error(f"Error en el cálculo: {e}")

if __name__ == "__main__":
    main()
