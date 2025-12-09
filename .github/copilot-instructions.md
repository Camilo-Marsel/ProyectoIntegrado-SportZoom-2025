# SportZoom AI Coding Agent Instructions

## Project Overview
SportZoom is a full-stack e-commerce platform for athletic footwear sales targeting small and medium businesses in Colombia. It integrates product catalog management, inventory control, shopping cart, payment processing (Wompi), and admin panel.

**Tech Stack:**
- **Backend:** Django 5.2.6 + Django REST Framework 3.16.1 + PostgreSQL
- **Frontend:** Angular 20 + Tailwind CSS 3.4 + RxJS
- **Auth:** JWT (djangorestframework-simplejwt) with custom user model
- **Database:** PostgreSQL with custom `Usuario` model extending `AbstractUser`

---

## Architecture & Data Flow

### Backend Structure (`backend/tienda/`)
The app follows Django REST Framework conventions with **models → serializers → views → URLs**:

1. **Models** (`models.py`): 
   - `Usuario` (extends `AbstractUser` with `es_admin` flag)
   - `Producto` (id, nombre, descripcion, precio, stock, marca, talla, imagen)
   - `Pedido` (numero_pedido UUID, carrito JSON, estado, Wompi payment tracking)
   
2. **Serializers** (`serializers.py`):
   - `ProductoSerializer`: includes computed fields (`imagen_url`, `disponibilidad`)
   - `AdminLoginSerializer`: validates admin status + JWT credentials
   - `PedidoSerializer`: handles order creation with read-only timestamp fields

3. **Views** (`views.py`):
   - **Public endpoints:** `ProductoList` (with filterable by marca, talla, price range)
   - **Admin endpoints:** `ProductoCreate`, `ProductoUpdate`, `ProductoDelete` (require `IsAdminUserCustom` permission)
   - **Checkout flow:** `crear_pedido` → `iniciar_pago` → `verificar_pago` (Wompi integration stubs)
   - **Query endpoints:** `consultar_pedido` by numero_pedido

4. **Permissions** (`permissions.py`):
   - Custom `IsAdminUserCustom`: checks `request.user.es_admin == True` (not Django's `is_staff`)
   - Admin login at `/api/admin/login/` uses `AdminLoginSerializer` to validate credentials and return JWT

### Frontend Structure (`frontend/src/app/`)
Standalone Angular 20 components with service-based architecture:

- **Components:** `tienda` (catalog), `carrito` (cart), `checkout` (payment), `confirmacion` (receipt), `consulta-pedido` (order lookup), `login` (admin)
- **Services:** `auth.service` (JWT token storage), `productos.service` (product queries), `carrito.service` (cart state), `checkout.service` (payment API)
- **Interceptors:** `AuthInterceptor` (auto-injects `Authorization: Bearer {token}` header)
- **Auth Storage:** tokens and user data stored in `localStorage` (with SSR checks via `isBrowser()`)

### API Routes (at `/api/`)
```
GET    /productos/              → ProductoList (filterable, paginated)
POST   /admin/login/            → AdminLoginView (returns JWT)
POST   /admin/productos/crear/  → ProductoCreate
PATCH  /admin/productos/{id}/actualizar/ → ProductoUpdate
DELETE /admin/productos/{id}/eliminar/    → ProductoDelete
POST   /checkout/crear-pedido/  → create order with UUID
POST   /checkout/pago/          → initiate Wompi payment
GET    /checkout/verificar/{numero_pedido}/ → verify payment status
GET    /pedidos/consultar/{numero_pedido}/  → customer order lookup
```

---

## Critical Workflows

### Starting Servers
**Backend** (requires Python 3.8+, PostgreSQL running):
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver  # http://localhost:8000
```

**Frontend** (requires Node.js 18+):
```bash
cd frontend
npm install
npm start  # http://localhost:4200 via ng serve
```

### Database Setup
```bash
# PostgreSQL (Linux/Mac: use createdb/createuser)
CREATE DATABASE sportzoom;
CREATE USER sportzoom_user WITH PASSWORD 'ClaveSportzoom123';
GRANT ALL PRIVILEGES ON DATABASE sportzoom TO sportzoom_user;

# Django migrations
python manage.py migrate
python manage.py createsuperuser
```

### Admin Workflow
1. Create superuser: `python manage.py createsuperuser` (sets `es_admin=True`)
2. Login via `/login` → POST to `/api/admin/login/` with credentials
3. Receive JWT token → stored in `localStorage`
4. Token auto-injected into requests via `AuthInterceptor`
5. Access admin endpoints (product CRUD) - protected by `IsAdminUserCustom`

---

## Project Conventions

### Database & Model Patterns
- **Custom user model:** Always use `Usuario` (not Django's `User`)
- **Timestamps:** `creado` (auto_now_add) on Producto; `fecha` on Pedido
- **Media files:** Upload path `productos/` → auto-resolved to `/media/productos/`
- **Choices as lists:** MARCAS and TALLAS use tuples in models, synchronized with frontend arrays
- **UUIDs for orders:** `numero_pedido = str(uuid.uuid4())[:8].upper()` in `Pedido.save()`

### Serializer Patterns
- **Computed fields:** Use `SerializerMethodField` for image URLs (e.g., `imagen_url`) and availability logic
- **Image handling:** `MultiPartParser` + `FormParser` required for file uploads in `CreateAPIView`
- **Request context:** Pass `{'request': self.request}` in serializer context for URL building

### View Patterns
- **Filtering:** Use `DjangoFilterBackend` + `SearchFilter` for marca/talla/precio_min/precio_max/search
- **Pagination:** DRF default (10 items/page) via settings
- **Admin checks:** All admin views use `permission_classes = [IsAdminUserCustom]`
- **CORS:** Allow only `http://localhost:4200` (hardcoded in settings)

### Frontend Patterns
- **SSR safety:** Always check `isBrowser()` before accessing `localStorage` (Angular SSR mode)
- **HTTP parameters:** Use `HttpParams` for query strings; map to DRF query params (e.g., `search`, `marca`, `precio_min`)
- **Interfaces:** Define `Producto`, `Usuario` interfaces in components/services for type safety
- **Token injection:** Interceptor auto-adds `Authorization` header; don't manually set headers for auth

### Naming Conventions
- **Endpoints:** kebab-case (`/admin/login/`, `/crear-pedido/`)
- **Model fields:** snake_case (`numero_pedido`, `es_admin`, `disponibilidad`)
- **TypeScript:** camelCase for variables (`filtroMarca`, `productoSeleccionado`)
- **Django:** snake_case for model fields, UPPERCASE for choices

---

## Integration Points & External Dependencies

### Wompi Payment Gateway (Stubs)
- `WOMPI_PUBLIC_KEY`, `WOMPI_PRIVATE_KEY`, `WOMPI_URL` in settings.py
- Views: `iniciar_pago` (POST), `verificar_pago` (GET) handle payment flow
- Order model stores `wompi_id`, `referencia_pago`, `estado` (pendiente/pagado/fallido)
- **Status:** Currently stubbed—real implementation pending Wompi API integration

### Email Notifications
- Frontend uses `EmailJS` for confirmation emails (in checkout flow)
- Backend stores order details; frontend handles email dispatch

### Image Processing
- Pillow library for image validation
- Images stored in `backend/media/productos/`
- Frontend builds absolute URLs via `imagen_url` serializer method

### CORS Configuration
- Frontend at `http://localhost:4200` requires CORS headers from backend
- `CORS_ALLOW_ALL_ORIGINS = True` in settings (dev only—tighten for production)

---

## Testing & Debugging Commands

### Backend
```bash
python manage.py makemigrations      # Create migration files
python manage.py migrate             # Apply migrations
python manage.py shell               # Interactive Django shell
python manage.py createsuperuser     # Create admin account
```

### Frontend
```bash
npm test                 # Run Jasmine tests (rarely used in this project)
npm run build           # Production build
ng serve --host 0.0.0.0 # Serve on all interfaces
```

### Common Issues
- **"No such table" errors:** Run `python manage.py migrate`
- **"es_admin attribute missing":** Ensure user created via Django admin or `createsuperuser`
- **CORS errors:** Verify `http://localhost:4200` in `CORS_ALLOWED_ORIGINS` and `DEBUG=True`
- **Image 404s:** Check `MEDIA_ROOT` / `MEDIA_URL` match; ensure `if settings.DEBUG` in urls.py

---

## Key Files Reference

| File | Purpose |
|------|---------|
| `backend/tienda/models.py` | Core data models (Usuario, Producto, Pedido) |
| `backend/tienda/views.py` | API endpoints and business logic |
| `backend/tienda/serializers.py` | DRF model serializers with computed fields |
| `backend/tienda/permissions.py` | Custom permission class `IsAdminUserCustom` |
| `backend/config/settings.py` | Django config: DB, JWT, CORS, Wompi keys |
| `backend/config/urls.py` | URL routing; JWT token endpoints |
| `frontend/src/app/services/*.ts` | HTTP service layer for backend calls |
| `frontend/src/app/interceptors/auth.interceptor.ts` | Auto-inject JWT headers |
| `frontend/src/app/tienda/tienda.ts` | Catalog component with filtering logic |

---

## Development Priorities
1. **Admin authentication:** Always test admin login + token injection before CRUD operations
2. **Filtering:** Verify marca/talla/price filters match serializer + view implementations
3. **Image uploads:** Test with MultiPartParser; validate absolute URL generation
4. **Order flow:** Track `numero_pedido` UUID generation and Wompi payment stubs
5. **CORS errors:** First check `DEBUG=True` and `CORS_ALLOWED_ORIGINS`
