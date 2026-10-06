// Movie interface for our blockbuster UI!
export interface Movie {
  id: number;
  title: string;
  year: number | null;
  genres: string[];
  poster_url: string | null;
  overview: string;
  global_rating: number;
}
