#!/usr/bin/env python
# coding: utf-8


# ### TRANCHE HAUTE

import pandas as pd
df = pd.read_csv("2019-communes-criteres-repartition.csv", decimal=",")
icc = df["Informations générales - Code INSEE de la commune"]
to_remove = df.loc[icc.astype(str).str.match(pat = '9[7-9].+')].index
after_removal = df.drop(to_remove)


choix_nombre_habitant_tranche_haute = int(input("Choix du nombre d'habitants : "))
df2 = after_removal.loc[after_removal["Informations générales - Population DGF Année N'"] > choix_nombre_habitant_tranche_haute]

po = df2["Potentiel fiscal et financier des communes - Potentiel financier"].sum()
pe =  df2["Informations générales - Population DGF Année N'"].sum()
potentiel_financier_moyen = po / pe

df2["potentiel_financier"] = potentiel_financier_moyen / df2["Potentiel fiscal et financier des communes - Potentiel financier par habitant"]

ksc = df2["Dotation de solidarité urbaine - Nombre de logements sociaux de la commune"].sum()
kth = df2["Dotation de solidarité urbaine - Nombre de logements TH de la commune"].sum()

b = ksc / kth

a = df2["Dotation de solidarité urbaine - Nombre de logements sociaux de la commune"] / df2["Dotation de solidarité urbaine - Nombre de logements TH de la commune"]

df2["logements_sociaux"] = a / b

va = df2["Dotation de solidarité urbaine - Nombre de bénéficiaires des aides au logement de la commune"] / df2["Dotation de solidarité urbaine - Nombre de logements TH de la commune"]

vadb = df2["Dotation de solidarité urbaine - Nombre de bénéficiaires des aides au logement de la commune"].sum() / df2["Dotation de solidarité urbaine - Nombre de logements TH de la commune"].sum()

df2["allocation_logement"] = va / vadb

hu = df2["Dotation de solidarité urbaine - Revenu imposable des habitants de la commune"].sum() / df2["Informations générales - Population INSEE Année N "].sum()

df2["revenu_imposable"] = hu / df2["Dotation de solidarité urbaine - Revenu imposable par habitant"]

#INDICE SYNTHETIQUE

ponderation_potentiel_financier = 0.30
ponderation_logement_sociaux = 0.15
ponderation_revenu_imposable = 0.25
ponderation_allocation_logement = 0.30

ecart_potentiel_financier_par_hab = df2["potentiel_financier"]
ecart_revenu_imposable_par_hab = df2["revenu_imposable"]
ecart_de_pourcentage_de_logements_sociaux = df2["logements_sociaux"]
ecart_de_pourcentage_allocation_logement = df2["allocation_logement"]

c1 = ecart_potentiel_financier_par_hab * ponderation_potentiel_financier
c2 = ecart_revenu_imposable_par_hab * ponderation_revenu_imposable
c3 = ecart_de_pourcentage_de_logements_sociaux * ponderation_logement_sociaux
c4 = ecart_de_pourcentage_allocation_logement * ponderation_allocation_logement

indice_synthetique = c1 + c2 + c3 + c4

df2["indice_synthetique"] = indice_synthetique

villes_maximum_haute = 2/3

tri_et_ordre = df2.nlargest(round(villes_maximum_haute * len(df2) + 0.5) , columns='indice_synthetique')

taux_potentiel_financier = 2.5
communes_hautes_eligibles = tri_et_ordre.loc[tri_et_ordre["Potentiel fiscal et financier des communes - Potentiel financier par habitant"] < taux_potentiel_financier * tri_et_ordre["Potentiel fiscal et financier des communes - Potentiel financier moyen de la strate"]]

for code_insee, commune in zip(communes_hautes_eligibles["Informations générales - Code INSEE de la commune"], communes_hautes_eligibles["Informations générales - Nom de la commune"]) :
    print(f"Code INSEE {code_insee}, Nom de la commune :{commune}")