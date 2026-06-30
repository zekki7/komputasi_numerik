import numpy as np

def divided_difference_table(x, y):
    """
    Menghitung tabel divided difference Newton.
    x, y: list/array titik data
    Return: matriks segitiga (n x n) berisi koefisien divided difference.
            Baris ke-i, kolom ke-0 adalah y[i] (f(x_i)).
            Koefisien polinomial Newton = diagonal atas: table[0][0], table[0][1], ..., table[0][n-1]
    """
    n = len(x)
    table = np.zeros((n, n))
    table[:, 0] = y

    for j in range(1, n):
        for i in range(n - j):
            table[i][j] = (table[i + 1][j - 1] - table[i][j - 1]) / (x[i + j] - x[i])

    return table


def newton_coefficients(table):
    """Mengambil koefisien polinomial Newton dari diagonal atas tabel divided difference."""
    n = table.shape[0]
    return [table[0][j] for j in range(n)]


def newton_interpolate(x_data, coeffs, x_eval):
    """
    Evaluasi polinomial Newton di titik x_eval.
    P(x) = c0 + c1(x-x0) + c2(x-x0)(x-x1) + ...
    """
    n = len(coeffs)
    result = coeffs[0]
    product_term = 1.0

    for i in range(1, n):
        product_term *= (x_eval - x_data[i - 1])
        result += coeffs[i] * product_term

    return result


def newton_polynomial_string(x_data, coeffs, decimals=4):
    """Membuat representasi string polinomial Newton untuk ditampilkan ke user."""
    terms = [f"{coeffs[0]:.{decimals}f}"]
    product_str = ""

    for i in range(1, len(coeffs)):
        product_str += f"(x - {x_data[i-1]:.{decimals}f})"
        c = coeffs[i]
        sign = "+" if c >= 0 else "-"
        terms.append(f" {sign} {abs(c):.{decimals}f}{product_str}")

    return "P(x) = " + "".join(terms)


def newton_curve(x_data, coeffs, num_points=200):
    """Menghasilkan titik-titik (x,y) sepanjang rentang data untuk plotting kurva."""
    x_min, x_max = min(x_data), max(x_data)
    xs = np.linspace(x_min, x_max, num_points)
    ys = [newton_interpolate(x_data, coeffs, xv) for xv in xs]
    return xs, ys
