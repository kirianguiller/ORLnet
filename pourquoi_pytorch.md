# PyTorch
Par besoin d’extensibilité (scalability), nous avons décidé de migrer sur PyTorch et sur un serveur gpu. En effet, 
Keras et Google Colab ne nous permettent pas de manipuler la totalité de nos données dans un temps raisonnable.

De plus, Pytorch possède pour notre problématique des avantages tels que les dataloader, 
le transfer learning et les pré-traitements ainsi que l'apprentissage sont bien plus personnalisable

## Dataloader
PyTorch dispose d’une classe Dataloader qui permet de ne charger en mémoire les données que batch par batch. 
Cela ralentit l'entraînement mais permet de pouvoir traiter des volumes de données très important. 
Dans ce processus de chargement de données, peut être incorporé des pipeline de transformation. 
Par exemple, pour les images, on peut ajouter un processus de normalisation de l’image, 
de changement de la taille, de rotation/translation, etc.. 
Cela permet donc de pré-traiter nos données et de faire de l’augmentation de données 
(technique utilisée pour améliorer la généralisation des modèles en transformant avant l’entrainement 
des échantillons de manière aléatoire).

En partant des spectrogrammes, nous n’avons pas réellement besoin de faire de l’augmentation de données puisque 
le format des spectrogrammes est contrôlé (position, angle et couleurs similaires d’une image à l’autre) mais 
la deuxième fonction du dataloader, le chargement par batch, nous est très utile.

## Transfer Learning
Une autre raison qui nous a amené à tester pytorch est la possibilité de faire de 
l’apprentissage par transfert (transfer learning). En effet, il existe déjà des modèles ResNet et 
VGG pré-entrainés sur des grandes banques d’images. On peut donc ensuite récupérer ces modèles, 
garder les couches convolutives qui servent à extraire les informations de l’image (à faire de l’abstraction) 
et ensuite ne réentrainer que les derniere couches (généralement le classifieur).


## Personnalisable
PyTorch possède un autre avantage par rapport à Keras qui est qu’il est très customisable. 
Il est facile d’ajouter des couches supplémentaires telles que la batchnormalisation, 
le dropout ou d’autres couches. De plus, le code de l'entraînement du modèle doit être écrit 
ligne par ligne. Il est donc plus facile de faire des erreurs mais aussi plus faciles de rajouter des 
lignes de codes qui s'exécutent à chaque epoch du modèle.
