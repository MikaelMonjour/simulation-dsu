#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np

choix_commune = input("Tu veux calculer la dotation 2019 pour quelle ville ? : ")
departement = input("Numero du département à deux chiffre ex 67 : ")
print("[+] Calcul pour une commune de plus de 10 000 habitants")

df = pd.read_csv("2019-communes-criteres-repartition.csv", decimal=",")
_nombre_de_villes_elligibles = len(
    df["RANG_DSU_SUP_10K"].replace(0, np.nan).dropna()
) * (
    2 / 3
)  # Les deux tiers de 1032

# Selection des colonnes
df2 = df[
    [
        "Informations générales - Nom de la commune",
        "Informations générales - Population DGF Année N'",
        "Informations générales - Population INSEE Année N ",
        "Informations générales - Code département de la commune",
        "Dotation de solidarité urbaine - Nombre de bénéficiaires des aides au logement de la commune",
        "Dotation de solidarité urbaine - Nombre de logements TH de la commune",
        "Dotation de solidarité urbaine - Part des bénéficiaires d'aides au logement par rapport au nombre de logements des communes mét de plus de 10000 habitants",
        "Dotation de solidarité urbaine - Nombre de logements sociaux de la commune",
        "Dotation de solidarité urbaine - Part des logements sociaux dans le total des logements des communes métropolitaines de plus de 10000 habitants",
        "Dotation de solidarité urbaine - Revenu imposable moyen par habitant des communes mét de plus de 10 000 habitants",
        "Dotation de solidarité urbaine - Revenu imposable par habitant",
        "Dotation de solidarité urbaine - Potentiel financier moyen par habitant des communes métropolitaines de plus de 10000 habitants",
        "Potentiel fiscal et financier des communes - Potentiel financier par habitant",
        "EFFORT_FISCAL",  # Changer nom de colonne en production
        "RANG_DSU_SUP_10K",  # Changer nom de colonne en production
        "RANG_DSU_5K_A_10K",  # Changer nom de colonne en production
        "Dotation de solidarité urbaine - Montant attribution spontanée DSU",
    ]
]

dfcity = df.loc[
    (df["Informations générales - Nom de la commune"] == choix_commune)
    & (
        df["Informations générales - Code département de la commune"]
        == int(departement)
    )
]

if len(dfcity) == 0:
    print(
        f"[!] Il n'existe pas de commune {choix_commune} dans le {departement} - > Arrêt du programme !"
    )
else:
    population_dgf_commune = dfcity[
        "Informations générales - Population DGF Année N'"
    ].values[0]
    population_insee_commune = dfcity[
        "Informations générales - Population INSEE Année N "
    ].values[0]
    beneficiaires_aide_au_logement_commune = dfcity[
        "Dotation de solidarité urbaine - Nombre de bénéficiaires des aides au logement de la commune"
    ].values[0]
    leffort_fiscal = dfcity["EFFORT_FISCAL"].values[0]

    dsu_annee_precedente = dfcity[
        "Dotation de solidarité urbaine - Montant attribution spontanée DSU"
    ].values[0]

    print(f"[+] {population_insee_commune}")
    if population_insee_commune > 10000:
        rang = dfcity["RANG_DSU_SUP_10K"].values[0]

        _pfi_reference_10000 = 1292.66  # Potentiel Financier de référence au niveau national communes > 10K
        pfi_commune = dfcity[
            "Potentiel fiscal et financier des communes - Potentiel financier par habitant"
        ].values[
            0
        ]  # Potentiel financier de la commune pour laquelle on calcule la dotation
        ecart_potentiel_financier_par_hab = _pfi_reference_10000 / pfi_commune

        _ri_reference_10000 = (
            15396.50  # Le revenu imposable par habitant commune plus de 10K hab
        )
        ri_commune = dfcity[
            "Dotation de solidarité urbaine - Revenu imposable par habitant"
        ].values[
            0
        ]  # Le revenu imposable par habitant de la commune
        ecart_revenu_imposable_par_hab = _ri_reference_10000 / ri_commune

        _part_des_logement_sociaux_plus_de_10000 = 0.232031
        part_des_logement_sociaux_de_la_commune = (
            dfcity[
                "Dotation de solidarité urbaine - Nombre de logements sociaux de la commune"
            ].values[0]
            / dfcity[
                "Dotation de solidarité urbaine - Nombre de logements TH de la commune"
            ].values[0]
        )
        ecart_de_pourcentage_de_logements_sociaux = (
            part_des_logement_sociaux_de_la_commune
            / _part_des_logement_sociaux_plus_de_10000
        )

        _part_des_allocations_logements_plus_de_10000 = 0.515391
        part_des_allocations_logements_commune = (
            dfcity[
                "Dotation de solidarité urbaine - Nombre de bénéficiaires des aides au logement de la commune"
            ].values[0]
            / dfcity[
                "Dotation de solidarité urbaine - Nombre de logements TH de la commune"
            ].values[0]
        )
        ecart_de_pourcentage_allocation_logement = (
            part_des_allocations_logements_commune
            / _part_des_allocations_logements_plus_de_10000
        )

        ponderation_potentiel_financier = 0.30  # Possibilité de changé via amendement
        ponderation_revenu_imposable = 0.25
        ponderation_logement_sociaux = 0.15
        ponderation_allocation_logement = 0.30

        c1 = ecart_potentiel_financier_par_hab * ponderation_potentiel_financier
        c2 = ecart_revenu_imposable_par_hab * ponderation_revenu_imposable
        c3 = ecart_de_pourcentage_de_logements_sociaux * ponderation_logement_sociaux
        c4 = ecart_de_pourcentage_allocation_logement * ponderation_allocation_logement

        indice_synthetique = c1 + c2 + c3 + c4

        rang_de_la_commune = rang  # Par rapport à l'indice synthétique RENNES (diiférent en fonction de la commune)
        numerateur_coeff_rang = (
            (3.5 * rang_de_la_commune) + 0.5 - (4 * _nombre_de_villes_elligibles)
        )
        denominateur_coeff_rang = 1 - _nombre_de_villes_elligibles

        coefficient_de_rang = numerateur_coeff_rang / denominateur_coeff_rang

        population_insee_de_la_commune = population_insee_commune
        population_qpv_de_la_commune = beneficiaires_aide_au_logement_commune
        coefficient_qpv = 1 + 2 * (
            population_qpv_de_la_commune / population_insee_de_la_commune
        )

        # ESsayer de retouver le calcul de la valeur de point
        _valeur_de_point = (
            0.57362212  # Modification en fonction des critères de dessus (POUR 2019)
        )
        population_dgf = population_dgf_commune  # Dans fichier DGCL
        effort_fiscal_de_la_commune = (
            leffort_fiscal if leffort_fiscal < 1.3 else 1.3
        )  # Dans fichier DGCL - Plafond de 1.3

        montant_abondement = (
            indice_synthetique
            * population_dgf
            * effort_fiscal_de_la_commune
            * coefficient_de_rang
            * coefficient_qpv
            * _valeur_de_point
        )

        DSU2019 = dsu_annee_precedente + montant_abondement
        print(f"DSU 2019 : {DSU2019}")
        df = pd.DataFrame(
            {"": [montant_abondement, dsu_annee_precedente]},
            index=["Abondement", "DSU N-1"],
        )
        plot = df.plot.pie(y="", title="TOTAL DSU", figsize=(10, 6))
        fig = plot.get_figure()
        fig.savefig("figure.png", dpi=300)

    elif population_insee_commune > 5000 and population_insee_commune < 10000:
        rang = dfcity["RANG_DSU_5K_A_10K"].values[0]
        print("Ville de 5K Habitants")
    else:
        print("Moins de 5 000 habitants")
