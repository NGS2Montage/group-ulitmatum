import { Injectable } from '@angular/core';

@Injectable()
export class LetterService {
  getLetters(): Promise<string[]> {
    return Promise.resolve(["T", "A", "C", "H"]);
  }
}