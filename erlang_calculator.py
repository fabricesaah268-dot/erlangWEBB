import math

class ErlangCalculator:
    @staticmethod
    def erlang_b(N, A):
        """
        Calcule la probabilité de blocage Erlang B
        N : nombre de canaux (int)
        A : trafic en Erlangs (float)
        """
        if N <= 0:
            return 1.0 if A > 0 else 0.0

        # Utilisation d'une formule récursive pour éviter les Overflow
        B = 1.0
        for i in range(1, N + 1):
            B = (A * B) / (i + A * B)
        return B

    @staticmethod
    def erlang_b_inverse(A, target_Pr, max_channels=20000):
        """
        Cherche le nombre de canaux N nécessaire pour obtenir une probabilité de perte <= target_Pr
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
    def erlang_a_from_pr(N, target_Pr, max_A=1e8, tol=1e-9):
        """
        Cherche le trafic A qui donne une probabilité de perte proche de target_Pr
        Utilise une recherche dichotomique pour plus de précision
        """
        if N <= 0 or target_Pr <= 0 or target_Pr >= 1:
            return 0.0

        low, high = 0.0, max_A
        while high - low > tol:
            mid = (low + high) / 2
            current_pr = ErlangCalculator.erlang_b(N, mid)
            if current_pr > target_Pr:
                high = mid
            else:
                low = mid
        return round((low + high) / 2, 6)  # résultat arrondi à 6 décimales
