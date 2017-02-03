import { Injectable } from '@angular/core';
import { Observable, Subject } from 'rxjs/Rx';
import { WebSocketService } from './websocket.service';

const CHAT_URL = 'ws://' + window.location.host + '/anagrams';

export interface Message {
    author: string,
    message: string,
    newDate?: string
}

@Injectable()
export class ChatService {
    public messages: Subject<Message>;

    constructor(wsService: WebSocketService) {
        this.messages = <Subject<Message>>wsService
            .connect(CHAT_URL)
            .map((response: MessageEvent): Message => {
                console.log("here is a response?", response);
                // let data = JSON.parse(response.data);
                return {
                    author: 'author', //data.author,
                    message: response.data,
                    newDate : 'date' //data.newDate
                }
            });
    }
} // end class ChatService