import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Movie } from '../models/movie.model';
import { environment } from '../../../environments/environment';

@Injectable({ providedIn: 'root' })
export class MovieService {
  private http = inject(HttpClient);
  private baseUrl = environment.apiBaseUrl;

  getPopularMovies(): Observable<Movie[]> {
    return this.http.get<Movie[]>(`${this.baseUrl}/movies/popular`);
  }

  getRecommendedMovies(userId: number): Observable<Movie[]> {
    return this.http.get<Movie[]>(`${this.baseUrl}/users/${userId}/recommendations`);
  }
}
