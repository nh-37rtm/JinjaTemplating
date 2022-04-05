Object : <u>[INTERNE-EDL] Hub One – {{project_name}} : Environnement « {{env_name}} »</u>

[url_base]: https://{{base_url}} "Url de base"
[url_angular.ui]: https://{{base_url}}/ "Url Projet Angular.UI"

[url_history.api]: https://{{base_url}}/history-api/ "Url vers swagger de l'API history"
[url_importexport.api]: https://{{base_url}}/importexport-api/swagger/index.html "Url vers swagger de l'API importexport"
[url_pmm.api]: https://{{base_url}}/platformmanagement-api/ "Url vers swagger de l'API pmm"
[url_identity.api]: https://{{base_url}}/identity-api/ "Url vers swagger de l'API identity"
[url_ticketing.api]: https://{{base_url}}/ticketingmanagement-api/
[url_customermanagement.api]: https://{{base_url}}/customermanagement-api/
[url_assetmanagement.api]: https://{{base_url}}/assetmanagement-api/

{# [url_mission.api]: https://{{base_url}}/identity-api/swagger/index.html "Url vers swagger de l'API mission" #}

[url_kv_bus_message_dev]: https://portal.azure.com/#@hubonefr.onmicrosoft.com/asset/Microsoft_Azure_KeyVault/Secret/https://{{keyvault.base_url}}/secrets/{{keyvault.bus_id}} "Accès bus de message"
[url_kv_bdd_dev]: https://portal.azure.com/#@hubonefr.onmicrosoft.com/asset/Microsoft_Azure_KeyVault/Secret/https://{{keyvault.base_url}}/secrets/{{keyvault.database_id}} "Connexion string base de données"
[url_kv_stockage_dev]: https://portal.azure.com/#@hubonefr.onmicrosoft.com/asset/Microsoft_Azure_KeyVault/Secret/https://{{keyvault.base_url}}/secrets/{{keyvault.storageaccount_id}} "Accès Stockage BLOB"



Bonjour,

Je voulais vous informer que votre environnement est disponible  pour le projet {{project_name}} et également vous faire parvenir un récapitulatif des données propres à l'environnement de {{env_name}} :

* URL de base : [ici][url_base]
* History API (Swagger): [ici][url_history.api]
* Import Export API (Swagger): [ici][url_importexport.api]
* Platform Management API (Swagger): [ici][url_pmm.api]
* Identity API (Swagger): [ici][url_identity.api]
* Ticketing Management API [ici][url_ticketing.api]
* Asset Management API [ici][url_assetmanagement.api]
{# * Mission API (Swagger): [ici][url_mission.api] #}


Voici les informations de connexion qui vous permettrons accéder aux différents stockage de données (liens keyvault de stockage sécurisés):

* Accès Bus de message (Azure Service Bus): [ici][url_kv_bus_message_dev]
* Base de données (Azure SQL Database): [ici][url_kv_bdd_dev]
* Compte de Stockage blob (Azure Blob storage): [ici][url_kv_stockage_dev]

Note : Nous gérons les accès à ces données par utilisateur, en cas de problème d'accès merci de nous contacter.

L'accès à la base de données est possible seulement depuis certains réseaux
- HubOffice (Réseau bureautique ou depuis VPN DSI)
- Réseau WorklabEDL disponible sur site Dardilly.

Pour rappel toutes ces informations sont disponibles sur la page (README) du projet :

README : [ici]({{readme_link}})

Cet environnement étant destiné aux employés Hub One, <u>merci de ne pas partager ces informations</u> et/ou des informations permettant d’utiliser cette plateforme par une personne extérieure à la société.
Pour l’usage des personnes externe à l’entreprise le pôle production peux, sur demande, déployer des environnements clients : démo/ pré-prod/prod (sur les clusters de PPR/PRD).

Si vous avez des questions n'hésitez pas à nous contacter (Nicolas B., Cyrille N. ou moi).

Cordialement,

Nicolas Heim