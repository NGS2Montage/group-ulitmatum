// Modules
import { NgModule } from '@angular/core'
import { BrowserModule } from '@angular/platform-browser'
import { FormsModule }   from '@angular/forms';

// Services
import { LetterService } from './services/letter.service';
import { ChatService } from './services/chat.service';
import { WebSocketService } from './services/websocket.service';

// Components
import { AppComponent } from './app.component';
import { CreateMessage } from './components/create-message.component';
import { ChatComponent } from './components/chat.component';

@NgModule({
  imports: [ BrowserModule, FormsModule ],
  declarations: [ AppComponent, ChatComponent, CreateMessage ],
  bootstrap: [ AppComponent ],
  providers: [ LetterService, ChatService, WebSocketService ],
})
export class AppModule {}