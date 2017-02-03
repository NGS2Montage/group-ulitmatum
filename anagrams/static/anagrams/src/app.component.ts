//our root app component
import {Component, OnInit} from '@angular/core'

// Services
import { LetterService } from './services/letter.service';


@Component({
  selector: 'my-app',
  template: `
      <h1>Hello World</h1>
      <ul class="letters">
        <li *ngFor="let letter of letters">
          {{letter}}
        </li>
      </ul>
      <h1 class="text-center">Angular 2 WebSockets example</h1>
      <div class="row">
        <div class="col-md-6">
          <!-- Column with small Chat application using websockets -->
          <create-message></create-message>
          <hr/>
          <chat-component></chat-component>
        </div>
      </div>
  `,
})
export class AppComponent implements OnInit {
  letters: string[];

  constructor(private letterService: LetterService) { }

  getLetters(): void {
    this.letterService.getLetters().then(letters => this.letters = letters);
  }

  ngOnInit(): void {
    this.getLetters();
  }
}
