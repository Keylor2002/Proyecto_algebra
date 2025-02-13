import streamlit as st
import numpy as np

def mostrar_pasos_suma(A, B):
    pasos = "Paso a paso de la suma de matrices:\n"
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            pasos += f"({A[i, j]}) + ({B[i, j]}) = {A[i, j] + B[i, j]}\n"
    return pasos

def mostrar_pasos_resta(A, B):
    pasos = "Paso a paso de la resta de matrices:\n"
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            pasos += f"({A[i, j]}) - ({B[i, j]}) = {A[i, j] - B[i, j]}\n"
    return pasos

def mostrar_pasos_multiplicacion(A, B):
    pasos = "Paso a paso de la multiplicación de matrices:\n"
    resultado = np.dot(A, B)
    for i in range(A.shape[0]):
        for j in range(B.shape[1]):
            elementos = [f"({A[i, k]}*{B[k, j]})" for k in range(A.shape[1])]
            pasos += " + ".join(elementos) + f" = {resultado[i, j]}\n"
    return pasos

def main():
    st.title("Calculadora de Operaciones Matriciales")
    operacion = st.selectbox("Selecciona una operación", ["Suma", "Resta", "Multiplicación"])
    filas = st.number_input("Número de filas de la primera matriz", min_value=1, step=1)
    columnas = st.number_input("Número de columnas de la primera matriz", min_value=1, step=1)
    
    A_input = st.text_area("Ingresa la primera matriz (separada por espacios y saltos de línea)")
    if operacion in ["Suma", "Resta"]:
        B_input = st.text_area("Ingresa la segunda matriz (mismo tamaño que la primera)")
    else:
        columnas_B = st.number_input("Número de columnas de la segunda matriz", min_value=1, step=1)
        B_input = st.text_area("Ingresa la segunda matriz (compatible con la primera)")
    
    if st.button("Calcular"):
        try:
            A = np.array([list(map(float, row.split())) for row in A_input.strip().split("\n")])
            B = np.array([list(map(float, row.split())) for row in B_input.strip().split("\n")])
            
            if operacion == "Suma" or operacion == "Resta":
                if A.shape != B.shape:
                    st.error("Error: Las matrices deben tener las mismas dimensiones para la suma o resta.")
                    return
            elif operacion == "Multiplicación":
                if A.shape[1] != B.shape[0]:
                    st.error("Error: El número de columnas de la primera matriz debe ser igual al número de filas de la segunda matriz.")
                    return
            
            if operacion == "Suma":
                resultado = A + B
                pasos = mostrar_pasos_suma(A, B)
            elif operacion == "Resta":
                resultado = A - B
                pasos = mostrar_pasos_resta(A, B)
            elif operacion == "Multiplicación":
                resultado = np.dot(A, B)
                pasos = mostrar_pasos_multiplicacion(A, B)
            
            st.subheader("Resultado:")
            st.write(resultado)
            st.subheader("Paso a paso:")
            st.text(pasos)
        except Exception as e:
            st.error(f"Error en el cálculo: {e}")

if __name__ == "__main__":
    main()

