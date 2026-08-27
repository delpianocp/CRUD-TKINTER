# ⚡ CRUD Mediciones Eléctricas — Tkinter

> Aplicación de escritorio en Python para el registro y gestión de mediciones eléctricas · Arquitectura MVC · Patrón Observer · ORM Peewee · Interfaz gráfica con Tkinter

---

## 📌 Descripción

Aplicación desktop desarrollada en Python para registrar, visualizar, modificar y eliminar mediciones eléctricas (sector, fase, fecha y hora). Implementa buenas prácticas de diseño de software con arquitectura **MVC**, patrón de diseño **Observer**, **decoradores** para logging automático y soporte para múltiples bases de datos.

---

## 🛠️ Tecnologías y módulos utilizados

| Módulo | Uso |
|---|---|
| **Tkinter** | Interfaz gráfica de escritorio |
| **Matplotlib** | Visualización de gráficos de mediciones |
| **Peewee ORM** | Abstracción de base de datos (MySQL / SQLite) |
| **SQLite3** | Base de datos local por defecto |
| **re** | Validaciones con expresiones regulares |
| **socket (UDP)** | Servidor UDP para recepción de datos |

---

## 🏗️ Arquitectura del proyecto

El proyecto sigue el patrón **MVC (Modelo - Vista - Controlador)** con patrones de diseño adicionales:

```
CRUD-TKINTER/
│
├── controlador.py          # Controlador: punto de entrada, inicializa la vista
├── vista.py                # Vista: interfaz gráfica con Tkinter
├── modelo_ORM.py           # Modelo: ORM Peewee, operaciones CRUD sobre la DB
│
├── funcion_deco.py         # Decorador: registro automático de operaciones en log
├── log_actividad.py        # Logger: registra actividad y errores del sistema
├── validaciones.py         # Validaciones de datos con expresiones regulares
├── udp_server.py           # Servidor UDP para recibir mediciones externas
│
├── registroMed.db          # Base de datos SQLite (generada automáticamente)
├── log-reg.txt             # Log de actividad del sistema
├── reg_errores.txt         # Log de errores del sistema
├── reg_errores.py          # Módulo de registro de errores
│
├── image/                  # Recursos gráficos de la interfaz
└── Documentacion en html/  # Documentación del proyecto en HTML
```

---

## 🗄️ Modelo de datos

La tabla `Mediciones` almacena los siguientes campos:

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | Auto | Identificador único |
| `sector` | CharField | Sector donde se tomó la medición |
| `fase` | FloatField | Valor de la medición de fase |
| `fecha` | CharField | Fecha de la medición |
| `hora` | CharField | Hora de la medición |

---

## ⚙️ Funcionalidades

- **Crear** — Registrar nuevas mediciones con sector, fase, fecha y hora
- **Leer** — Listar todas las mediciones o filtrar por fecha o sector
- **Actualizar** — Modificar cualquier campo de un registro existente
- **Eliminar** — Borrar un registro por su ID
- **Graficar** — Visualizar mediciones con Matplotlib
- **Servidor UDP** — Recibir mediciones automáticamente desde dispositivos externos
- **Log automático** — Registro de cada operación CRUD mediante decoradores
- **Manejo de errores** — Log de errores con trazabilidad

---

## 🎨 Patrones de diseño implementados

- **MVC** — Separación clara entre Modelo, Vista y Controlador
- **Observer** — La base de datos notifica cambios a los observadores registrados
- **Decorator** — `@registro_log` registra automáticamente cada operación CRUD en el log

---

## 🗃️ Base de datos

Por defecto usa **SQLite** (sin configuración adicional). Para cambiar a **MySQL**, editar la línea 8 de `modelo_ORM.py`:

```python
# SQLite (por defecto)
base_datos_seleccion = "sqlite"

# MySQL
base_datos_seleccion = "mysql"
# Configurar también: host, user, passwd, database en el método selectMydb()
```

---

## 🚀 Instalación y uso

### 1. Clonar el repositorio

```bash
git clone https://github.com/delpianocp/CRUD-TKINTER.git
cd CRUD-TKINTER
```

### 2. Instalar dependencias

```bash
pip install peewee matplotlib
```

> Tkinter viene incluido con Python. SQLite3 también es parte de la librería estándar.

### 3. Ejecutar la aplicación

```bash
python controlador.py
```

La base de datos `registroMed.db` se crea automáticamente al primer inicio.

### 4. (Opcional) Iniciar el servidor UDP

```bash
python udp_server.py
```

---

## 📋 Requisitos

- Python 3.x
- peewee
- matplotlib
- Tkinter (incluido en Python estándar)

---

## 👤 Autor

**delpianocp** — [github.com/delpianocp](https://github.com/delpianocp)
