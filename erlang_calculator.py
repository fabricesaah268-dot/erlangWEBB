import math

class ErlangCalculator:
    @staticmethod
    def erlang_b(N, A):
        if N == 0:
            return 1.0 if A > 0 else 0.0
        try:
            numerator = (A ** N) / math.factorial(N)
            denominator = sum((A ** k) / math.factorial(k) for k in range(N + 1))
            return numerator / denominator
        except (OverflowError, ValueError):
            return 1.0

    @staticmethod
    def erlang_b_inverse(A, Pr, max_channels=1000):
        if A <= 0:
            return 0
        if Pr >= 1.0:
            return 1
        for N in range(1, max_channels + 1):
            if ErlangCalculator.erlang_b(N, A) <= Pr:
                return N
        return max_channels
    @staticmethod
    def erlang_a_from_pr(N, Pr, max_traffic=1000, step=0.01):
        """
        Approximation : cherche le trafic A qui donne une probabilité de perte proche de Pr
        """
        if N <= 0 or Pr <= 0 or Pr >= 1:
            return 0.0

        A = 0.0
        while A <= max_traffic:
            current_pr = ErlangCalculator.erlang_b(N, A)
            if current_pr <= Pr:
                return A
            A += step
        return max_traffic
