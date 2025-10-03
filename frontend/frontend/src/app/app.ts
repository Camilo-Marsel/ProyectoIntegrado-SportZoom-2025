import { Component } from '@angular/core';
import { TiendaComponent } from './tienda/tienda';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [TiendaComponent],
  templateUrl: './app.html',
  styleUrls: ['./app.css']
})
export class AppComponent {}
