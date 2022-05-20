Object : <u>[INTERNE-EDL] Hub One – Mobile Fleet Management : Environnement « PRD »</u>

[url_base]: https://homfm-prd.mobility.hubone.cloud "Url de base"
[url_angular.ui]: https://homfm-prd.mobility.hubone.cloud/ "Url Projet Angular.UI"

[url_history.api]: https://homfm-prd.mobility.hubone.cloud/history-api/ "Url vers swagger de l'API history"
[url_importexport.api]: https://homfm-prd.mobility.hubone.cloud/importexport-api/swagger/index.html "Url vers swagger de l'API importexport"
[url_pmm.api]: https://homfm-prd.mobility.hubone.cloud/platformmanagement-api/ "Url vers swagger de l'API pmm"
[url_identity.api]: https://homfm-prd.mobility.hubone.cloud/identity-api/ "Url vers swagger de l'API identity"
[url_ticketing.api]: https://homfm-prd.mobility.hubone.cloud/ticketingmanagement-api/
[url_customermanagement.api]: https://homfm-prd.mobility.hubone.cloud/customermanagement-api/
[url_assetmanagement.api]: https://homfm-prd.mobility.hubone.cloud/assetmanagement-api/



[url_kv_bus_message_dev]: https://portal.azure.com/#@hubonefr.onmicrosoft.com/asset/Microsoft_Azure_KeyVault/Secret/https://kv-infra-hoprd.vault.azure.net/secrets/cxstring-sbta-homfm-prd-hoprd "Accès bus de message"
[url_kv_bdd_dev]: https://portal.azure.com/#@hubonefr.onmicrosoft.com/asset/Microsoft_Azure_KeyVault/Secret/https://kv-infra-hoprd.vault.azure.net/secrets/cxstring-sqldb-homfm-prd-hoprd "Connexion string base de données"
[url_kv_stockage_dev]: https://portal.azure.com/#@hubonefr.onmicrosoft.com/asset/Microsoft_Azure_KeyVault/Secret/https://kv-infra-hoprd.vault.azure.net/secrets/cxstring-sthomfmprdhoprd "Accès Stockage BLOB"



Bonjour,

Je voulais vous informer que votre environnement est disponible  pour le projet Mobile Fleet Management et également vous faire parvenir un récapitulatif des données propres à l'environnement de PRD :

* URL de base : [ici][url_base]
* History API (Swagger): [ici][url_history.api]
* Import Export API (Swagger): [ici][url_importexport.api]
* Platform Management API (Swagger): [ici][url_pmm.api]
* Identity API (Swagger): [ici][url_identity.api]
* Ticketing Management API [ici][url_ticketing.api]
* Asset Management API [ici][url_assetmanagement.api]



Voici les informations de connexion qui vous permettrons accéder aux différents stockage de données (liens keyvault de stockage sécurisés):

* Accès Bus de message (Azure Service Bus): [ici][url_kv_bus_message_dev]
* Base de données (Azure SQL Database): [ici][url_kv_bdd_dev]
* Compte de Stockage blob (Azure Blob storage): [ici][url_kv_stockage_dev]

Note : Nous gérons les accès à ces données par utilisateur, en cas de problème d'accès merci de nous contacter.

L'accès à la base de données est possible seulement depuis certains réseaux
- HubOffice (Réseau bureautique ou depuis VPN DSI)
- Réseau WorklabEDL disponible sur site Dardilly.

Pour rappel toutes ces informations sont disponibles sur la page (README) du projet :

README : [ici]()

Cet environnement étant destiné aux employés Hub One, <u>merci de ne pas partager ces informations</u> et/ou des informations permettant d’utiliser cette plateforme par une personne extérieure à la société.
Pour l’usage des personnes externe à l’entreprise le pôle production peux, sur demande, déployer des environnements clients : démo/ pré-prod/prod (sur les clusters de PPR/PRD).

Si vous avez des questions n'hésitez pas à nous contacter (Nicolas B., Cyrille N. ou moi).

Cordialement,

Nicolas Heim