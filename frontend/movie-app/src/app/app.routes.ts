
import { Routes } from '@angular/router';
import { MovieListComponent } from './features/movies/movie-list/movie-list.component';
import { LoginComponent } from './features/auth/login.component';
import { UserProfileComponent } from './features/profile/user-profile.component';

export const routes: Routes = [
	{ path: '', component: LoginComponent },
	{ path: 'profile', component: UserProfileComponent },
	{ path: 'movies', component: MovieListComponent },
	{ path: '**', redirectTo: '' },
];
