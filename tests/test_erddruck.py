import sys
import os
import unittest
import math

# Fügen Sie das grundbau-Verzeichnis zum Python-Pfad hinzu
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "grundbau"))
)

from erddruck import (
    AktiverErddruckbeiwert,
    Erddruck,
    Erddruckkraft,
    Gleitflächenwinkel,
    ErddruckAuflastUnbegrenzt,
    ErddruckVerlauf,
)


class TestAktiverErddruckbeiwert(unittest.TestCase):

    def test_berechne_K_a_g(self):
        """
        Mit Hilfe des Testfalls wurde die Berechnung des
        aktiven Erddruckbeiwerts implementiert. Die einzelnen Terme werden
        getestet, um Fehler bei der Implementierung schneller zu finden.

        Aus "Grundbau in Beispielen Teil 1, Beispiel 6.14, S. 240."
        """
        objekt_1 = AktiverErddruckbeiwert(35, 10, 20, (2 / 3) * 35)

        # Erwarteter Wert des aktiven Erddruckbeiwerts
        expected_K_a_g = 0.44
        # Erwarteter Wert des Winkels delta_a
        expected_delta_a = 23.33
        # Ergebnisse der einzelnen Terme per Hand berechnet
        expected_cos_phi_k_minus_alpha_hoch = 0.82
        expected_cos_alpha_hoch = 0.97
        expected_cos_alpha_plus_delta_a = 0.84
        exp_sin_phi_k_plus_delta_a = 0.85
        exp_sin_phi_k_minus_beta = 0.26
        exp_cos_alpha_minus_beta = 0.98

        self.assertAlmostEqual(objekt_1.K_a_g, expected_K_a_g, 2)
        self.assertAlmostEqual(objekt_1.delta_a, expected_delta_a, 2)
        self.assertAlmostEqual(
            objekt_1.cos_phi_k_minus_alpha_hoch, expected_cos_phi_k_minus_alpha_hoch, 2
        )
        self.assertAlmostEqual(objekt_1.cos_alpha_hoch, expected_cos_alpha_hoch, 2)
        self.assertAlmostEqual(
            objekt_1.cos_alpha_plus_delta_a, expected_cos_alpha_plus_delta_a, 2
        )
        self.assertAlmostEqual(
            objekt_1.sin_phi_k_plus_delta_a, exp_sin_phi_k_plus_delta_a, 2
        )
        self.assertAlmostEqual(
            objekt_1.sin_phi_k_minus_beta, exp_sin_phi_k_minus_beta, 2
        )
        self.assertAlmostEqual(
            objekt_1.cos_alpha_minus_beta, exp_cos_alpha_minus_beta, 2
        )

    def test_berechne_K_a_g_2(self):
        """
        Aus "Grundbau in Beispielen Teil 1, Tabelle 6.13, S. 239.
        Exemplarisch werden Werte für den aktiven Erddruckbeiwert berechnet und
        mit Tabellenwerten verglichen.
        """
        # phi_k = 15, alpha = 0, beta = 0, delta_a = 2/3*phi_k
        objekt_1 = AktiverErddruckbeiwert(15, 0, 0, (2 / 3) * 15)
        expected_K_a_g = 0.53
        self.assertAlmostEqual(objekt_1.K_a_g, expected_K_a_g, 2)

        # phi_k = 15, alpha = 0, beta = 0, delta_a = 0
        objekt_1 = AktiverErddruckbeiwert(15, 0, 0, 0)
        expected_K_a_g = 0.59
        self.assertAlmostEqual(objekt_1.K_a_g, expected_K_a_g, 2)

        # phi_k = 40, alpha = 0, beta = 0, delta_a = 2/3*phi_k
        objekt_1 = AktiverErddruckbeiwert(40, 0, 0, (2 / 3) * 40)
        expected_K_a_g = 0.20
        self.assertAlmostEqual(objekt_1.K_a_g, expected_K_a_g, 2)

        # phi_k = 40, alpha = 0, beta = 0, delta_a = 0
        objekt_1 = AktiverErddruckbeiwert(40, 0, 0, 0)
        expected_K_a_g = 0.22
        self.assertAlmostEqual(objekt_1.K_a_g, expected_K_a_g, 2)


class TestAktiverErddruck(unittest.TestCase):

    # Aus Grundbau in Beispielen Teil 1, Bsp. 6.14, S. 240
    def test_berechne_e_g_a(self):
        phi_k = 35
        alpha = 10
        beta = 20
        delta_a = 2 / 3 * phi_k
        gamma_k = 20
        h = 5

        K_g_a = AktiverErddruckbeiwert(phi_k, alpha, beta, delta_a)
        e_g_a = Erddruck(
            gamma_k,
            h,
            K_g_a.K_a_g,
        )

        expected_e_g_a = 44.0  # [kN/m²]

        self.assertAlmostEqual(e_g_a.e_g, expected_e_g_a, 1)


class TestErddruckkraft(unittest.TestCase):

    # Aus Grundbau in Beispielen Teil 1, Bsp. 6.15, S. 241
    def test_berechne_erddruckkraft(self):

        e_g_a = 110  # [kN/m] erddruckkraft
        alpha = 10  # [°]
        delta_a = 24  # [°]

        erddruckHorizontal = Erddruckkraft(e_g_a, alpha, delta_a)

        expected_erddruckkraft_horizontal = 91.2  # [kN/m]
        expected_erddruckkraft_vertikal = 61.5  # [kN/m]

        self.assertAlmostEqual(
            erddruckHorizontal.e_g_ah, expected_erddruckkraft_horizontal, 1
        )
        self.assertAlmostEqual(
            erddruckHorizontal.e_g_av, expected_erddruckkraft_vertikal, 1
        )


class TestGleitflächenwinkel(unittest.TestCase):

    # Aus Grundbau in Beispielen Teil 1, Bsp. 6.16, S. 241
    def test_berechne_gleitflächenwinkel(self):

        objekt = Gleitflächenwinkel(35, 10, 20, 23.33)

        expected_g_a = 55.8  # [°]

        self.assertAlmostEqual(objekt.g_a, expected_g_a, 1)
        print(objekt.phi_k)
        print(objekt.g_a)


class TestUnbegrenzteFlächenlast(unittest.TestCase):

    def test_berechne_ErddruckAuflastUnbegrenzt(self):
        """
        Aus "Grundbau in Beispielen Teil 1, Beispiel 6.17, S. 242.


        """

        obj_aktErdBei = AktiverErddruckbeiwert(30, 0, 0, (2 / 3) * 30)
        obj_Erddruck = Erddruck(18, 5, 0.3)
        obj_ErddruckAuflastUnbegrenzt = ErddruckAuflastUnbegrenzt(30, 0.3, 5, 20)

        expected_K_a_g = 0.3
        expected_e_g_a = 27
        excepted_e_g_p = 9

        self.assertAlmostEqual(obj_aktErdBei.K_a_g, expected_K_a_g, 1)
        self.assertAlmostEqual(obj_Erddruck.e_g, expected_e_g_a, 0)
        self.assertAlmostEqual(obj_ErddruckAuflastUnbegrenzt.e_g_p, excepted_e_g_p, 0)
        print(obj_aktErdBei.K_a_g)
        print(obj_Erddruck.e_g)
        print(obj_ErddruckAuflastUnbegrenzt.e_g_p)
        print(obj_ErddruckAuflastUnbegrenzt.h_koordinaten)
        print(obj_ErddruckAuflastUnbegrenzt.y_koordinaten)


class TestErddruckVerlauf(unittest.TestCase):

    # Aus Grundbau in Beispielen Teil 1, Bsp. 6.15, S. 241
    def test_berechne_erddruckverlauf(self):

        obj_erddruckVerlauf = ErddruckVerlauf(20, 5, 50, 0.44)

        excepted_e_g_ = 44.0  # [kN/m²]

        self.assertAlmostEqual(obj_erddruckVerlauf.e_g, excepted_e_g_, 1)

        print(obj_erddruckVerlauf.h_koordinaten)
        print(obj_erddruckVerlauf.y_koordinaten)


if __name__ == "__main__":
    unittest.main()

# run the test
# python -m unittest tests.test_erddruck
