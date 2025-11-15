import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClientModule, HttpClient } from '@angular/common/http';
import { AuthService } from '../services/auth.service';
import { RouterLink } from '@angular/router';
import { CarritoService } from '../services/carrito.service';

interface Producto {
  id?: number;
  nombre: string;
  precio: number | null;
  stock: number | null;
  marca: string;
  talla: string;
  imagen: string;
  disponibilidad?: string;
  descripcion?: string;
}

interface Usuario {
  es_admin: boolean;
  username: string;
}

@Component({
  selector: 'app-tienda',
  standalone: true,
  templateUrl: './tienda.html',
  styleUrls: ['./tienda.css'],
  imports: [
    CommonModule,
    FormsModule,
    HttpClientModule,
    RouterLink
  ]
})
export class TiendaComponent implements OnInit {
  apiUrl = 'http://127.0.0.1:8000/api';
  productos: Producto[] = [];
  productoSeleccionado: Producto | null = null;
  
  // 🔍 Filtros
  filtroNombre: string = '';
  filtroMarca: string = '';
  filtroTalla: string = '';
  filtroPrecioMin: number | null = null;
  filtroPrecioMax: number | null = null;
  
  // 📄 Paginación
  paginaActual: number = 1;
  productosPorPagina: number = 10;
  totalProductos: number = 0;
  totalPaginas: number = 0;
  siguientePagina: string | null = null;
  paginaAnterior: string | null = null;

  indiceInicio = 0;
  indiceFin = 0;
  
  cargando: boolean = false;
  usuario: Usuario | null = null;

  // Opciones disponibles
  marcasDisponibles: string[] = [
    'Nike', 'Adidas', 'Puma', 'Reebok', 'Converse', 
    'Vans', 'New Balance', 'Asics', 'Under Armour'
  ];
  
  tallasDisponibles: string[] = [
    '35', '36', '37', '38', '39', '40', 
    '41', '42', '43', '44', '45'
  ];

  productoForm: Producto = {
    nombre: '',
    precio: null,
    stock: null,
    marca: 'Nike',
    talla: '40',
    imagen: '',
    descripcion: ''
  };

  selectedFile: File | null = null;
  
  // Exponer Math para el template
  Math = Math;

  constructor(
    private http: HttpClient,
    private authService: AuthService,
    private carritoService: CarritoService,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit(): void {
    this.usuario = this.authService.obtenerUsuarioActual();
    this.cargarProductos();
  }

  logout() {
    this.authService.logout();
    this.usuario = null;
    alert('Has cerrado sesión');
  }
  
  // 🔥 Cargar productos con filtros aplicados
cargarProductos() {
  console.log('🔥 CARGAR PRODUCTOS LLAMADO');
  this.cdr.detectChanges();
  this.cargando = true;

  // ✅ Solo enviar filtros que tengan valores reales (no vacíos ni null)
  let params: any = {};

  const nombreTrim = this.filtroNombre?.trim();
  const marcaTrim = this.filtroMarca?.trim();
  const tallaTrim = this.filtroTalla?.trim();

  console.log('Valores trimmed:', { nombreTrim, marcaTrim, tallaTrim });

  if (nombreTrim) params.search = nombreTrim;
  if (marcaTrim) params.marca = marcaTrim;
  if (tallaTrim) params.talla = tallaTrim;
  if (this.filtroPrecioMin != null) params.precio_min = this.filtroPrecioMin;
  if (this.filtroPrecioMax != null) params.precio_max = this.filtroPrecioMax;

  // 🔹 Mantener página actual o usar 1 si no hay valor
  params.page = this.paginaActual || 1;
  params.page_size = this.productosPorPagina;

  console.log('📤 Params enviados al backend:', params);

  this.http.get<any>(`${this.apiUrl}/productos/`, { params }).subscribe({
    next: (res) => {
      console.log('✅ Respuesta del backend:', res);
      this.productos = res.results || res;
      this.totalProductos = res.count || this.productos.length;
      this.totalPaginas = Math.ceil(this.totalProductos / this.productosPorPagina);
      this.siguientePagina = res.next;
      this.paginaAnterior = res.previous;

      // 🧮 Calcular índices para mostrar el rango
      this.indiceInicio = (this.paginaActual - 1) * this.productosPorPagina + 1;
      this.indiceFin = Math.min(this.indiceInicio + this.productos.length - 1, this.totalProductos);

      this.cargando = false;
      this.cdr.detectChanges();
    },
    error: (err) => {
      console.error('❌ Error al cargar productos', err);
      this.cargando = false;
      this.cdr.detectChanges();
    }
  });
}


  // 🎯 Aplicar filtros (al hacer clic en el botón)
 aplicarFiltros() {
  console.log('🔍 APLICAR FILTROS LLAMADO');

    // Espera una microtarea para dejar que Angular actualice los ngModel antes de filtrar
  queueMicrotask(() => {
      console.log('Valores actuales (tras sync de ngModel):', {
        nombre: this.filtroNombre,
        marca: this.filtroMarca,
        talla: this.filtroTalla,
        precioMin: this.filtroPrecioMin,
        precioMax: this.filtroPrecioMax
  });

  this.paginaActual = 1;
    setTimeout(() => {
      this.cargarProductos();
      });
    });
  }

  // 🧹 Limpiar todos los filtros
  limpiarFiltros() {
    this.filtroNombre = '';
    this.filtroMarca = '';
    this.filtroTalla = '';
    this.filtroPrecioMin = null;
    this.filtroPrecioMax = null;
    this.paginaActual = 1;
    this.cdr.detectChanges();
    this.cargarProductos();
    this.cdr.detectChanges();
  }

  // 📄 Navegación de paginación
  irAPagina(pagina: number) {
    if (pagina >= 1 && pagina <= this.totalPaginas) {
      this.paginaActual = pagina;
      this.cargarProductos();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  }

  paginaSiguiente() {
    if (this.siguientePagina) {
      this.irAPagina(this.paginaActual + 1);
    }
  }

  paginaAnteriorNav() {
    if (this.paginaAnterior) {
      this.irAPagina(this.paginaActual - 1);
    }
  }

  // Generar array de números de página para mostrar
  obtenerPaginas(): number[] {
    const paginas: number[] = [];
    const rango = 2;
    
    for (let i = Math.max(1, this.paginaActual - rango); 
         i <= Math.min(this.totalPaginas, this.paginaActual + rango); 
         i++) {
      paginas.push(i);
    }
    
    return paginas;
  }

  verDetalle(producto: Producto) {
    if (this.productoSeleccionado === producto) {
      this.productoSeleccionado = null;
      this.limpiarFormulario();
    } else {
      this.productoSeleccionado = producto;
      if (this.usuario?.es_admin) {
        this.productoForm = { ...producto };
      }
    }
  }

  // 🛒 Añadir producto al carrito
  agregarAlCarrito(producto: Producto) {
    if (!producto.id) return;

    this.carritoService.agregarProducto({
      id: producto.id,
      nombre: producto.nombre,
      precio: producto.precio ?? 0,
      imagen: producto.imagen,
      cantidad: 1
    });

    alert(`Añadido al carrito: ${producto.nombre}`);
  }

  onFileSelected(event: any) {
    this.selectedFile = event.target.files[0];
  }

  guardarProducto() {
    // Verificar autenticación
    const token = this.authService.obtenerToken();
    if (!token) {
      alert('⚠️ Debes iniciar sesión como administrador para crear productos');
      return;
    }

    // Crear headers sin Content-Type (FormData lo maneja automáticamente)
    const headers = this.authService.obtenerCabeceraAuth();

    const formData = new FormData();
    formData.append('nombre', this.productoForm.nombre ?? '');
    formData.append('descripcion', this.productoForm.descripcion ?? '');
    formData.append('precio', String(this.productoForm.precio ?? 0));
    formData.append('stock', String(this.productoForm.stock ?? 0));
    formData.append('marca', this.productoForm.marca ?? 'Nike');
    formData.append('talla', this.productoForm.talla ?? '40');

    if (this.selectedFile) {
      formData.append('imagen', this.selectedFile);
    }

    console.log('🔐 Token:', token);
    console.log('📦 FormData:', Object.fromEntries(formData.entries()));

    if (this.productoForm.id) {
      // 🔄 Actualizar producto existente
      this.http.put(`${this.apiUrl}/productos/${this.productoForm.id}/`, formData, { headers }).subscribe({
        next: () => {
          alert('✅ Producto actualizado correctamente');
          this.limpiarFormulario();
          this.cargarProductos();
        },
        error: (err) => {
          console.error('❌ Error al actualizar producto:', err);
          if (err.status === 403) {
            alert('⚠️ No tienes permisos de administrador');
          } else {
            alert('❌ Error al actualizar producto');
          }
        }
      });
    } else {
      // ➕ Crear producto nuevo
      this.http.post(`${this.apiUrl}/productos/`, formData, { headers }).subscribe({
        next: (res: any) => {
          this.productos.push(res);
          this.limpiarFormulario();
          this.cargarProductos();
          alert('✅ Producto agregado correctamente');
        },
        error: (err) => {
          console.error('❌ Error al crear producto:', err);
          if (err.status === 403) {
            alert('⚠️ No tienes permisos de administrador. Verifica que hayas iniciado sesión.');
          } else if (err.status === 401) {
            alert('⚠️ Tu sesión ha expirado. Por favor inicia sesión nuevamente.');
          } else {
            alert('❌ Error al crear producto: ' + (err.error?.detail || 'Error desconocido'));
          }
        }
      });
    }
  }

  editarProducto(producto: Producto) {
    this.productoForm = { ...producto };
    this.productoSeleccionado = producto;
  }

  eliminarProducto(id: number) {
    if (!confirm('¿Seguro que quieres eliminar este producto?')) return;

    const headers = this.authService.obtenerCabeceraAuth();

    this.http.delete(`${this.apiUrl}/productos/${id}/`, { headers }).subscribe({
      next: () => {
        this.productos = this.productos.filter((p) => p.id !== id);
        this.productoSeleccionado = null;
        this.limpiarFormulario();
        alert('Producto eliminado correctamente');
      },
      error: (err) => {
        console.error('Error al eliminar producto', err);
        alert('No se pudo eliminar el producto');
      }
    });
  }

  limpiarFormulario() {
    this.productoForm = {
      nombre: '',
      precio: null,
      stock: null,
      marca: 'Nike',
      talla: '40',
      imagen: '',
      descripcion: ''
    };
    this.selectedFile = null;
  }
}