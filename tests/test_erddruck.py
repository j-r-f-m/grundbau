import sys
import os
import unittest
import math

# Fügen Sie das grundbau-Verzeichnis zum Python-Pfad hinzu
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "grundbau"))
)

from erddruck import AktiverErddruckbeiwert, Erddruck, Erddruckkraft, Gleitflächenwinkel


class TestAktiverErddruckbeiwert(unittest.TestCase):
    """Es wird der aktive Erddruckbeiwert K^g_a berechnet  sowie die Zwischenergebnisse. Aus "Grundbau in Beispielen Teil 1, Bsp. 6.14, S. 240."""

    def test_berechne_K_a_g(self):
        objekt_1 = AktiverErddruckbeiwert(35, 10, 20, (2 / 3) * 35)

        # Ergebnisse der einzelnen Terme
        expected_K_a_g = 0.44
        expected_delta_a = 23.33
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
        """Aus "Grundbau in Beispielen Teil 1, Tabelle 6.13, S. 239."""
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

    def test_berechne_gleitflächenwinkel(self):

        objekt = Gleitflächenwinkel(35, 10, 20, 23.33)
        print(objekt.phi_k)
        print(objekt.cos_phi_k_minus_alpha)


if __name__ == "__main__":
    unittest.main()

# run the test
# python -m unittest tests.test_erddruck
