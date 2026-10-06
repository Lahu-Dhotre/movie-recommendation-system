import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';


@Component({
  selector: 'app-user-profile',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './user-profile.component.html',
  styleUrls: ['./user-profile.component.scss']
})
export class UserProfileComponent {
  users: { id: number; name: string; img: string }[] = [];

  constructor(private router: Router, private http: HttpClient) {}

  fetchUsers(): void {
    
  this.http.get<any[]>('http://localhost:8000/api/v1/users').subscribe(
    
    (response) => {
      console.log('Fetched users:', response);
      // Map the response to match the existing structure
      this.users = response.map(user => {
       
        return {
          id: user.user_id || user.id, // Use user_id if available, fallback to id
          name: user.name,
          img: user.img_url || 'https://via.placeholder.com/150' // Fallback image if img_url is null
        };
      }).filter(user => user !== null); // Filter out null values
      console.log('Mapped users:', this.users);
    },
    (error) => {
      console.error('Error fetching users:', error);
    }
  );
  }

   ngOnInit(): void {
    this.fetchUsers();
  }
  
  selectUser(user: { id: number; name: string; img: string } | undefined): void {
    console.log('Selected User ID:', user?.id);
    console.log('Selected Name:', user?.name);

    if (!user || !user.id) {
      console.error('User or User ID is undefined. Cannot select user.');
      return;
    }

    const selectedUser = { id: user.id, name: user.name, img: user.img };

    // Store the entire user object in localStorage
    localStorage.setItem('selectedUser', JSON.stringify(selectedUser));

    // Store the user ID separately in localStorage
    localStorage.setItem('selectedUserId', user.id.toString());

    console.log('Selected User ID:', user.id);

    // Navigate to the movies page
    this.router.navigate(['/movies']);
  }
}
