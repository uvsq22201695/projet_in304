#### (Ceci est le compte-rendu de Maël Fajon (étudiant en INTD-04) et de Alexandre François (étudiant en LDDBI) pour le projet d'IN304 de 2023.)
## Compte rendu :
Pour le projet d'IN304, nous nous sommes dits qu'il fallait commencer par récupérer les Tweets, que nous avons ensuite transformés en objets (de Programmation Orientée Objet), que nous pourrions ensuite manipuler plus facilement.

Une fois la structure des tweets créée, notre deuxième étape fut :
* de supprimer les hyperliens ainsi que les émojis du texte de chaque Tweet ;
* de récupérer les hashtags (#) et les mentions (@).

Puis, nous nous sommes alors demandés comment les compter et les stocker. Alors, nous nous sommes donc mis d'accord sur l'utilisation de dictionnaires pour stocker les valeurs suivantes:
* le nombre d'apparition (l'occurrence) des Hashtags et des mentions dans les Tweets ;
* l'identifiant des Tweets qui utilisent ces Hashtags ou ces mentions ;
* les pseudonymes de ceux qui ont utilisés ces Hashtags ou mentions (s'il n'y en a pas, des pseudonymes aléatoires que nous avons choisi de manière arbitraire sont donnés à chaque Tweet).

Une fois les Tweets, les Hashtags et les mentions terminés, nous sommes passés à l'interface graphique. Nous avons utilisé Gradio, une librairie graphique pour faire des sites.

Pendant un moment, nous avons eu du mal à nous en servir, car nous ne l'avions jamais utilisée auparavant.  De ce fait, le code que nous avions fait était assez compliqué à lire (c'était un code en spaghetti), qui finalement fut modifié afin de concevoir un code plus propre.

Alexandre fit en grande partie le côté interface et optimisation, et permit à ce projet d'être plus clair et plus lisible, pendant que Maël s'occupait des structures de données et de manipuler certaines données et les graphiques.

Nous avons très rapidement compris comment faire nos graphiques, et nous sommes donc mis à en mettre dans notre projet, pour aider à visualiser les données traitées.

Peu de temps après, nous nous sommes occupés des Topics, qui jusque-là, nous posaient problème. Finalement, il y avait peu de difficultés.
Nous nous sommes ensuite dits qu'il serait amusant d'ajouter une carte, affichant dans quels pays les utilisateurs avaient tweeté, et montrant combien il y avait de Tweets par pays.

Enfin, nous nous sommes mis comme objectif de rendre le code plus clair, et finalement, nous pensons avoir enfin fini ce projet.

Ce projet est disponible sur Github. Il nous a pris exactement deux mois et un jour pour être finalisé, nous espérons qu'il vous plaise.