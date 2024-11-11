import math


class Erddruck:
    """Berechnet die Erddruckordinate in abhängigkeit von der Wichte des Bodens,
    der Höhe der Wand und dem dimensionslosen Erddruckbeiwert"""

    def __init__(self, gamma_k, h, K):
        self.gamma_k = gamma_k  # [kN/m³] Wichte des Bodens
        self.h = h  # [m] betrachtete Stelle
        self.K = K  # [-] dimensionsloser Erddruckbeiwert
        self.e_g = self.berechne_e_g()  # [kN/m^2] Erddruckordiante

    def berechne_e_g(self):
        """
        Berechnet die Erddruckordiante e_g.

        :return: Die berechnete Erddruckordiante e_g_a.
        """
        self.e_g = self.gamma_k * self.h * self.K
        return self.e_g


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


class Erddruckkraft:
    """Berechnet die Erddruckkraft E^a_g. Sie kann in eine horizontale
    komponente E^g_ah und eine vertikale Komponente E^h_av zerlegt werden."""
    def __init__(self, e_g_a, alpha, delta_a):
        self.e_g_a = e_g_a  # [kN/m] Erddruckkraft
        self.alpha = alpha  # [°] Neigungswinkel der Wand   
        self.delta_a = delta_a  # [°] Wandreibungswinkel
        self.e_g_ah = self.berechne_e_g_ah()    # [kN/m] horizontale Komponente der Erddruckkraft
        self.e_g_av = self.berechne_e_g_av()    # [kN/m] vertikale Komponente der Erddruckkraft

    def berechne_e_g_ah(self):
        """
        Berechnet die horizontale Komponente der Erddruckkraft E^g_ah.
        """

        # Umrechnung von Grad in Bogenmaß
        self.alpha_rad = math.radians(self.alpha)
        self.delta_a_rad = math.radians(self.delta_a)

        self.e_g_ah = self.e_g_a * math.cos(self.alpha_rad + self.delta_a_rad)
        return self.e_g_ah
    
    def berechne_e_g_av(self):
        """
        Berechnet die vertikale Komponente der Erddruckkraft E^g_av.
        """

        # Umrechnung von Grad in Bogenmaß
        self.alpha_rad = math.radians(self.alpha)
        self.delta_a_rad = math.radians(self.delta_a)

        self.e_g_av = self.e_g_a * math.sin(self.alpha_rad + self.delta_a_rad)
        return self.e_g_av