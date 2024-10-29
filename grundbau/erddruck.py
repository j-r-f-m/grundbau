import math


class Erddruck:
    """Berechnet die Erddruckordinate in abhängigkeit von der Wichte des Bodens,
    der Höhe der Wand und dem dimensionslosen Erddruckbeiwert"""

    def __init__(self, gamma_k, h, K_a_g):
        self.gamma_k = gamma_k  # [-]
        self.h = h  # [m]
        self.K_a_g = K_a_g  # [-]
        # Erddruckordiante
        self.e_g_a = self.berechne_e_g_h()  # [kN/m^2]

    def berechne_e_g_h(self):
        """
        Berechnet die Erddruckordiante e_g_a.

        :return: Die berechnete Erddruckordiante e_g_a.
        """
        self.e_g_a = self.gamma_k * self.h * self.K_a_g
        return self.e_g_a


class AktiverErddruckbeiwert:
    def __init__(self, phi_k, alpha, beta, delta_a):
        """
        Initialisiert die BerechneKAG-Klasse mit den gegebenen Winkeln in Grad.

        :param phi_k: Winkel phi_k in Grad
        :param alpha: Winkel alpha in Grad
        :param beta: Winkel beta in Grad
        """
        self.phi_k = phi_k  # [°]
        self.alpha = alpha  # [°]
        self.beta = beta  # [°]
        self.delta_a = delta_a  # [°]
        self.K_a_g = self.berechne_K_a_g()  # [-]

    def berechne_K_a_g(self):
        """
        Berechnet den Wert von K_a^g basierend auf den gegebenen Winkeln.

        :return: Der berechnete Wert von K_a^g
        """

        # Umrechnung von Grad in Bogenmaß
        self.phi_k_rad = math.radians(self.phi_k)
        self.alpha_rad = math.radians(self.alpha)
        self.delta_a_rad = math.radians(self.delta_a)
        self.beta_rad = math.radians(self.beta)

        # Berechnung der einzelnen Komponenten
        self.cos_phi_k_minus_alpha_hoch = math.cos(self.phi_k_rad - self.alpha_rad) ** 2
        self.cos_alpha_hoch = math.cos(self.alpha_rad) ** 2
        self.cos_alpha_plus_delta_a = math.cos(self.alpha_rad + self.delta_a_rad)
        self.sin_phi_k_plus_delta_a = math.sin(self.phi_k_rad + self.delta_a_rad)
        self.sin_phi_k_minus_beta = math.sin(self.phi_k_rad - self.beta_rad)
        self.cos_alpha_minus_beta = math.cos(self.alpha_rad - self.beta_rad)

        # Berechnung des Bruchs innerhalb der Wurzel
        self.bruch_in_wurzel = (
            self.sin_phi_k_plus_delta_a * self.sin_phi_k_minus_beta
        ) / (self.cos_alpha_plus_delta_a * self.cos_alpha_minus_beta)

        # Berechnung der Wurzel
        self.wurzel = math.sqrt(self.bruch_in_wurzel)

        # Berechnung des gesamten Ausdrucks
        self.K_a_g = self.cos_phi_k_minus_alpha_hoch / (
            self.cos_alpha_hoch * self.cos_alpha_plus_delta_a * (1 + self.wurzel) ** 2
        )

        return self.K_a_g
