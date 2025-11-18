import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink, Router } from '@angular/router';
import { CarritoService } from '../services/carrito.service';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-carrito',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './carrito.component.html',
})
export class CarritoComponent implements OnInit {
  productos: any[] = [];

  constructor(
    private carritoService: CarritoService,
    private router: Router,
    private http: HttpClient
  ) {}

  ngOnInit(): void {
    this.productos = this.carritoService.obtenerCarrito();

    this.carritoService.carrito$.subscribe((productos) => {
      this.productos = productos;
    });
  }

  eliminar(id: number): void {
    this.carritoService.eliminarProducto(id);
  }

  vaciarCarrito(): void {
    const confirmar = confirm('¿Seguro que deseas vaciar el carrito?');
    if (confirmar) {
      this.carritoService.limpiarCarrito();
    }
  }

  get total(): number {
    return this.carritoService.calcularTotal();
  }

  finalizarCompra() {
    // Payload para crear pedido
    const pedidoPayload = {
      nombre: 'Cliente', // puedes pedir nombre si quieres
      email: 'Cliente@email.com',
      direccion: 'Direccion de Cliente',
      total: this.total,
      carrito: this.productos.map(p => ({
        id: p.id,
        nombre: p.nombre,
        precio: p.precio,
        cantidad: p.cantidad || 1
      }))
    };

    // Crear pedido en el backend
    this.http.post('http://localhost:8000/api/checkout/crear-pedido/', pedidoPayload)
      .subscribe({
        next: (resp: any) => {
          // Guardar el numero_pedido en localStorage
          localStorage.setItem('numero_pedido', resp.numero_pedido);

          // Redirigir al checkout
          this.router.navigate(['/checkout']);
        },
        error: () => {
          alert('Error al crear el pedido, intenta de nuevo.');
        }
      });
  }
}
