import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { CarritoService } from '../services/carrito.service';

@Component({
  selector: 'app-carrito',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './carrito.component.html',
})
export class CarritoComponent implements OnInit {
  productos: any[] = [];

  constructor(private carritoService: CarritoService) {}

  ngOnInit(): void {
    // Recupera productos almacenados localmente
    this.productos = this.carritoService.obtenerCarrito();

    // Suscripción para actualizar en tiempo real al agregar o eliminar
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
}
