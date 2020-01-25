import pandas as pd

df=pd.read_csv("Downloads/2019-communes-criteres-repartition.csv")
#df["Informations générales - Code département de la commune"]=df["Informations générales - Code département de la commune"].astype(str)

#Liste des villes de plus de 10k habitants eligibles

pop_haute = 10000 #Volume d'habitants 

dg=df[(df["Informations générales - Population DGF Année N'"]>=pop_haute)]

nb_villes_sup_pop_haute = len(dg)

dg["f1"]=dg["Dotation de solidarité urbaine - Potentiel financier moyen par habitant des communes métropolitaines de 5000 à 9999 habitants"].apply(lambda x: float(x.split()[0].replace(',', '.')))/dg["Potentiel fiscal et financier des communes - Potentiel financier par habitant"].apply(lambda x: float(x.split()[0].replace(',', '.')))
dg["f2"]=dg["Dotation de solidarité urbaine - Nombre de logements sociaux de la commune"].astype(int)/dg["Dotation de solidarité urbaine - Nombre de logements TH de la commune"].astype(int)/dg["Dotation de solidarité urbaine - Part des logements sociaux dans le total des logements des communes métropolitaines de 5000 à 9999 habitants"].apply(lambda x: float(x.split()[0].replace(',', '.')))
dg["f3"]=dg["Dotation de solidarité urbaine - Nombre de bénéficiaires des aides au logement de la commune"].astype(int)/dg["Dotation de solidarité urbaine - Nombre de logements TH de la commune"].astype(int)/dg["Dotation de solidarité urbaine - Part des bénéficiaires d'aides au logement par rapport au nombre de logements des communes mét de 5000 à 9999 habitants"].apply(lambda x: float(x.split()[0].replace(',', '.')))
dg["f4"]=dg["Dotation de solidarité urbaine - Revenu imposable moyen par habitant des communes mét de 5000 à 9999 habitants"].apply(lambda x: float(x.split()[0].replace(',', '.')))/dg["Dotation de solidarité urbaine - Revenu imposable par habitant"].apply(lambda x: float(x.split()[0].replace(',', '.')))

var1 = 0.3 # Ponderation pour la premiere variable de l'indexe synthétique
var2 = 0.15 # Ponderation pour la deuxième variable de l'indexe synthétique
var3 = 0.3 # Ponderation pour la troisième variable de l'indexe synthétique
var4 = 0.25 # Ponderation pour la quatrième variable de l'indexe synthétique

dg["Indice synthétique"]= var1 * dg["f1"]+ var2 * dg["f2"] + var3 * dg["f3"] + var4 * dg["f4"]

var5 = 2/3 #Limite des X premières villes de plus de 10k habitants, ordonnées par Indice synthétique

dg2=dg.nlargest(round(var5 * nb_villes_sup_pop_haute + 0.5) , columns='Indice synthétique')
nb_villes_avant_filtre= len(dg2) # Nombre de villes qui font parti des X premières

var6 = 2.5 # Ponderation à appliquer sur le potentiel financier des villes

dg2=dg.nlargest(round(var5 * nb_villes_sup_pop_haute + 0.5) , columns='Indice synthétique')

print(dg[dg["Informations générales - Nom de la commune"]=="RENNES"][["f1","f2","f3","f4", "Indice synthétique","rank IS"]])

print(dg.sort_values(by="Indice synthétique"))
