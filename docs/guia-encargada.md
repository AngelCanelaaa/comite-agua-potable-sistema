## Guía de Uso del Sistema

Cómo ver, agregar, editar y actualizar información · Comité de Agua Potable

## Esta guía es para ti, encargada del cobro:

Aquí aprenderás a:

- Abrir el sistema en tu computadora
- Ver la información de usuarios, tomas y pagos
- Agregar un usuario nuevo (contrato nuevo)
- Registrar un pago
- Registrar un gasto
- Actualizar o corregir información
- Consultar reportes (quién debe, cuánto entró, cuánto se gastó)

## A. CÓMO ABRIR EL SISTEMA

### Paso 1. Busca el programa

Busca en tus aplicaciones el programa llamado 'DB Browser for SQLite' y ábrelo.

### Paso 2. Abre la base de datos

Haz clic en el botón 'Open Database' (arriba a la izquierda).

### Paso 3. Selecciona el archivo

Navega a la carpeta donde está guardado el sistema y selecciona el archivo: agua_potable.db

### Paso 4. Listo

Verás el sistema abierto con todas las tablas a la izquierda. Haz clic en la pestaña 'Browse Data' para ver los datos.

## Tip — Cómo ver la información de cualquier tabla:

- Haz clic en la pestaña 'Browse Data' (arriba)
- En el menú que dice 'Table' selecciona la tabla que quieres ver:
- usuarios → para ver las personas con contrato
- tomas → para ver cada toma de agua
- pagos → para ver todos los pagos registrados
- gastos → para ver los gastos del comité

## B. CÓMO AGREGAR UN USUARIO NUEVO (CONTRATO NUEVO)

Cuando alguien contrata el servicio por primera vez, necesitas hacer DOS cosas: primero registrar al usuario y luego registrar su toma.

**PARTE 1 — Registrar al usuario:**

### Paso 1. Ve a la tabla usuarios

En 'Browse Data', selecciona la tabla 'usuarios'.

### Paso 2. Haz clic en el botón +

Abajo de la tabla hay un botón con un símbolo + (Insert a new record). Haz clic en él.

### Paso 3. Llena los datos

Se creará una fila nueva. Haz doble clic en cada celda para escribir:

| **Campo** | **Qué escribir** |
|----|----|
| **id_usuario** | Lo pone el sistema automáticamente, no tocar |
| **nombre** | Nombre completo de la persona (ejemplo: Pérez Gómez María) |
| **calle** | Nombre de la calle (ejemplo: MORELOS) |
| **activo** | Escribe el número 1 (significa que está activo) |
| **fecha_registro** | La fecha de hoy en formato 2026-03-06 |

### Paso 4. Guarda

Haz clic en el botón 'Write Changes' (arriba) para guardar. Siempre hazlo después de cualquier cambio.
**PARTE 2 — Registrar la toma:**

### Paso 5. Ve a la tabla tomas

En 'Browse Data', selecciona la tabla 'tomas'.

### Paso 6. Haz clic en +

Agrega una fila nueva igual que antes.

### Paso 7. Llena los datos de la toma

Escribe en cada celda:

| **Campo** | **Qué escribir** |
|----|----|
| **id_toma** | Lo pone el sistema automáticamente |
| **id_usuario** | El número de id del usuario que acabas de registrar |
| **calle** | Calle donde está la toma |
| **numero_toma** | Un número o código que identifique la toma (ejemplo: M-15) |
| **tarifa_mensual** | 100 (o 70 si es de uso y venga) |
| **activa** | 1 |
| **fecha_contrato** | Fecha de hoy (ejemplo: 2026-03-06) |
| **notas** | Puedes dejarlo vacío o escribir una observación |

### Paso 8. Guarda

Haz clic en 'Write Changes' para guardar.

## C. CÓMO REGISTRAR UN PAGO

Cuando alguien venga a pagar, necesitas registrar el pago en DOS tablas: primero en 'pagos' y luego en 'detalle_pagos_meses'.

### Paso 1. Ve a la tabla pagos

En 'Browse Data', selecciona 'pagos' y haz clic en +

| **Campo** | **Qué escribir** |
|------------------|------------------------------------------|
| **id_pago** | Automático |
| **id_toma** | El número de la toma que está pagando |
| **fecha_pago** | Fecha de hoy (ejemplo: 2026-03-06) |
| **monto_pagado** | Lo que te dio en efectivo (ejemplo: 100) |
| **tipo_pago** | MENSUAL / ADELANTO / ADEUDO / ANUAL |
| **anio** | 2026 |
| **notas** | Opcional, algún comentario del pago |

### Paso 2. Guarda y anota el id_pago

Haz clic en 'Write Changes'. Fíjate bien en el número id_pago que se asignó, lo necesitarás en el siguiente paso.

### Paso 3. Ve a detalle_pagos_meses

Selecciona esa tabla y haz clic en + por cada mes que cubre el pago.

| **Campo** | **Qué escribir** |
|-------------------|-------------------------------------------------------|
| **id_detalle** | Automático |
| **id_pago** | El número que anotaste del paso anterior |
| **mes** | El número del mes: 1=enero, 2=febrero... 12=diciembre |
| **anio** | 2026 |
| **monto_mes** | Lo que corresponde a ese mes (ejemplo: 100) |
| **es_bonificado** | 0 (normal) o 1 (mes gratis por oferta) |

## Ejemplo — Alguien paga enero y febrero juntos ($200):

En pagos: monto_pagado = 200, tipo_pago = MENSUAL

En detalle_pagos_meses: agrega DOS filas:

Fila 1 — id_pago = (el que se asignó), mes = 1, monto_mes = 100, es_bonificado = 0

Fila 2 — id_pago = (el mismo), mes = 2, monto_mes = 100, es_bonificado = 0

## D. CÓMO REGISTRAR UN GASTO

### Paso 1. Ve a la tabla gastos

En 'Browse Data', selecciona 'gastos' y haz clic en +

| **Campo** | **Qué escribir** |
|----|----|
| **id_gasto** | Automático |
| **id_categoria** | 1=SUELDOS 2=LUZ 3=ARREGLOS_OFICINA 4=ARREGLOS_CALLE 5=CONTRATOS 6=OTROS |
| **fecha** | Fecha del gasto (ejemplo: 2026-03-06) |
| **concepto** | Descripción breve (ejemplo: Sueldo cobrador marzo) |
| **monto** | Cantidad en pesos (ejemplo: 5000) |
| **mes** | Número del mes: 1=enero... 12=diciembre |
| **anio** | 2026 |
| **notas** | Opcional |

### Paso 2. Guarda

Haz clic en 'Write Changes'.

## E. CÓMO CORREGIR O ACTUALIZAR UN DATO

### Paso 1. Encuentra el registro

En 'Browse Data', selecciona la tabla y busca el registro que quieres corregir.

### Paso 2. Haz doble clic en la celda

Haz doble clic directamente sobre el dato que quieres cambiar.

### Paso 3. Escribe el nuevo valor

Borra el valor anterior y escribe el correcto.

### Paso 4. Guarda

Haz clic en 'Write Changes' para guardar el cambio.

## Importante — Antes de editar o eliminar:

- Nunca elimines un pago ya registrado a menos que sea un error claro.
- Si una toma se cancela, cambia el campo 'activa' a 0 (no la borres).
- Si un usuario se va, cambia el campo 'activo' a 0 (no lo borres).
- Siempre haz clic en 'Write Changes' después de cualquier cambio.
- Si te equivocas antes de guardar, haz clic en 'Revert Changes' para deshacer.

## F. CÓMO VER LOS REPORTES

Los reportes se llaman 'Vistas'. Para verlos, ve a 'Browse Data' y en el menú 'Table' busca los que empiezan con vista\_

| **Vista (reporte)** | **¿Para qué sirve?** |
|----|----|
| **vista_padron** | Ver todas las tomas activas con nombre del usuario |
| **vista_estado_toma** | Ver qué meses ha pagado cada toma |
| **vista_adeudos** | Ver quiénes tienen tomas con meses sin pagar |
| **vista_ingresos_mensuales** | Ver cuánto se cobró cada mes |
| **vista_gastos_mensuales** | Ver cuánto se gastó cada mes por categoría |
| **vista_balance_mensual** | Ver el balance: cuánto entró, cuánto salió y cuánto sobró |

## G. CÓMO HACER UN RESPALDO (MUY IMPORTANTE)

## Haz esto al menos una vez por semana:

1. Cierra DB Browser (o cierra la base de datos primero con File → Close Database)

2. Ve a la carpeta donde está el archivo agua_potable.db

3. Copia ese archivo a una USB o a Google Drive

4. Ponle un nombre con la fecha, por ejemplo: agua_potable_2026-03-06.db

Si algo le pasa a la computadora, con ese respaldo no pierdes nada.

## Sistema de Control y Cobro — Comité de Agua Potable

Emiliano Zapata, Villamar, Michoacán · 2026
