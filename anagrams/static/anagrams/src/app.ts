//our root app component
import {Component, NgModule, OnInit} from '@angular/core'
import {BrowserModule} from '@angular/platform-browser'
import { LetterService } from './letter.service';
import { ChatService } from './chat.service';
import { WebSocketService } from './websocket.service';

@Component({
  selector: 'my-app',
  template: `
      <ul class="heroes">
        <li *ngFor="let letter of letters">
          {{letter}}
        </li>
      </ul>
  `,
})
export class AppComponent implements OnInit {
  letters: string[];

  constructor(private letterService: LetterService) { }

  getHeroes(): void {
    this.letterService.getHeroes().then(letters => this.letters = letters);
  }

  ngOnInit(): void {
    this.getHeroes();
  }
}

@NgModule({
  imports: [ BrowserModule ],
  declarations: [ AppComponent ],
  bootstrap: [ AppComponent ],
  providers: [ LetterService, ChatService, WebSocketService ],
})
export class AppModule {}