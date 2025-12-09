# 🏃‍♂️ SportZoom – Plataforma de E-commerce para Calzado Deportivo

## 📋 Descripción

SportZoom es una plataforma web desarrollada para facilitar la venta de calzado deportivo y apoyar la digitalización de pequeños y medianos negocios en Colombia. El proyecto integra gestión de catálogo, inventario, carrito de compras y un panel administrativo completo.

### Contexto del Problema

Hoy en día, vender calzado en Colombia no es tan sencillo, sobre todo para los pequeños y medianos negocios que quieren competir con las grandes marcas. Abrir una tienda física es costoso, la visibilidad en internet es limitada y manejar el inventario puede ser difícil. Todo esto hace que se pierdan oportunidades de venta y que muchos emprendimientos no puedan crecer como deberían.

**SportZoom** busca resolver estos problemas ofreciendo una solución digital accesible que integra ventas en línea, gestión de inventario y procesamiento de pagos en una sola plataforma.

---

## ✨ Características Principales

### Para Compradores
- 🛍️ **Catálogo organizado** con filtros por marca, talla y precio
- 🔍 **Búsqueda avanzada** de productos
- 🛒 **Carrito de compras** intuitivo
- 💳 **Checkout simplificado** con simulación de pago
- 📧 **Confirmación por email** con detalles del pedido
- 📦 **Consulta de pedidos** mediante código único

### Para Administradores
- ➕ **CRUD completo** de productos
- 📊 **Gestión de inventario** en tiempo real
- 🏷️ **Organización por marcas y tallas**
- 🔐 **Autenticación JWT** segura
- 👤 **Panel administrativo** dedicado

---

## 🛠️ Tecnologías Utilizadas

### Backend
- **Framework:** Django 5.2.6
- **API:** Django REST Framework 3.16.1
- **Base de Datos:** PostgreSQL
- **Autenticación:** JWT (djangorestframework-simplejwt)
- **Manejo de imágenes:** Pillow
- **CORS:** django-cors-headers

### Frontend
- **Framework:** Angular 20
- **Estilos:** Tailwind CSS 3.4
- **HTTP Client:** RxJS
- **Email:** EmailJS
- **PDF:** jsPDF

### Herramientas de Desarrollo
- **Control de versiones:** Git / GitHub
- **Cliente Git:** GitKraken
- **Gestión de entorno:** Python venv / Node.js npm

---

## 📦 Instalación y Configuración

### Prerrequisitos

- Python 3.8+
- Node.js 18+ y npm
- PostgreSQL 12+
- Git

### 1️⃣ Clonar el Repositorio
```bash
git clone https://github.com/tu-usuario/ProyectoIntegrado-SportZoom-2025.git
cd ProyectoIntegrado-SportZoom-2025
```

### 2️⃣ Configurar el Backend (Django)

#### Crear y activar entorno virtual
```bash
cd backend

# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

#### Instalar dependencias
```bash
pip install -r requirements.txt
```

#### Configurar PostgreSQL

Crear la base de datos en PostgreSQL:
```sql
CREATE DATABASE sportzoom;
CREATE USER sportzoom_user WITH PASSWORD 'ClaveSportzoom123';
GRANT ALL PRIVILEGES ON DATABASE sportzoom TO sportzoom_user;
```

#### Aplicar migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```

#### Crear superusuario (administrador)
```bash
python manage.py createsuperuser
```

#### Ejecutar el servidor backend
```bash
python manage.py runserver
```

El backend estará disponible en: **http://localhost:8000**

---

### 3️⃣ Configurar el Frontend (Angular)

Abrir una nueva terminal:
```bash
cd frontend
```

#### Instalar dependencias
```bash
npm install
```

#### Ejecutar el servidor de desarrollo
```bash
npm start
# o alternativamente
ng serve
```

El frontend estará disponible en: **http://localhost:4200**

---

## 🚀 Uso del Sistema

### Acceso a la Aplicación

1. **Usuario Comprador:**
   - Accede a `http://localhost:4200`
   - Navega por el catálogo
   - Agrega productos al carrito
   - Completa el checkout
   - Consulta tu pedido con el código recibido

2. **Administrador:**
   - Accede a `http://localhost:4200/login`
   - Inicia sesión con las credenciales de superusuario
   - Gestiona productos, inventario y pedidos desde el panel administrativo

### Comandos Útiles

#### Backend
```bash
# Correr servidor
python manage.py runserver

# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Acceder al shell de Django
python manage.py shell
```

#### Frontend
```bash
# Correr desarrollo
npm start

# Compilar para producción
npm run build

# Ejecutar tests
npm test
```

---

## 📂 Estructura del Proyecto
```
ProyectoIntegrado-SportZoom-2025/
├── backend/
│   ├── config/              # Configuración del proyecto Django
│   ├── tienda/              # App principal
│   │   ├── models.py        # Modelos (Usuario, Producto, Pedido)
│   │   ├── views.py         # Vistas y endpoints API
│   │   ├── serializers.py   # Serializadores DRF
│   │   ├── urls.py          # Rutas de la API
│   │   └── permissions.py   # Permisos personalizados
│   ├── media/               # Imágenes de productos
│   ├── manage.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── tienda/           # Componente catálogo
│   │   │   ├── carrito/          # Componente carrito
│   │   │   ├── checkout/         # Componente pago
│   │   │   ├── confirmacion/     # Componente confirmación
│   │   │   ├── consulta-pedido/  # Componente consulta
│   │   │   ├── login/            # Componente login admin
│   │   │   └── services/         # Servicios HTTP
│   │   ├── index.html
│   │   └── styles.css
│   ├── package.json
│   └── angular.json
│
└── README.md
```

---

## 👥 Equipo de Desarrollo

- **Max Daniel Pérez Quintero** - Ingeniería en Sistemas - Universidad de Antioquia
- **Santiago Villegas Naranjo** - Ingeniería en Sistemas - Universidad de Antioquia  
- **Camilo Marsel Areiza Céspedes** - Ingeniería en Sistemas - Universidad de Antioquia

---

## 📅 Cronograma

- **Inicio:** 19 de agosto de 2025
- **Entrega:** 25 de noviembre de 2025
- **Sustentación:** 2 de diciembre de 2025

---

## 🔮 Próximas Características

- [ ] Integración real con pasarela de pago Wompi
- [ ] Sistema de reseñas y valoraciones
- [ ] Historial de pedidos para usuarios registrados
- [ ] Reportes de ventas y análisis de inventario
- [ ] Despliegue en servidor de producción
- [ ] Notificaciones push
- [ ] Gestión de múltiples imágenes por producto

---

## 📄 Licencia

Este proyecto es un trabajo académico desarrollado para la Universidad de Antioquia.

---

## 📧 Contacto

Para consultas o soporte: **sportzoom300@gmail.com**