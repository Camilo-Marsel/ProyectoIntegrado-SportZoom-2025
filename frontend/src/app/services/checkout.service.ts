import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class CheckoutService {

  // URL de tu backend para procesar pagos simulados
  private backendUrl = 'http://localhost:8000/api/checkout/pago/';

  constructor(private http: HttpClient) {}

  // Confirmar pago con backend simulado
  confirmarPago(payload: any): Observable<any> {
    return this.http.post(this.backendUrl, payload);
  }
}

