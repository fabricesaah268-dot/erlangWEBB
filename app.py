from flask import Flask, render_template, request
from erlang_calculator import ErlangCalculator

app = Flask(__name__)

@app.route("/")
def index():
    # Valeurs par défaut
    return render_template(
        "index.html",
        result_channels=None,
        result_loss=None,
        result_traffic=None,
        N="",
        Pr="",
        A="",
        target_Pr=""
    )

@app.route("/channels", methods=["POST"])
def channels():
    result_channels = None
    A = ""
    target_Pr = ""
    if request.method == "POST":
        try:
            A = float(request.form["A"])
            target_Pr = float(request.form["target_Pr"])
            N = ErlangCalculator.erlang_b_inverse(A, target_Pr)
            result_channels = f"Nombre de canaux requis : {N}"
        except Exception as e:
            result_channels = f"Erreur : {e}"
    return render_template(
        "index.html",
        result_channels=result_channels,
        result_loss=None,
        result_traffic=None,
        A=A,
        target_Pr=target_Pr,
        N="",
        Pr=""
    )

@app.route("/blocking", methods=["POST"])
def blocking():
    result_loss = None
    N = ""
    A = ""
    if request.method == "POST":
        try:
            N = int(request.form["N"])
            A = float(request.form["A"])
            Pr = ErlangCalculator.erlang_b(N, A)
            result_loss = f"Probabilité de blocage : {Pr:.6f}"
        except Exception as e:
            result_loss = f"Erreur : {e}"
    return render_template(
        "index.html",
        result_channels=None,
        result_loss=result_loss,
        result_traffic=None,
        N=N,
        A=A,
        Pr="",
        target_Pr=""
    )

@app.route("/traffic", methods=["POST"])
def traffic():
    result_traffic = None
    N = ""
    Pr = ""
    if request.method == "POST":
        try:
            N = int(request.form["N"])
            Pr = float(request.form["Pr"])
            A = ErlangCalculator.erlang_a_from_pr(N, Pr)
            result_traffic = f"Trafic A : {A:.2f} Erlangs"
        except Exception as e:
            result_traffic = f"Erreur : {e}"
    return render_template(
        "index.html",
        result_channels=None,
        result_loss=None,
        result_traffic=result_traffic,
        N=N,
        Pr=Pr,
        A="",
        target_Pr=""
    )

if __name__ == "__main__":
    app.run(debug=True)
