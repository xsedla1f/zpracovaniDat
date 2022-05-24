# Zpracování datových sad
***
Účelem tohoto projektu je zpracování datových sad pro jejich následné užití
při trénování modelu neuronové sítě Google BERT.

Ve složce /logs se nachází celkem 20 souborů s logy událostí, každý z jiného zdroje (viz název)

Postup zpracování dat je následující:
* načtení zdrojových souborů ve formátu .txt a .log do proměnných (každý soubor obsahuje 2000 záznamů);
* vytvoření souborů .csv s hlavičkou ['labels', 'log'];
* vyplnění .csv souborů příslušnými daty podle identifikátoru 'labels';
* rozdělení .csv souborů na tři části (ve výchozím stavu je poměr 1200:400:400);
* sloučení do finálních datových sad (train, validate, test v poměru 24000:8000:8000);
* náhodné promíchání finálních datových sad.