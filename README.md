# Flask Backend TFG

Backend para la plataforma web del Grado de Farmacia de la Facultad de Farmacia (UGR).

## Objetivo

El objetivo es desarrollar una API Restful para que posibles frontends, como el de
[frontend_tfg](https://github.com/JoseCarlosPPK/frontend_tfg) funcionen.

Para ello ha sido necesario previamente el análisis, diseño e implementación de la base de datos. Se proporciona una imagen docker con la base de datos diseñada para usar en desarrollo.

## Cómo iniciar el proyecto

Se está utilizando el _task runner_ `taskipy`, que trabaja en conjunto con el gestor de dependencias `poetry`.

La primera vez ha de instalar todas las dependencias:

```
poetry install
```

-  Para poner en marcha los contenederes docker:

```
poetry run task docker
task docker # si has ejecutado poetry shell previamente
```

-  Para poner en marcha el servidor de desarrollo de flask en modo debug:

```
poetry run task flask
task flask # si has ejecutado poetry shell previamente
```
