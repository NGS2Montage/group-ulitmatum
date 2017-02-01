import { Injectable } from '@angular/core';

@Injectable()
export class LetterService {
  getHeroes(): Promise<string[]> {
    return Promise.resolve(["T", "A", "C"]);
  }
}
