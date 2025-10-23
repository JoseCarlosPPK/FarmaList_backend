# 💊 FarmaList Backend - TFG 🎓

Backend para la plataforma web para el Grado de Farmacia de la Facultad de Farmacia (UGR).

Backend para la gestión de **centros colaboradores** y **listados de prácticas externas** para el Grado de Farmacia de la Facultad de Farmacia de la **UGR**. Implementa la lógica de negocio a través de una API RESTful.

## 🎯 Objetivo

Lógica necesaria para gestionar los listados de centros colaboradores para las prácticas externas
de los alumnos del grado.

El objetivo es desarrollar una **API Restful** para que posibles frontends, como el de
[frontend_tfg](https://github.com/JoseCarlosPPK/frontend_tfg) funcionen.

## Estado

Hay dos desarrollos llevándose a cabo:

1. [centros-datos-duplicados](https://github.com/JoseCarlosPPK/FarmaList_backend/tree/centros-datos-duplicados/main): A la hora de crear los listados, los datos de los centros se duplican (si te interesa mantener el estado de los listados tal cual los creastes aunque modifiques o borres los centros a posteriori). Version 1.0.0

2. [centros-por-referencia](https://github.com/JoseCarlosPPK/FarmaList_backend/tree/centros-por-referencia/main) A la hora de crear los listados, se utilizan referencias de los centros. No hay duplicación de datos pero si un centro se elimina, tampoco aparecerá en un listado que ya creaste en el pasado. _Actualmente en desarrollo_
