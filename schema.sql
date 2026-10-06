-- ============================================================
-- BASE DE DATOS: Comité de Agua Potable - Emiliano Zapata
-- Sistema de control y cobro del servicio de agua potable
-- ============================================================
-- Tecnología: SQLite
-- Autor: Angel de Jesús Canela Figueroa
-- Número de Control: 22420453
-- Fecha: 2026
-- ============================================================


-- ------------------------------------------------------------
-- TABLA: usuarios
-- Personas físicas o morales que contratan el servicio.
-- Un usuario puede tener una o más tomas (contratos).
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario      INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre          TEXT    NOT NULL,               -- Nombre completo del usuario
    calle           TEXT    NOT NULL,               -- Calle donde vive (dirección)
    activo          INTEGER NOT NULL DEFAULT 1,     -- 1 = activo, 0 = dado de baja
    fecha_registro  TEXT    NOT NULL DEFAULT (DATE('now'))
);


-- ------------------------------------------------------------
-- TABLA: tomas
-- Cada toma es un contrato independiente de servicio de agua.
-- Un usuario puede tener varias tomas (cada una se cobra aparte).
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS tomas (
    id_toma         INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario      INTEGER NOT NULL,               -- A quién pertenece esta toma
    calle           TEXT    NOT NULL,               -- Calle donde está instalada la toma
    numero_toma     TEXT,                           -- Número o identificador de la toma (opcional)
    tarifa_mensual  REAL    NOT NULL DEFAULT 100.0, -- Tarifa normal = $100, uso esporádico = $70
    activa          INTEGER NOT NULL DEFAULT 1,     -- 1 = activa, 0 = suspendida/cancelada
    fecha_contrato  TEXT    NOT NULL DEFAULT (DATE('now')),  -- Fecha en que se hizo el contrato
    notas           TEXT,                           -- Observaciones (ej: "uso y venga", local, etc.)

    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);


-- ------------------------------------------------------------
-- TABLA: pagos
-- Registro de cada pago recibido por una toma.
-- Un pago puede cubrir uno o varios meses (adelantos, adeudos,
-- o pago del año completo con descuento por oferta).
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS pagos (
    id_pago         INTEGER PRIMARY KEY AUTOINCREMENT,
    id_toma         INTEGER NOT NULL,               -- Qué toma está pagando
    fecha_pago      TEXT    NOT NULL DEFAULT (DATE('now')),  -- Fecha real del cobro
    monto_pagado    REAL    NOT NULL,               -- Dinero que entregó el usuario
    tipo_pago       TEXT    NOT NULL,               -- 'MENSUAL', 'ADELANTO', 'ADEUDO', 'ANUAL'
    anio            INTEGER NOT NULL,               -- Año al que corresponde el pago
    notas           TEXT,                           -- Observaciones del cobrador

    FOREIGN KEY (id_toma) REFERENCES tomas(id_toma)
);


-- ------------------------------------------------------------
-- TABLA: detalle_pagos_meses
-- Detalla exactamente qué mes(es) cubre cada pago.
-- Un pago puede cubrir varios meses, por eso se separa en detalle.
-- Ejemplo: pago anual de enero cubre enero-octubre (2 gratis = nov y dic)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS detalle_pagos_meses (
    id_detalle      INTEGER PRIMARY KEY AUTOINCREMENT,
    id_pago         INTEGER NOT NULL,               -- A qué pago pertenece este detalle
    mes             INTEGER NOT NULL,               -- Mes cubierto: 1=Enero, 2=Febrero... 12=Diciembre
    anio            INTEGER NOT NULL,               -- Año del mes cubierto
    monto_mes       REAL    NOT NULL,               -- Cuánto se asigna a ese mes
    es_bonificado   INTEGER NOT NULL DEFAULT 0,     -- 1 = mes gratis por oferta anual, 0 = pagado normal

    FOREIGN KEY (id_pago) REFERENCES pagos(id_pago)
);


-- ------------------------------------------------------------
-- TABLA: ofertas_anuales
-- Define las ofertas de pago anual por mes de contratación.
-- Permite que el sistema calcule automáticamente el descuento.
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS ofertas_anuales (
    id_oferta       INTEGER PRIMARY KEY AUTOINCREMENT,
    anio            INTEGER NOT NULL,               -- Año en que aplica la oferta
    mes_limite      INTEGER NOT NULL,               -- Mes máximo para aprovechar la oferta (1=Ene, 2=Feb, 3=Mar)
    meses_bonificados INTEGER NOT NULL,             -- Cuántos meses gratis da la oferta
    descripcion     TEXT                            -- Ej: "Paga 10, lleva 12 (enero)"
    -- Ejemplo de datos:
    -- 2026, 1, 2, "Paga en enero: 2 meses gratis"
    -- 2026, 2, 1, "Paga en febrero: 1 mes gratis"
    -- 2026, 3, 1, "Paga en marzo: 1 mes gratis"
);


-- ------------------------------------------------------------
-- TABLA: ingresos_extra
-- Ingresos que no vienen de pagos de tomas:
-- contratos nuevos, donaciones, cuotas especiales, etc.
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS ingresos_extra (
    id_ingreso      INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha           TEXT    NOT NULL DEFAULT (DATE('now')),
    concepto        TEXT    NOT NULL,               -- Descripción del ingreso
    monto           REAL    NOT NULL,
    mes             INTEGER NOT NULL,               -- Mes al que pertenece (1-12)
    anio            INTEGER NOT NULL,
    notas           TEXT
);


-- ------------------------------------------------------------
-- TABLA: categorias_gasto
-- Catálogo de tipos de gasto del comité.
-- Permite agregar nuevas categorías sin cambiar la estructura.
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS categorias_gasto (
    id_categoria    INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre          TEXT    NOT NULL UNIQUE,        -- Nombre de la categoría
    descripcion     TEXT                            -- Descripción opcional
    -- Datos iniciales (se insertan en seed.sql):
    -- 'SUELDOS'         - Pago al personal del comité
    -- 'LUZ'             - Electricidad de pozos y bombas
    -- 'ARREGLOS_OFICINA'- Reparaciones dentro de la oficina
    -- 'ARREGLOS_CALLE'  - Reparaciones en tuberías y red de distribución
    -- 'CONTRATOS'       - Materiales para instalación de nuevas tomas
    -- 'OTROS'           - Gastos eventuales no clasificados
);


-- ------------------------------------------------------------
-- TABLA: gastos
-- Registro de cada gasto realizado por el comité.
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS gastos (
    id_gasto        INTEGER PRIMARY KEY AUTOINCREMENT,
    id_categoria    INTEGER NOT NULL,               -- Tipo de gasto
    fecha           TEXT    NOT NULL DEFAULT (DATE('now')),
    concepto        TEXT    NOT NULL,               -- Descripción específica del gasto
    monto           REAL    NOT NULL,
    mes             INTEGER NOT NULL,               -- Mes al que pertenece (1-12)
    anio            INTEGER NOT NULL,
    notas           TEXT,                           -- Observaciones adicionales

    FOREIGN KEY (id_categoria) REFERENCES categorias_gasto(id_categoria)
);


-- ============================================================
-- VISTAS ÚTILES PARA REPORTES
-- ============================================================

-- Vista: estado de cuenta por toma (qué meses ha pagado en el año actual)
CREATE VIEW IF NOT EXISTS vista_estado_toma AS
SELECT
    t.id_toma,
    u.nombre                        AS nombre_usuario,
    t.calle,
    t.numero_toma,
    t.tarifa_mensual,
    t.activa,
    dpm.mes,
    dpm.anio,
    dpm.monto_mes,
    dpm.es_bonificado
FROM tomas t
JOIN usuarios u ON t.id_usuario = u.id_usuario
LEFT JOIN pagos p ON p.id_toma = t.id_toma
LEFT JOIN detalle_pagos_meses dpm ON dpm.id_pago = p.id_pago;


-- Vista: resumen mensual de ingresos por cobro de tomas
CREATE VIEW IF NOT EXISTS vista_ingresos_mensuales AS
SELECT
    dpm.anio,
    dpm.mes,
    COUNT(DISTINCT p.id_toma)       AS tomas_que_pagaron,
    SUM(dpm.monto_mes)              AS total_cobrado
FROM detalle_pagos_meses dpm
JOIN pagos p ON p.id_pago = dpm.id_pago
WHERE dpm.es_bonificado = 0
GROUP BY dpm.anio, dpm.mes;


-- Vista: resumen mensual de gastos por categoría
CREATE VIEW IF NOT EXISTS vista_gastos_mensuales AS
SELECT
    g.anio,
    g.mes,
    cg.nombre                       AS categoria,
    SUM(g.monto)                    AS total_gastado
FROM gastos g
JOIN categorias_gasto cg ON cg.id_categoria = g.id_categoria
GROUP BY g.anio, g.mes, cg.nombre;


-- Vista: balance mensual (ingresos totales vs gastos totales)
CREATE VIEW IF NOT EXISTS vista_balance_mensual AS
SELECT
    anio,
    mes,
    SUM(ingresos)                   AS total_ingresos,
    SUM(gastos)                     AS total_gastos,
    SUM(ingresos) - SUM(gastos)     AS sobrante
FROM (
    -- Ingresos de tomas
    SELECT anio, mes, SUM(monto_mes) AS ingresos, 0 AS gastos
    FROM detalle_pagos_meses
    WHERE es_bonificado = 0
    GROUP BY anio, mes

    UNION ALL

    -- Ingresos extra
    SELECT anio, mes, SUM(monto) AS ingresos, 0 AS gastos
    FROM ingresos_extra
    GROUP BY anio, mes

    UNION ALL

    -- Gastos
    SELECT anio, mes, 0 AS ingresos, SUM(monto) AS gastos
    FROM gastos
    GROUP BY anio, mes
)
GROUP BY anio, mes;


-- Vista: tomas con adeudo (meses sin pagar en el año actual)
-- Identifica qué tomas no tienen registrado pago en cada mes
CREATE VIEW IF NOT EXISTS vista_adeudos AS
SELECT
    t.id_toma,
    u.nombre                        AS nombre_usuario,
    t.calle,
    t.numero_toma,
    t.tarifa_mensual
FROM tomas t
JOIN usuarios u ON t.id_usuario = u.id_usuario
WHERE t.activa = 1
  AND t.id_usuario = u.id_usuario;
  -- Nota: el filtro real de adeudos se aplica desde el código
  -- comparando los meses pagados vs los meses transcurridos del año


-- Vista: listado completo de tomas activas con su usuario
CREATE VIEW IF NOT EXISTS vista_padron AS
SELECT
    t.id_toma,
    u.id_usuario,
    u.nombre                        AS nombre_usuario,
    t.calle                         AS calle_toma,
    t.numero_toma,
    t.tarifa_mensual,
    t.fecha_contrato,
    t.notas
FROM tomas t
JOIN usuarios u ON t.id_usuario = u.id_usuario
WHERE t.activa = 1
ORDER BY t.calle, u.nombre;
