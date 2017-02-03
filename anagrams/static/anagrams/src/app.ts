//our root app component
import {Component, NgModule, OnInit} from '@angular/core'

// Modules
import { BrowserModule } from '@angular/platform-browser'
import { FormsModule }   from '@angular/forms';

// Services
import { LetterService } from './letter.service';
import { ChatService } from './chat.service';
import { WebSocketService } from './websocket.service';

// Components
import { CreateMessage } from './create-message.component';
import { ChatComponent } from './chat.component';


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

@NgModule({
  imports: [ BrowserModule, FormsModule ],
  declarations: [ AppComponent, ChatComponent, CreateMessage ],
  bootstrap: [ AppComponent ],
  providers: [ LetterService, ChatService, WebSocketService ],
})
export class AppModule {}