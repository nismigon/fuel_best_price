# Fuel best price founder

The aim of this application is to found the best price for a selected fuel in a certain range.

In order to achieve this goal, this application get the open source data from french government and parse it.

Requirements: You need to install Python 3 on your computer.

Example of usage :

```sh
python main.py configuration.json 48.858370 2.294481 SP95 10
```

Exemple of return :

```txt
Downloading and extracting file
Loading data
Filter by the distance
Sorting by price
Top 1 : prix = 1.710, position : 38 avenue Henri Barbusse (92700)
Top 2 : prix = 1.790, position : Avenue de la Libération. Immeuble Santa Maria (20600)
Top 3 : prix = 2.077, position : 10 Rue Westermeyer (94200)
Top 4 : prix = 2.099, position : 1 Boulevard de la Chapelle (75010)
Top 5 : prix = 2.107, position : 55 Rue de la Commune de Paris (93300)
Top 6 : prix = 2.159, position : 18 Boulevard de la République (92420)
Top 7 : prix = 2.190, position : 16 Avenue André Morizet (92100)
Top 8 : prix = 2.199, position : 192 Avenue Louis Roche (92230)
Top 9 : prix = 2.236, position : 89 AV A. BRIAND (94110)
Top 10 : prix = 2.250, position : 164 Boulevard Haussmann (75008)
Top 11 : prix = 2.289, position : 4 AVENUE FOCH (75016)
Top 12 : prix = 2.300, position : 175 Avenue Ledru-Rollin (75011)
Top 13 : prix = 2.390, position : 23 Boulevard Victor Hugo (93400)
Top 14 : prix = 2.390, position : 8,10,10bis Rue Bailleul (75001)
Top 15 : prix = 2.670, position : 253 Boulevard Raspail (75014)
Top 16 : prix = 2.690, position : 69 Avenue Kléber (75116)
Top 17 : prix = 2.740, position : 15 Avenue Duquesne (75007)
```

Generalization :

```sh
pythin main.py <configuration_file> <latitude> <longitude> <fuel> <range>
```
