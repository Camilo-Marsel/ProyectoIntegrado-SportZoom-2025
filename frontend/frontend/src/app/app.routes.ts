import { Routes } from '@angular/router';
import { LoginComponent } from './login/login';
import { TiendaComponent } from './tienda/tienda';


export const routes: Routes = [
  { path: '', redirectTo: 'tienda', pathMatch: 'full' },
  { path: 'login', component: LoginComponent },
  { path: 'tienda', component: TiendaComponent },
];