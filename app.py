from flask import Flask, request, render_template
from erlang_calculator import ErlangCalculator

app = Flask(__name__)

@app.route("/")
def home():
    # Affiche la page sans résultats au départ
    return render_template("index.html")

# 1. Calcul du nombre de canaux (N)
@app.route("/channels", methods=["POST"])
def channels():
    try:
        A = float(request.form.get("A", 10))
        Pr = float(request.form.get("Pr", 0.01))
        N = ErlangCalculator.erlang_b_inverse(A, Pr)
        return render_template("index.html", result_channels=f"Nombre de canaux requis : {N}")
    except Exception as e:
        return render_template("index.html", result_channels=f"Erreur : {e}")

# 2. Calcul de la probabilité de perte (Pr)
@app.route("/loss", methods=["POST"])
def loss():
    try:
        A = float(request.form.get("A", 10))
        N = int(request.form.get("N", 15))
        Pr = ErlangCalculator.erlang_b(N, A)
        return render_template("index.html", result_loss=f"Probabilité de perte : {Pr:.6f} ({Pr*100:.2f}%)")
    except Exception as e:
        return render_template("index.html", result_loss=f"Erreur : {e}")

# 3. Calcul du trafic A
@app.route("/traffic", methods=["POST"])
def traffic():
    try:
        N = int(request.form.get("N", 15))
        Pr = float(request.form.get("Pr", 0.01))
        A = ErlangCalculator.erlang_a_from_pr(N, Pr)
        return render_template("index.html", result_traffic=f"Trafic A : {A:.6f} Erlangs")
    except Exception as e:
        return render_template("index.html", result_traffic=f"Erreur : {e}")

if __name__ == "__main__":
    app.run(debug=True)
