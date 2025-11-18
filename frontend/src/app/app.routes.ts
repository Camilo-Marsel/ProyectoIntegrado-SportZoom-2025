import { Routes } from '@angular/router';
import { LoginComponent } from './login/login';
import { TiendaComponent } from './tienda/tienda';
import { CarritoComponent } from './carrito/carrito';
import { CheckoutComponent } from './checkout/checkout';
import { ConfirmacionComponent } from './confirmacion/confirmacion';

export const routes: Routes = [
  { path: '', redirectTo: 'tienda', pathMatch: 'full' },
  { path: 'login', component: LoginComponent },
  { path: 'tienda', component: TiendaComponent },
  { path: 'carrito', component: CarritoComponent },
  { path: 'checkout', component: CheckoutComponent },
  { path: 'confirmacion', component: ConfirmacionComponent },
];
