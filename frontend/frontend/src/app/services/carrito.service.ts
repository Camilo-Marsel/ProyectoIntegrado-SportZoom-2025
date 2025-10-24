import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

interface ProductoCarrito {
  id: number;
  nombre: string;
  precio: number;
  cantidad: number;
  imagen: string;
}

@Injectable({ providedIn: 'root' })
export class CarritoService {
  private carrito: ProductoCarrito[] = [];
  private carritoSubject = new BehaviorSubject<ProductoCarrito[]>([]);
  carrito$ = this.carritoSubject.asObservable();

  agregarProducto(producto: ProductoCarrito) {
    const existente = this.carrito.find(p => p.id === producto.id);
    if (existente) {
      existente.cantidad++;
    } else {
      this.carrito.push({ ...producto, cantidad: 1 });
    }
    this.carritoSubject.next(this.carrito);
    localStorage.setItem('carrito', JSON.stringify(this.carrito));
  }

  eliminarProducto(id: number) {
    this.carrito = this.carrito.filter(p => p.id !== id);
    this.carritoSubject.next(this.carrito);
    localStorage.setItem('carrito', JSON.stringify(this.carrito));
  }

  obtenerCarrito(): ProductoCarrito[] {
    const guardado = localStorage.getItem('carrito');
    if (guardado) {
      this.carrito = JSON.parse(guardado);
      this.carritoSubject.next(this.carrito);
    }
    return this.carrito;
  }

  limpiarCarrito() {
    this.carrito = [];
    this.carritoSubject.next([]);
    localStorage.removeItem('carrito');
  }

  calcularTotal(): number {
    return this.carrito.reduce((acc, p) => acc + p.precio * p.cantidad, 0);
  }
}
