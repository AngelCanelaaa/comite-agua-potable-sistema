## REPORTE DE AVANCE — SERVICIO SOCIAL

Digitalización y optimización del sistema de control y cobro del servicio de agua potable

| | |
|---|---|
| **Alumno** | **Institución Receptora** |
| Angel de Jesús Canela Figueroa | Comité de Agua Potable |
| **Número de Control** | **Localidad** |
| 22420453 | Emiliano Zapata, Villamar, Michoacán |
| **Carrera** | **Período de reporte** |
| Ingeniería en Sistemas Computacionales | Enero — Julio 2026 |

## 1. OBJETIVO DEL PROYECTO

El objetivo del proyecto de servicio social es digitalizar el proceso de control y cobro del servicio de agua potable del Comité de Agua Potable de la localidad de Emiliano Zapata, Villamar, Michoacán. Actualmente el comité gestiona más de 300 usuarios de manera manual mediante cuadernos y hojas de cálculo básicas, lo cual genera dificultades para consultar información, identificar adeudos y generar reportes administrativos.

Se diseñó e implementó una base de datos local que permite registrar usuarios, tomas de agua, pagos y gastos del comité, optimizando la gestión de la información y facilitando su consulta.

## 2. DIAGNÓSTICO DEL SISTEMA ACTUAL

Antes de diseñar la solución se realizó un análisis del proceso manual existente, identificando las siguientes problemáticas:

1. El registro de pagos se realizaba en cuadernos físicos, sin respaldo digital.
2. No existía un método ágil para identificar usuarios con adeudos.
3. Los gastos del comité (sueldos, luz, arreglos) se registraban en hojas de cálculo sin estructura uniforme.
4. No había manera de generar reportes de balance mensual o anual de forma rápida.
5. El padrón de más de 300 usuarios activos no estaba centralizado ni organizado.
6. Un mismo usuario puede tener múltiples tomas, lo que dificultaba el control de pagos por toma.
7. Existen tarifas diferenciadas (\$100 mensual normal, \$70 para uso esporádico) que no estaban documentadas formalmente.
8. Las ofertas anuales (descuento por pago anticipado en enero, febrero y marzo) no tenían registro sistemático.

## 3. TECNOLOGÍA UTILIZADA Y JUSTIFICACIÓN

| **Tecnología** | **Justificación** |
|:---|----|
| **SQLite** | Base de datos relacional local. No requiere servidor ni instalación adicional. Todo el sistema queda en un único archivo (.db) portable y respaldable fácilmente. |
| **Python 3** | Lenguaje principal para el desarrollo de scripts de inicialización, carga de datos y pruebas. Multiplataforma (macOS y Windows). |
| **DB Browser for SQLite** | Herramienta visual gratuita que permite al encargado del comité consultar y administrar la base de datos sin necesidad de escribir código SQL. |

## ¿Por qué SQLite y no MySQL, PostgreSQL o Supabase?

- El sistema es de uso LOCAL — no requiere conexión a internet.
- Es operado por una sola persona (la encargada del cobro) en una sola computadora.
- SQLite no requiere instalar ni configurar un servidor de base de datos.
- El archivo .db es fácilmente respaldable copiándolo a una USB o nube.
- Es la solución más apropiada para sistemas administrativos locales de pequeña escala.

## 4. ESTRUCTURA DE LA BASE DE DATOS IMPLEMENTADA

Se diseñó e implementó una base de datos relacional con 7 tablas y 6 vistas, que cubren todos los procesos del comité:

| **Tabla** | **Función** | **Campos principales** |
|:---|----|----|
| **usuarios** | Padrón de personas con contrato | nombre, calle, activo, fecha_registro |
| **tomas** | Cada toma/contrato independiente | id_usuario, calle, tarifa (\$100/\$70), activa |
| **pagos** | Registro de cada cobro realizado | id_toma, fecha, monto, tipo (mensual/anual/adelanto/adeudo) |
| **detalle_pagos_meses** | Detalle de qué mes(es) cubre cada pago | id_pago, mes, anio, monto_mes, es_bonificado |
| **ofertas_anuales** | Define los descuentos por pago anual anticipado | anio, mes_límite, meses_bonificados |
| **gastos** | Egresos del comité por categoría | id_categoria, fecha, concepto, monto, mes |
| **categorias_gasto** | Catálogo: sueldos, luz, arreglos, contratos, otros | nombre, descripcion |
| **ingresos_extra** | Ingresos que no son pagos de tomas | concepto, monto, mes, anio |

**Adicionalmente se crearon 6 vistas (consultas predefinidas) para reportes:**

| **Vista** | **¿Qué muestra?** |
|:---|----|
| **vista_padron** | Listado completo de tomas activas con nombre del usuario |
| **vista_estado_toma** | Qué meses ha pagado cada toma en el año actual |
| **vista_adeudos** | Tomas activas con meses sin pagar |
| **vista_ingresos_mensuales** | Total cobrado por mes de pagos de tomas |
| **vista_gastos_mensuales** | Total gastado por mes, desglosado por categoría |
| **vista_balance_mensual** | Ingresos vs gastos + sobrante por mes y año |

## 5. ARCHIVOS DESARROLLADOS

| **Archivo** | **Descripción** |
|:---|----|
| **schema.sql** | Define la estructura completa de tablas, relaciones y vistas. Es el plano de la base de datos. |
| **seed.sql** | Inserta los datos iniciales: 6 categorías de gasto y las 3 ofertas anuales 2026. |
| **inicializar_bd.py** | Script Python que ejecuta schema.sql y seed.sql para crear la base de datos desde cero. |
| **datos_prueba_completos.py** | Script de pruebas que insertó datos ficticios y verificó el correcto funcionamiento de todas las tablas y vistas. |
| **agua_potable.db** | El archivo de base de datos SQLite generado por inicializar_bd.py. No se incluye en el repositorio; se regenera ejecutando el script. |

## 6. PRUEBAS DE FUNCIONAMIENTO REALIZADAS

Se ejecutaron pruebas que cubrieron los 4 tipos de pago que maneja el comité:

| **Tipo de pago** | **Caso probado** | **Resultado** |
|:---|----|----|
| **MENSUAL** | Pago normal mes a mes | Martínez Soria Rosa Elena pagó enero, febrero y marzo (\$100 cada mes). Correcto. |
| **ANUAL** | Pago año completo con oferta de enero | Chávez Ruiz Joaquín pagó \$1,100 en enero (11 meses), con diciembre bonificado por la oferta. Correcto. |
| **ADEUDO** | Pago de meses atrasados | Bautista Manzo Francisco liquidó en marzo los 3 meses pendientes (\$300). Correcto. |
| **ADELANTO** | Pago de meses futuros | Prado Canela Carlos pagó \$300 en febrero, cubriendo febrero, marzo y abril. Correcto. |

## Resultados del script de pruebas:

5 usuarios insertados correctamente

6 tomas registradas (incluyendo un usuario con 2 tomas independientes)

13 pagos registrados con los 4 tipos de pago

28 meses cubiertos en detalle (incluyendo meses bonificados por oferta)

15 gastos registrados en 6 categorías diferentes

3 ingresos extra (contratos nuevos)

Todas las vistas generaron resultados correctos

El balance mensual reflejó correctamente ingresos, gastos y sobrante

## 7. AVANCE RESPECTO AL CRONOGRAMA

| **Actividad** | **Estado** | **Observaciones** |
|:---|----|----|
| Análisis del proceso manual actual | Completada | Se identificaron 8 problemáticas del sistema manual |
| Levantamiento de requerimientos | Completada | Entrevistas con encargada del cobro realizadas |
| Diseño de la estructura de la BD | Completada | 7 tablas, 6 vistas, relaciones definidas |
| Desarrollo e implementación de la BD | Completada | Base de datos SQLite funcional creada |
| Pruebas de funcionamiento y ajustes | En proceso | Pruebas básicas exitosas; pruebas con datos reales pendientes |
| Digitalización del padrón de usuarios | Pendiente | Programada para siguiente etapa |
| Generación de reportes administrativos | Pendiente | Vistas creadas; interfaz gráfica pendiente |
| Documentación del sistema | Pendiente | En desarrollo continuo |
| Capacitación al encargado del cobro | Pendiente | Programada para etapa final |
| Apoyo técnico y seguimiento | Continuo | Se brinda soporte durante todo el servicio social |

## Reporte de Avance — Servicio Social 2026

Angel de Jesús Canela Figueroa · 22420453 · ISC · Comité de Agua Potable, Emiliano Zapata, Villamar, Mich.
