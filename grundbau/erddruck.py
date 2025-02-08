import math
import numpy as np


class Erddruck:
    """Berechnet die Erddruckordinate in abhängigkeit von der Wichte des Bodens,
    der Höhe der Wand und dem dimensionslosen Erddruckbeiwert"""

    def __init__(self, gamma_k: float, h: float, K: float):
        self.gamma_k = gamma_k  # [kN/m³] Wichte des Bodens
        self.h = h  # [m] betrachtete Stelle bzw. Höhe der Wand
        self.K = K  # [-] dimensionsloser Erddruckbeiwert
        self.e_g = self.berechne_e_g()  # [kN/m^2] Erddruckordiante

    def berechne_e_g(self) -> float:
        """
        Berechnet die Erddruckordiante e_g für eine gegebene Höhe

        :return: Die berechnete Erddruckordiante e_g_a.
        """
        self.e_g = self.gamma_k * self.h * self.K
        return self.e_g


class ErddruckVerlauf:
    """
    Berechnet den Erddruckverlauf für eine gegebene Höhe
    params:
    gamma_k: Wichte des Bodens
    h: betrachtete Stelle bzw. Höhe der Wand
    step: Schrtitweite
    K: dimensionsloser Erddruckbeiwert
    """

    def __init__(self, gamma_k: float, h: float, step: float, K: float):
        """
        Initialisiert die BerechneKAG-Klasse mit den gegebenen Parametern.

        :param gamma_k: Wichte des Bodens in kN/m³
        :param h: Höhe der Wand in m
        :param step: Schrittweite in m
        :param K: dimensionsloser Erddruckbeiwert
        """
        self.gamma_k = gamma_k  # [kN/m³] Wichte des Bodens
        self.h = h  # [m] betrachtete Stelle bzw. Höhe der Wand
        self.step = step  # [m] Schrtitweite
        self.K = K  # [-] dimensionsloser Erddruckbeiwert
        # self.e_g = self.berechne_e_g()  # [kN/m^2] Erddruckordiante

        self.h_koordinaten = np.linspace(
            0, self.h, self.step
        )  # [m] Höhenverlauf - y-Achse
        self.y_koordinaten = (
            self.erstelleVerlauf()
        )  # [kN/m^2] Erddruckverlauf - y-Achse

    def berechne_e_g(self, h) -> float:
        """
        Berechnet die Erddruckordiante e_g für eine gegebene Höhe

        :return: Die berechnete Erddruckordiante e_g_a.
        """
        self.e_g = self.gamma_k * h * self.K
        return self.e_g

    def erstelleVerlauf(self) -> np.ndarray:
        """
        Erstellt die Arrays für den Erddruckverlauf
        """
        vectorized_function = np.vectorize(self.berechne_e_g)
        self.y_koordinaten = vectorized_function(self.h_koordinaten)
        return self.y_koordinaten


class AktiverErddruckbeiwert:
    """
    Berechnet den aktiven Erddruckbeiwert K_a^g für eine gegebene
    Winkelkombination.
    """

    def __init__(self, phi_k: float, alpha: float, beta: float, delta_a: float):
        """
        Initialisiert die BerechneKAG-Klasse mit den gegebenen Winkeln in Grad.

        :param phi_k: Winkel phi_k in Grad
        :param alpha: Winkel alpha in Grad
        :param beta: Winkel beta in Grad
        :param delta_a: Winkel delta_a in Grad
        """
        self.phi_k = phi_k  # [°]
        self.alpha = alpha  # [°]
        self.beta = beta  # [°]
        self.delta_a = delta_a  # [°]
        self.K_a_g = self.berechne_K_a_g()  # [-]

    def berechne_K_a_g(self) -> float:
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

        # Überprüfung auf Division durch Null
        if self.cos_alpha_plus_delta_a == 0 or self.cos_alpha_minus_beta == 0:
            raise ValueError(
                "Ungültige Winkelkombination: Division durch Null möglich."
            )

        # Berechnung des Bruchs innerhalb der Wurzel
        self.bruch_in_wurzel = (
            self.sin_phi_k_plus_delta_a * self.sin_phi_k_minus_beta
        ) / (self.cos_alpha_plus_delta_a * self.cos_alpha_minus_beta)

        # Überprüfung, ob der Wurzelwert nicht negativ ist
        if self.bruch_in_wurzel < 0:
            raise ValueError("Ungültige Winkelkombination: Negativer Wurzelwert.")

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

    def __init__(self, e_g_a: float, alpha: float, delta_a: float):
        self.e_g_a = e_g_a  # [kN/m] Erddruckkraft
        self.alpha = alpha  # [°] Neigungswinkel der Wand
        self.delta_a = delta_a  # [°] Wandreibungswinkel
        self.e_g_ah = (
            self.berechne_e_g_ah()
        )  # [kN/m] horizontale Komponente der Erddruckkraft
        self.e_g_av = (
            self.berechne_e_g_av()
        )  # [kN/m] vertikale Komponente der Erddruckkraft

    def berechne_e_g_ah(self) -> float:
        """
        Berechnet die horizontale Komponente der Erddruckkraft E^g_ah.
        """

        # Umrechnung von Grad in Bogenmaß
        self.alpha_rad = math.radians(self.alpha)
        self.delta_a_rad = math.radians(self.delta_a)

        self.e_g_ah = self.e_g_a * math.cos(self.alpha_rad + self.delta_a_rad)
        return self.e_g_ah

    def berechne_e_g_av(self) -> float:
        """
        Berechnet die vertikale Komponente der Erddruckkraft E^g_av.
        """

        # Umrechnung von Grad in Bogenmaß
        self.alpha_rad = math.radians(self.alpha)
        self.delta_a_rad = math.radians(self.delta_a)

        self.e_g_av = self.e_g_a * math.sin(self.alpha_rad + self.delta_a_rad)
        return self.e_g_av


class Gleitflächenwinkel:
    def __init__(self, phi_k: float, alpha: float, beta: float, delta_a: float):
        """
        Initialisiert die Klasse mit den gegebenen Winkeln in Grad.

        :param phi_k: Winkel phi_k in Grad
        :param alpha: Winkel alpha in Grad
        :param beta: Winkel beta in Grad
        :param delta_a: Winkel delta_a in Grad
        """
        self.phi_k = phi_k
        self.alpha = alpha
        self.beta = beta
        self.delta_a = delta_a
        self.g_a = self.berechne_g_a()

    def berechne_g_a(self) -> float:
        """
        Berechnet den Wert von g_a basierend auf der gegebenen Formel.

        :return: Der berechnete Wert von g_a
        """
        # Umrechnung der Winkel von Grad in Bogenmaß
        phi_k_rad = math.radians(self.phi_k)
        alpha_rad = math.radians(self.alpha)
        beta_rad = math.radians(self.beta)
        delta_a_rad = math.radians(self.delta_a)

        # Berechnung der einzelnen Komponenten
        self.cos_phi_k_minus_alpha = math.cos(phi_k_rad - alpha_rad)
        self.sin_phi_k_minus_alpha = math.sin(phi_k_rad - alpha_rad)
        self.sin_phi_k_plus_delta_a = math.sin(phi_k_rad + delta_a_rad)
        self.sin_phi_k_minus_beta = math.sin(phi_k_rad - beta_rad)
        self.cos_alpha_minus_beta = math.cos(alpha_rad - beta_rad)
        self.cos_alpha_plus_delta_a = math.cos(alpha_rad + delta_a_rad)

        # Überprüfung auf Division durch Null
        if self.sin_phi_k_minus_beta == 0 or self.cos_alpha_plus_delta_a == 0:
            raise ValueError(
                "Ungültige Winkelkombination: Division durch Null möglich."
            )

        # Berechnung des Bruchs innerhalb der Wurzel
        bruch_in_wurzel = (self.sin_phi_k_plus_delta_a * self.cos_alpha_minus_beta) / (
            self.sin_phi_k_minus_beta * self.cos_alpha_plus_delta_a
        )

        # Überprüfung, ob der Wurzelwert nicht negativ ist
        if bruch_in_wurzel < 0:
            raise ValueError("Ungültige Winkelkombination: Negativer Wurzelwert.")

        # Berechnung der Wurzel
        wurzel = math.sqrt(bruch_in_wurzel)

        # Berechnung des gesamten Ausdrucks im Nenner
        nenner = self.sin_phi_k_minus_alpha + wurzel

        # Überprüfung auf Division durch Null
        if nenner == 0:
            raise ValueError(
                "Ungültige Winkelkombination: Division durch Null im Nenner."
            )

        # Berechnung des gesamten Bruchs
        bruch = self.cos_phi_k_minus_alpha / nenner

        # Berechnung von g_a
        g_a = self.phi_k + math.degrees(math.atan(bruch))

        return g_a


class ErddruckAuflastUnbegrenzt:
    def __init__(self, p: float, k_g: float):
        """
        Berechnet den Erddruck infolge einer unbegrenzten Fläachenlast p
        [kN/m²].

        :param p: Auflast p in kN/m²
        :param k_g: Erddruckbeiwert (aktiv, usw.)
        """
        self.p = p  # [kN/m²]
        self.k_g = k_g  # [-]
        self.e_g_p = self.berechne_e_p_a()  # [kN/m²]

    def berechne_e_p_a(self) -> float:
        """
        Berechnet den Erddruck e_g infolge einer unbegrenzten Flächenlast p.

        :return: Der berechnete Erddruck e_g
        """
        e_g_p = self.p * self.k_g
        return e_g_p
