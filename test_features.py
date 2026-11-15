from features import (extraire_features, extraire_features_lot, suit,
                      motif_clavier, mot_courant, plus_longue_repetition,
                      NOMS_FEATURES)


def test_suit():
    assert suit("abc") == 1
    assert suit("987") == 1
    assert suit("aba") == 0
    assert suit("9:") == 0
    assert suit("abcba") == 1
    assert suit("ab") == 0
    assert suit("") == 0


def test_motif_clavier():
    assert motif_clavier("azerty123") == 1
    assert motif_clavier("Mouad_qwerty") == 1
    assert motif_clavier("AZERTY") == 1
    assert motif_clavier("ytrewq") == 1
    assert motif_clavier("Zx9!") == 0
    assert motif_clavier("Mouad123@") == 0
    assert motif_clavier("") == 0


def test_mot_courant():
    assert mot_courant("Password1") == 1
    assert mot_courant("P@ssw0rd") == 1
    assert mot_courant("Admin2024") == 1
    assert mot_courant("Zx9!kLm") == 0
    assert mot_courant("") == 0


def test_repetition():
    assert plus_longue_repetition("aaaa") == 4
    assert plus_longue_repetition("abab") == 1
    assert plus_longue_repetition("") == 0


def test_exemple_complet():
    f = extraire_features("Mouad123@ ")
    attendu = {
        "longueur": 10, "nb_minuscules": 4, "nb_majuscules": 1,
        "nb_chiffres": 3, "nb_symboles": 2, "diversite": 4,
        "nb_uniques": 10, "ratio_uniques": 1.0, "max_repetition": 1,
        "a_une_suite": 1, "a_motif_clavier": 0, "a_mot_courant": 0,
    }
    assert f == attendu


def test_cas_limites():
    for entree in ("", None, 12345):
        f = extraire_features(entree)
        assert all(valeur == 0 for valeur in f.values())


def test_repetition_ratio():
    f = extraire_features("aaaa")
    assert f["max_repetition"] == 4
    assert f["nb_uniques"] == 1
    assert f["ratio_uniques"] == 0.25


def test_lot():
    df = extraire_features_lot(["abc", "Mouad123@ "])
    assert df.shape == (2, len(NOMS_FEATURES))
    assert list(df.columns) == NOMS_FEATURES


def test_cles_coherentes():
    assert list(extraire_features("test").keys()) == NOMS_FEATURES


if __name__ == "__main__":
    tests = [test_suit, test_motif_clavier, test_mot_courant, test_repetition,
             test_exemple_complet, test_cas_limites, test_repetition_ratio,
             test_lot, test_cles_coherentes]
    for t in tests:
        t()
        print(t.__name__, "OK")
    print("Tous les tests passent.")