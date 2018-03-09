# Introduction
Lorsque je quitte la maison, je fais attention à éteindre les lumières pour plusieurs raisons. L’une d’elle est la diminution de la facture d’électricité et l’autre est la diminution de l’impact sur l’environnement.
Cet évènement est aujourd’hui naturel pour tous, car nous avons confiance dans notre fournisseur d’énergie : Chaque soir j’enclenche l’interrupteur, et je sais que la lumière s’allumera.

Nous pouvons appliquer cette routine dans notre milieu professionnel en éteignant nos environnements de développements. Cette pratique associée à la virtualisation et l’Auto Scaling a un réel impact sur l’environnement selon une étude de Berkeley Lab et sur votre facture AWS.

[United States Data Center Energy Usage Report | Energy Technologies Area](https://eta.lbl.gov/publications/united-states-data-center-energy)

# Architecture
Ce blog post va nous permettre d’automatiser cette pratique.

L’interrupteur est matérialisé par un évènement SNS et prend ainsi n’importe quelle forme en fonction de votre besoin : Amazon Dash Button, Bot Slack, Hipchat ou Facebook Messenger, Amazon Alexa, etc ... Vu que nos environnements sont partagés par une équipe, il est important de la notifier de l’arrêt de la plate-forme et d’annuler cet arrêt si une personne de l’équipe a besoin de travailler. Ce message d’arrêt prend n’importe quelle forme : Chatbot Facebook ou Slack, Amazon Alexa.


Voici les composants de l’architecture :
- 3 topics SNS, le premier en écoute des notifications d’arrêt des environnements, un en écoute des notifications d’annulation de l’arrêt des environnements et la dernière qui envoie des messages de notification
- Step function qui orchestre le workflow de destruction, d’annulation des environnements ainsi que les notifications
- Cloudformation pilote la destruction des environnements en fonction de tags paramétrés par l’utilisateur
- Lambda qui fait la glue entre chacun des composants

Je fais un focus sur le workflow Step function et l’utilisation particulière des Activities avec la Wait task. Suite à un message d’arrêt d’environnement, deux tâches sont exécutés en parallèle, CancelActivity est une activité qui attend l’éxecution d’un worker lambda lié au Topic SNS d’annulation, et WaitWorker qui attends pendant x secondes et execute une lambda qui vérifie les activités en cours (donc celles qui n’ont pas encore d’annulation) et la fail.
Ainsi en fonction du résultat de l’activity, on supprime ou pas l’environnement.


# Déploiement
Un template cloudformation

## Intégrer la solution avec AWS Iot Button

## Intégrer la solution avec Slack
https://aws.amazon.com/about-aws/whats-new/2015/12/aws-lambda-launches-slack-integration-blueprints/


