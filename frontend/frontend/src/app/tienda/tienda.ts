import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClientModule, HttpClient } from '@angular/common/http';

interface Producto {
  id: number;
  nombre: string;
  precio: string;
  stock: number;
  imagen: string;
  disponibilidad: string;
  descripcion?: string;
}

@Component({
  selector: 'app-tienda',
  standalone: true,
  templateUrl: './tienda.html',
  styleUrls: ['./tienda.css'],
  imports: [
    CommonModule,
    FormsModule,
    HttpClientModule
  ]
})
export class TiendaComponent implements OnInit {
  productos: Producto[] = [];
  productoSeleccionado: Producto | null = null;
  filtroNombre: string = '';
  cargando: boolean = false;

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    this.cargarProductos();
  }

  cargarProductos() {
  this.cargando = true;
  this.http.get<any>('/api/productos/')
    .subscribe({
      next: res => {
        console.log("Respuesta del backend:", res); // 👈 debug
        this.productos = res.results;
        this.cargando = false;
      },
      error: err => {
        console.error('Error al cargar productos', err);
        this.cargando = false;
      }
    });
}

  verDetalle(producto: Producto) {
    this.productoSeleccionado = producto;
  }

  filtrarProductos(): Producto[] {
    return this.productos.filter(p =>
      p.nombre.toLowerCase().includes(this.filtroNombre.toLowerCase())
    );
  }

  agregarAlCarrito(producto: Producto) {
    console.log('Producto añadido al carrito:', producto);
    alert(`Añadido al carrito: ${producto.nombre}`);
  }
}