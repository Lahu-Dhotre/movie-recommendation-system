import os
import sqlalchemy
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

# Path to u.item file
U_ITEM_PATH = os.path.join(os.path.dirname(__file__), 'ml-100k', 'u.item')

# Create SQLAlchemy engine
engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# Movie table columns: id, title, overview, poster_url (add more if needed)

def parse_u_item_line(line):
    # u.item format: movie_id|title|release_date|video_release_date|IMDb_URL|genre1|...|genreN
    parts = line.strip().split('|')
    movie_id = int(parts[0])
    title = parts[1]
    overview = ''  # No overview in u.item
    poster_url = ''  # No poster_url in u.item
    return {
        'id': movie_id,
        'title': title,
        'overview': overview,
        'poster_url': poster_url
    }

def import_movies():
    with engine.connect() as conn:
        with open(U_ITEM_PATH, encoding='ISO-8859-1') as f:
            for line in f:
                movie = parse_u_item_line(line)
                # Check if movie already exists
                result = conn.execute(text("SELECT id FROM movies WHERE id = :id"), {'id': movie['id']})
                if result.fetchone():
                    continue  # Skip duplicates
                # Insert movie
                conn.execute(text("""
                    INSERT INTO movies (id, title, overview, poster_url)
                    VALUES (:id, :title, :overview, :poster_url)
                """), movie)
        conn.commit()
    print("Import completed.")

if __name__ == "__main__":
    import_movies()
