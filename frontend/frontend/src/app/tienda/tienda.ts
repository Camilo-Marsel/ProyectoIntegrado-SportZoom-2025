import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClientModule, HttpClient } from '@angular/common/http';
import { AuthService } from '../services/auth.service';
import { RouterLink } from '@angular/router';
import { CarritoService } from '../services/carrito.service';

interface Producto {
  id?: number;
  nombre: string;
  precio: number | null;   // ✅ ahora puede ser null
  stock: number | null;    // ✅ ahora puede ser null
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
  filtroNombre: string = '';
  cargando: boolean = false;

  usuario: Usuario | null = null;

  // ✅ ahora los valores inician en null para mostrar placeholder
  productoForm: Producto = {
    nombre: '',
    precio: null,
    stock: null,
    imagen: '',
    descripcion: ''
  };

  selectedFile: File | null = null;

  constructor(
    private http: HttpClient,
    private authService: AuthService,
    private carritoService: CarritoService
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

  cargarProductos() {
    this.cargando = true;
    this.http.get<any>(`${this.apiUrl}/productos/`).subscribe({
      next: (res) => {
        console.log('Respuesta del backend:', res);
        this.productos = res.results || res;
        this.cargando = false;
      },
      error: (err) => {
        console.error('Error al cargar productos', err);
        this.cargando = false;
      }
    });
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

  filtrarProductos(): Producto[] {
    return this.productos.filter((p) =>
      p.nombre.toLowerCase().includes(this.filtroNombre.toLowerCase())
    );
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
    const headers = this.authService.obtenerCabeceraAuth();

    const formData = new FormData();
    formData.append('nombre', this.productoForm.nombre ?? '');
    formData.append('descripcion', this.productoForm.descripcion ?? '');
    formData.append('precio', String(this.productoForm.precio ?? 0));
    formData.append('stock', String(this.productoForm.stock ?? 0));

    if (this.selectedFile) {
      formData.append('imagen', this.selectedFile);
    }

    if (this.productoForm.id) {
      // 🔄 Actualizar producto existente
      this.http.put(`${this.apiUrl}/productos/${this.productoForm.id}/`, formData, { headers }).subscribe({
        next: () => {
          alert('Producto actualizado correctamente');
          this.limpiarFormulario();
          this.cargarProductos();
        },
        error: (err) => {
          console.error('Error al actualizar producto', err);
          alert('Error al actualizar producto');
        }
      });
    } else {
      // ➕ Crear producto nuevo
      this.http.post(`${this.apiUrl}/productos/`, formData, { headers }).subscribe({
        next: (res: any) => {
          this.productos.push(res);
          this.limpiarFormulario();
          alert('Producto agregado correctamente');
        },
        error: (err) => {
          console.error('Error al crear producto', err);
          alert('Error al crear producto');
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
    // ✅ se deja vacío para que los placeholders se vean
    this.productoForm = {
      nombre: '',
      precio: null,
      stock: null,
      imagen: '',
      descripcion: ''
    };
    this.selectedFile = null;
  }
}
