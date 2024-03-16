Récupération des données de capteur depuis un broker MQTT
=========================================================

Ce projet a été initié par l'épicerie participative [l'Elefan](https://lelefan.org/).

## Fonctionnement

Ce projet récupère les données de capteur sur un broker MQTT et les importe dans une base de données

## Installation globale

### En local

1. Configurer les variables d'environnement dans le fichier `.env` (voir `.env.EXEMPLE`)
1. Installer les packages python `pip install -r requirements.txt`
1. Lancer le docker-compose pour instancier une DB et un broker MQTT `cd dev && docker compose up`
1. Run `python src/sensor_fetcher.py`

### Avec Docker

1. Installer docker
1. Configurer les variables d'environnement dans un fichier `.env` (voir `.env.EXEMPLE`)
1. Build the image within the directory : `docker build -t sensorfetcher:latest "."`
1. Run `docker run --network="host" -it sensorfetcher:latest`

Organisation
------------

    ├── LICENSE
    ├── README.md               <- The top-level README for developers using this project.
    ├── requirements.txt        <- The requirements file for production environement
    ├── requirements-dev.txt    <- The requirements file for developpment environement
    ├── setup.py                <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                     <- Source code for use in this project.
    │   ├── __init__.py         <- Makes src a Python module
    │   ├── database_manager.py <- Contains all the logic for storing data in a mysql database
    │   ├── mqtt_connector.py   <- Contains all the logic for retriving data on a MQTT broker
    │   └── sensor_fetcher.py   <- Scripts to start fetching data from the broker and storing them on DB
    └── tox.ini                 <- tox file with settings for running tox; see tox.readthedocs.io


