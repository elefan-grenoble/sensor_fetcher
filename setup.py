from setuptools import find_packages, setup

setup(
    name='src',
    packages=find_packages(),
    version='0.1.0',
    description='Récupération de données de capteur envoyées sur un broker MQTT',
    author='Albin Petit',
    license='MIT',
)
