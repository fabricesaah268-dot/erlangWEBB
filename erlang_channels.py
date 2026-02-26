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
        if N <= 0:
            return 1.0 if A > 0 else 0.0
        try:
            numerator = (A ** N) / math.factorial(N)
            denominator = sum((A ** k) / math.factorial(k) for k in range(N + 1))
            return numerator / denominator
        except (OverflowError, ValueError):
            # Sécurité : éviter les débordements
            return 1.0

    @staticmethod
    def erlang_b_inverse(A, target_Pr, max_channels=5000):
        """
        Calcule le nombre de canaux nécessaires
        A: trafic en Erlangs
        target_Pr: probabilité de perte acceptée
        """
        if A <= 0:
            return 0
        if target_Pr >= 1.0:
            return 1
        for N in range(1, max_channels + 1):
            if ErlangCalculator.erlang_b(N, A) <= target_Pr:
                return N
        return max_channels

    @staticmethod
    def erlang_a_from_pr(N, target_Pr, tol=1e-9, max_iter=200, max_A=1e6):
        """
        Calcule le trafic A (Erlangs) tel que la probabilité de perte pour N canaux
        soit égale à target_Pr. Utilise une recherche binaire.
        """
        if N <= 0:
            raise ValueError("N doit être strictement positif")
        if target_Pr <= 0:
            return 0.0
        if target_Pr >= 1.0:
            return float('inf')

        low, high = 0.0, 1.0
        while ErlangCalculator.erlang_b(N, high) < target_Pr and high < max_A:
            high *= 2.0

        if ErlangCalculator.erlang_b(N, high) < target_Pr:
            return max_A

        for _ in range(max_iter):
            mid = (low + high) / 2.0
            val = ErlangCalculator.erlang_b(N, mid)
            if abs(val - target_Pr) <= tol:
                return mid
            if val < target_Pr:
                low = mid
            else:
                high = mid

        return (low + high) / 2.0

    @staticmethod
    def calculate_loss_probability(N, A):
        """Calcule la probabilité de perte pour N canaux et A Erlangs"""
        return ErlangCalculator.erlang_b(N, A)


class ErlangGUI:
    # Ton interface Tkinter reste inchangée, avec les onglets pour :
    # - Nombre de canaux
    # - Probabilité de perte
    # - Trafic A
    # - Informations
    # Les méthodes calculate_channels, calculate_loss_prob et calculate_traffic_A
    # utilisent directement les fonctions corrigées ci-dessus.
    ...
    # (Ton code GUI est correct, donc je ne le recopie pas intégralement ici.
    # Tu peux garder ta version telle quelle et remplacer uniquement la classe ErlangCalculator.)
