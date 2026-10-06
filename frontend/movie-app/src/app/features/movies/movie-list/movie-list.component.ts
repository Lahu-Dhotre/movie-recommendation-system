import { ChangeDetectionStrategy, Component, Signal, computed, effect, inject, signal, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatIconModule } from '@angular/material/icon';
import { MovieService } from '../../../core/services/movie.service';
import { Movie } from '../../../core/models/movie.model';
import { HttpClient } from '@angular/common/http';


@Component({
  selector: 'app-movie-list',
  standalone: true,
  imports: [CommonModule, MatCardModule, MatToolbarModule, MatProgressSpinnerModule, MatIconModule],
  templateUrl: './movie-list.component.html',
  styleUrls: ['./movie-list.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class MovieListComponent implements OnInit {
  moviesToWatch: any[] = []; // Initialize as an empty array
  topPicks: { id: number; title: string; overview: string; poster_url: string }[] = []; // Define the structure of topPicks explicitly

  selectedUser: { id: number; name: string; img: string } | null = null;

  // Store ratings in-memory and in localStorage for persistence per user
  private ratings: { [movieId: number]: number } = {};

  readonly loading = signal(true); // Re-added the loading signal to track loading state

  constructor(private router: Router, private http: HttpClient) {
    // Get selected user from localStorage
    const userStr = localStorage.getItem('selectedUser');
    if (userStr) {
      try {
        this.selectedUser = JSON.parse(userStr);
      } catch {
        this.selectedUser = null;
      }
    }
    this.loadMoviesFromSession();
  }

  ngOnInit(): void {
    // Fetch movies only once during the ngOnInit lifecycle
    this.fetchMovies();
    this.fetchTopPicks();
  }

  signOut() {
    localStorage.removeItem('selectedUser');
    this.router.navigate(['/profile']);
  }

  fetchMovies(): void {
    this.http.get<any[]>('http://localhost:8000/api/v1/movies/').subscribe(
      (response) => {
        console.log('API Response:', response);
        if (response && Array.isArray(response) && response.length > 0) {
          this.moviesToWatch = response.map(movie => ({
            movie_id: movie.movie_id || movie.id, // Ensure compatibility with both movie_id and id fields
            title: movie.title,
            overview: movie.overview,
            poster_url: movie.poster_url || 'https://via.placeholder.com/150'
          }));
          console.log('Mapped Movies:', this.moviesToWatch);

          // Store moviesToWatch in session storage
          //sessionStorage.setItem('moviesToWatch', JSON.stringify(this.moviesToWatch));
        } else {
          console.warn('API returned an empty or invalid response.');
        }
      },
      (error) => {
        console.error('Error fetching movies:', error);
      }
    );
  }

 fetchTopPicks(): void {
  this.http.get<any>('http://localhost:8000/api/v1/recommendations/11').subscribe(
    (response) => {
      console.log('Top Picks API Response:', response);
      if (response && Array.isArray(response.recommendations) && response.recommendations.length > 0) {
        this.topPicks = response.recommendations.slice(0, 5).map((movie: any) => ({
          id: movie.movie_id || movie.id,
          title: movie.title,
          overview: movie.overview,
          poster_url: movie.poster_url || 'https://via.placeholder.com/150'
        }));
        
      }
    },
    (error) => {
      console.error('Error fetching top picks:', error);
    }
  );
}

  loadMoviesFromSession(): void {
    const storedMovies = sessionStorage.getItem('moviesToWatch');
    if (storedMovies) {
      try {
        this.moviesToWatch = JSON.parse(storedMovies);
        console.log('Loaded movies from session:', this.moviesToWatch);
      } catch (error) {
        console.error('Error parsing movies from session storage:', error);
      }
    }

    // Load topPicks from session storage
    const storedTopPicks = sessionStorage.getItem('topPicks');
    if (storedTopPicks) {
      try {
        this.topPicks = JSON.parse(storedTopPicks);
        console.log('Loaded top picks from session:', this.topPicks);
      } catch (error) {
        console.error('Error parsing top picks from session storage:', error);
      }
    }
  }

addRating(movieId: number, rating: number): void {
  if (!this.selectedUser || !this.selectedUser.id) {
    console.error('No user selected or user ID is missing. Cannot add rating.');
    return;
  }

  const payload = {
    user_id: this.selectedUser.id, // Include user_id
    movie_id: movieId,            // Include movie_id
    rating                        // Include rating
  };
  
  console.log('Payload to be sent:', payload); // Log the payload for debugging

  this.http.post('http://localhost:8000/api/v1/movie_ratings', payload).subscribe(
    () => {
      console.log(`Rating added successfully for movie ID ${movieId}`);
    },
    (error) => {
      console.error('Error adding rating:', error);
    }
  );
 }
}

