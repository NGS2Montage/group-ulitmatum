import { Injectable } from '@angular/core';
import { Observable, Subject } from 'rxjs/Rx';
import { WebSocketService } from './websocket.service';

const CHAT_URL = 'ws://' + window.location.host + '/anagrams';

export interface WebSocketMessage {
    type: string,
    payload: Any
}

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
            .map((response: MessageEvent): WebSocketMessage => {
                console.log("hot off the socket", response);
                let data = JSON.parse(response.data);
                return {
                    type: data.type,
                    payload: data
                }
            })
            .filter((message: WebSocketMessage): boolean => {
                return message.type === "chat";
            })
            .map((message: WebSocketMessage): Message => {
                return {
                    author: message.payload.user,
                    message: message.payload.message,
                    newDate : message.payload.date
                };
            });
    }
} // end class ChatService