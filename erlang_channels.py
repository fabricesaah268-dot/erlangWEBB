import tkinter as tk
from tkinter import ttk, messagebox
import math

class ErlangCalculator:
    """Calcul du nombre de canaux selon la formule d'Erlang B"""
    
    @staticmethod
    def erlang_b(N, A):
        """
        Calcule la probabilité de perte Erlang B
        N: nombre de canaux
        A: trafic en Erlangs
        """
        if N == 0:
            return 1.0 if A > 0 else 0.0
        
        # Éviter les débordements de calcul
        try:
            numerator = (A ** N) / math.factorial(N)
            denominator = sum((A ** k) / math.factorial(k) for k in range(N + 1))
            return numerator / denominator
        except (OverflowError, ValueError):
            return 1.0
    
    @staticmethod
    def erlang_b_inverse(A, Pr, max_channels=1000):
        """
        Calcule le nombre de canaux nécessaires
        A: trafic en Erlangs
        Pr: probabilité de perte acceptée (Grade of Service)
        max_channels: nombre maximum de canaux à tester
        """
        if A <= 0:
            return 0
        if Pr >= 1.0:
            return 1
        
        for N in range(1, max_channels + 1):
            if ErlangCalculator.erlang_b(N, A) <= Pr:
                return N
        
        return max_channels

    @staticmethod
    def erlang_a_from_pr(N, Pr, tol=1e-9, max_iter=100, max_A=1e6):
        """
        Calcule le trafic A (Erlangs) tel que la probabilité de perte pour N canaux
        soit égale à Pr. Résout erlang_b(N, A) = Pr par recherche binaire.
        N: nombre de canaux (int)
        Pr: probabilité de perte cible (0 <= Pr < 1)
        """
        if N <= 0:
            raise ValueError("N doit être strictement positif")
        if Pr <= 0:
            return 0.0
        if Pr >= 1.0:
            return float('inf')

        # Chercher une borne supérieure suffisante
        low = 0.0
        high = 1.0
        try:
            while ErlangCalculator.erlang_b(N, high) < Pr and high < max_A:
                high *= 2.0
        except Exception:
            return max_A

        if ErlangCalculator.erlang_b(N, high) < Pr:
            return max_A

        # Recherche binaire
        for _ in range(max_iter):
            mid = (low + high) / 2.0
            val = ErlangCalculator.erlang_b(N, mid)
            if abs(val - Pr) <= tol:
                return mid
            if val < Pr:
                low = mid
            else:
                high = mid

        return (low + high) / 2.0
    
    @staticmethod
    def calculate_loss_probability(N, A):
        """Calcule la probabilité de perte pour N canaux et A Erlangs"""
        return ErlangCalculator.erlang_b(N, A)


class ErlangGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculatrice d'Erlang B - Nombre de Canaux")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
        # Configurer le style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Palette de couleurs
        self.bg = "#f5f7fb"
        self.panel = "#ffffff"
        self.accent = "#2a9df4"
        self.accent_dark = "#1673c8"
        self.text = "#222222"
        self.note = "#6b7280"
        self.button_fg = "#ffffff"

        # Appliquer styles
        style.configure('.', background=self.bg, foreground=self.text)
        style.configure('TFrame', background=self.bg)
        style.configure('TLabel', background=self.bg, foreground=self.text)
        style.configure('TLabelframe', background=self.panel, foreground=self.text)
        style.configure('TLabelframe.Label', background=self.panel, foreground=self.accent_dark)
        style.configure('TNotebook', background=self.bg)
        style.configure('TNotebook.Tab', background=self.panel, padding=[10, 6])
        style.configure('Accent.TButton', background=self.accent, foreground=self.button_fg, relief='flat')
        style.map('Accent.TButton', background=[('active', self.accent_dark)])

        # Configurer la couleur de fond principale
        try:
            self.root.configure(bg=self.bg)
        except Exception:
            pass
        
        # Frame principal
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Titre
        title_label = ttk.Label(main_frame, text="Calcul du Nombre de Canaux",
                               font=("Arial", 14, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=10)
        title_label.configure(foreground=self.accent_dark)
        
        # Onglets
        notebook = ttk.Notebook(main_frame)
        notebook.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Onglet 1: Calcul du nombre de canaux
        tab1_frame = ttk.Frame(notebook)
        notebook.add(tab1_frame, text="Nombre de Canaux")
        self.setup_tab1(tab1_frame)
        
        # Onglet 2: Calcul de la probabilité de perte
        tab2_frame = ttk.Frame(notebook)
        notebook.add(tab2_frame, text="Probabilité de Perte")
        self.setup_tab2(tab2_frame)
        
        # Onglet 3: Calcul du Trafic A
        tab4_frame = ttk.Frame(notebook)
        notebook.add(tab4_frame, text="Trafic A")
        self.setup_tab4(tab4_frame)

        # Onglet 4: Informations (placé en dernier)
        tab3_frame = ttk.Frame(notebook)
        notebook.add(tab3_frame, text="Informations")
        self.setup_tab3(tab3_frame)
    
    def setup_tab1(self, parent):
        """Configuration de l'onglet 1: Calcul du nombre de canaux"""
        frame = ttk.LabelFrame(parent, text="Paramètres", padding="10")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Trafic A
        ttk.Label(frame, text="Trafic (A) en Erlangs:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.entry_A = ttk.Entry(frame, width=20)
        self.entry_A.grid(row=0, column=1, padx=5, pady=5)
        self.entry_A.insert(0, "10")
        
        # Probabilité de perte
        ttk.Label(frame, text="Probabilité de Perte (Pr):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.entry_Pr = ttk.Entry(frame, width=20)
        self.entry_Pr.grid(row=1, column=1, padx=5, pady=5)
        self.entry_Pr.insert(0, "0.01")
        
        # Résultat
        ttk.Label(frame, text="Nombre de Canaux N:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.result_N = ttk.Label(frame, text="", font=("Arial", 12, "bold"), foreground="blue")
        self.result_N.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        self.result_N.configure(foreground=self.accent_dark)
        
        # Bouton de calcul
        ttk.Button(frame, text="Calculer", command=self.calculate_channels, style='Accent.TButton').grid(row=3, column=0, columnspan=2, pady=10)
        
        # Notes
        notes_text = "Note: Formule d'Erlang B\nPr = (A^N / N!) / Σ(A^k / k!)"
        notes_label = ttk.Label(frame, text=notes_text, font=("Arial", 9), foreground=self.note)
        notes_label.grid(row=4, column=0, columnspan=2, pady=10)
    
    def setup_tab2(self, parent):
        """Configuration de l'onglet 2: Calcul de la probabilité de perte"""
        frame = ttk.LabelFrame(parent, text="Paramètres", padding="10")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Trafic A
        ttk.Label(frame, text="Trafic (A) en Erlangs:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.entry_A2 = ttk.Entry(frame, width=20)
        self.entry_A2.grid(row=0, column=1, padx=5, pady=5)
        self.entry_A2.insert(0, "10")
        
        # Nombre de canaux
        ttk.Label(frame, text="Nombre de Canaux (N):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.entry_N = ttk.Entry(frame, width=20)
        self.entry_N.grid(row=1, column=1, padx=5, pady=5)
        self.entry_N.insert(0, "15")
        
        # Résultat
        ttk.Label(frame, text="Probabilité de Perte Pr:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.result_Pr = ttk.Label(frame, text="", font=("Arial", 12, "bold"), foreground=self.accent_dark)
        self.result_Pr.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Pourcentage
        ttk.Label(frame, text="Pourcentage (%):").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.result_Pr_percent = ttk.Label(frame, text="", font=("Arial", 12, "bold"), foreground=self.accent_dark)
        self.result_Pr_percent.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Bouton de calcul
        ttk.Button(frame, text="Calculer", command=self.calculate_loss_prob, style='Accent.TButton').grid(row=4, column=0, columnspan=2, pady=10)
    
    def setup_tab3(self, parent):
        """Configuration de l'onglet 3: Informations"""
        frame = ttk.Frame(parent, padding="15")
        frame.pack(fill=tk.BOTH, expand=True)
        
        info_text = """
FORMULE D'ERLANG B

Cette application calcule le nombre de canaux nécessaires en fonction
du trafic et de la qualité de service (Grade of Service).

PARAMÈTRES:
• A (Trafic): Intensité du trafic en Erlangs
  1 Erlang = 1 appel simultané continu
  Exemple: 10 Erlangs = 10 appels simultanés moyens

• Pr (Probabilité de Perte): Probabilité maximale d'appel perdu
  Exemple: 0.01 = 1% d'appels perdus (Grade of Service: 0.01)
  Valeurs typiques: 0.001 à 0.05

• N (Nombre de canaux): Nombre minimum de canaux requis

FORMULE:
Pr = (A^N / N!) / (Σ A^k / k!) pour k=0 à N

APPLICATIONS:
• Dimensionnement de centrales téléphoniques
• Planification de réseaux de communication
• Calcul de capacité de lignes de transmission
• Optimisation des ressources réseau
        """
        
        text_widget = tk.Text(frame, wrap=tk.WORD, height=20, width=60,
                     font=("Courier", 9), bg=self.panel, fg=self.text, relief='flat')
        text_widget.pack(fill=tk.BOTH, expand=True)
        text_widget.insert(tk.END, info_text)
        text_widget.config(state=tk.DISABLED)

    def setup_tab4(self, parent):
        """Configuration de l'onglet 4: Calcul du trafic A à partir de N et Pr"""
        frame = ttk.LabelFrame(parent, text="Paramètres", padding="10")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Nombre de canaux
        ttk.Label(frame, text="Nombre de Canaux (N):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.entry_N2 = ttk.Entry(frame, width=20)
        self.entry_N2.grid(row=0, column=1, padx=5, pady=5)
        self.entry_N2.insert(0, "15")

        # Probabilité de perte
        ttk.Label(frame, text="Probabilité de Perte (Pr):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.entry_Pr2 = ttk.Entry(frame, width=20)
        self.entry_Pr2.grid(row=1, column=1, padx=5, pady=5)
        self.entry_Pr2.insert(0, "0.01")

        # Résultat
        ttk.Label(frame, text="Trafic (A) en Erlangs:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.result_A = ttk.Label(frame, text="", font=("Arial", 12, "bold"), foreground=self.accent_dark)
        self.result_A.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)

        # Bouton de calcul
        ttk.Button(frame, text="Calculer", command=self.calculate_traffic_A, style='Accent.TButton').grid(row=3, column=0, columnspan=2, pady=10)

        notes_text = "Note: On inverse la formule d'Erlang B par recherche binaire pour trouver A"
        notes_label = ttk.Label(frame, text=notes_text, font=("Arial", 9), foreground=self.note)
        notes_label.grid(row=4, column=0, columnspan=2, pady=10)

    def calculate_traffic_A(self):
        """Calcule le trafic A pour un N et Pr donnés"""
        try:
            N = int(self.entry_N2.get())
            Pr = float(self.entry_Pr2.get())

            if N <= 0:
                messagebox.showerror("Erreur", "Le nombre de canaux doit être positif")
                return
            if Pr < 0 or Pr >= 1:
                messagebox.showerror("Erreur", "Pr doit être dans [0, 1)")
                return

            A = ErlangCalculator.erlang_a_from_pr(N, Pr)

            if A == float('inf'):
                self.result_A.config(text="Infini (Pr proche de 1)")
            else:
                self.result_A.config(text=f"{A:.6f} Erlangs")

        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer des valeurs numériques valides")
    
    def calculate_channels(self):
        """Calcule le nombre de canaux"""
        try:
            A = float(self.entry_A.get())
            Pr = float(self.entry_Pr.get())
            
            if A <= 0:
                messagebox.showerror("Erreur", "Le trafic A doit être positif")
                return
            if Pr <= 0 or Pr >= 1:
                messagebox.showerror("Erreur", "Pr doit être entre 0 et 1")
                return
            
            N = ErlangCalculator.erlang_b_inverse(A, Pr)
            self.result_N.config(text=f"{N} canaux")
            
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer des valeurs numériques valides")
    
    def calculate_loss_prob(self):
        """Calcule la probabilité de perte"""
        try:
            A = float(self.entry_A2.get())
            N = int(self.entry_N.get())
            
            if A <= 0:
                messagebox.showerror("Erreur", "Le trafic A doit être positif")
                return
            if N <= 0:
                messagebox.showerror("Erreur", "Le nombre de canaux doit être positif")
                return
            
            Pr = ErlangCalculator.erlang_b(N, A)
            Pr_percent = Pr * 100
            
            self.result_Pr.config(text=f"{Pr:.6f}")
            self.result_Pr_percent.config(text=f"{Pr_percent:.4f}%")
            
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer des valeurs numériques valides")


def main():
    root = tk.Tk()
    app = ErlangGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

