import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from newton_interp import (
    divided_difference_table,
    newton_coefficients,
    newton_interpolate,
    newton_polynomial_string,
    newton_curve,
)

st.set_page_config(page_title="Newton's Divided Difference Interpolation", layout="centered")

st.title("Newton's Divided Difference Interpolation")
st.caption("Tugas Akhir Komputasi Numerik — Topik: Interpolation")

st.markdown("---")

# ----------------------------
# INPUT (simple text box, bukan tabel editable)
# ----------------------------
st.subheader("1. Input Data")

col1, col2 = st.columns(2)
with col1:
    x_input = st.text_input("Nilai x (pisahkan dengan koma)", value="1, 2, 3, 4")
with col2:
    y_input = st.text_input("Nilai y (pisahkan dengan koma)", value="1, 4, 9, 16")

x_eval = st.number_input("Nilai x yang ingin diinterpolasi", value=2.5, step=0.1, format="%.4f")

hitung = st.button("Hitung Interpolasi", type="primary", use_container_width=True)

# ----------------------------
# PARSE INPUT
# ----------------------------
def parse_numbers(text):
    try:
        return [float(v.strip()) for v in text.split(",") if v.strip() != ""]
    except ValueError:
        return None

if hitung:
    x_data = parse_numbers(x_input)
    y_data = parse_numbers(y_input)

    if x_data is None or y_data is None:
        st.error("Format input salah. Pastikan hanya berisi angka dipisahkan koma, contoh: 1, 2, 3, 4")
    elif len(x_data) != len(y_data):
        st.error(f"Jumlah nilai x ({len(x_data)}) dan y ({len(y_data)}) harus sama.")
    elif len(x_data) < 2:
        st.error("Minimal masukkan 2 titik data.")
    elif len(set(x_data)) != len(x_data):
        st.error("Nilai x tidak boleh ada yang sama (duplikat).")
    else:
        # PROCESS
        table = divided_difference_table(x_data, y_data)
        coeffs = newton_coefficients(table)
        hasil = newton_interpolate(x_data, coeffs, x_eval)
        poly_str = newton_polynomial_string(x_data, coeffs)

        st.markdown("---")
        st.subheader("2. Hasil")

        st.metric(label=f"P({x_eval})", value=f"{hasil:.6f}")

        with st.expander("Lihat tabel divided difference"):
            n = len(x_data)
            col_names = ["x", "f(x)"] + [f"Order-{j}" for j in range(1, n)]
            display_data = []
            for i in range(n):
                row = [x_data[i], table[i][0]]
                for j in range(1, n):
                    row.append(table[i][j] if i < n - j else None)
                display_data.append(row)
            table_df = pd.DataFrame(display_data, columns=col_names)
            st.dataframe(table_df.style.format(precision=4, na_rep=""), use_container_width=True, height=min(38 * (n + 1), 300))

        with st.expander("Lihat persamaan polinomial"):
            st.code(poly_str, language="text")

        st.subheader("3. Grafik")
        xs_curve, ys_curve = newton_curve(x_data, coeffs)

        fig, ax = plt.subplots(figsize=(5, 3))
        ax.plot(xs_curve, ys_curve, label="Kurva interpolasi", color="#1f77b4", linewidth=1.5)
        ax.scatter(x_data, y_data, color="red", zorder=5, s=25, label="Data asli")
        ax.scatter([x_eval], [hasil], color="green", marker="x", s=60, zorder=6, label="Titik hasil")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.legend(fontsize=8)
        ax.grid(True, linestyle="--", alpha=0.4)
        fig.tight_layout()
        st.pyplot(fig, use_container_width=False)

else:
    st.info("Masukkan data x dan y, lalu klik **Hitung Interpolasi**.")