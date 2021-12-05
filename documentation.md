#Installation
MALSchedule is currently not on PIP, so you must clone the folder into your working directory.
`git clone https://github.com/SUPERMECHM500/MALSchedule`

Now you can get the current week's release schedule. You will require an internet connection.
```py
from MALSchedule import MALSchedule

scheduler = MALSchedule()
schedule = scheduler.request_schedule()
```

`schedule` is now a dictionary of lists. Each key represents the day of the week, starting with "Monday", "Tuesday", etc. Two other keys are also present: "Other" and "Unknown".
```json
{
     /* Lists of Anime */
    "Monday": [...],
    "Tuesday": [...],
    "Wednesday": [...],
    "Thursday": [...],
    "Friday": [...],
    "Saturday": [...],
    "Sunday": [...],
    "Other": [...],
    "Unknown": [...],
}
```

Each key has a list for its value, with each item in the list representing the following dataclass in `mal_members` (high to low) order:
```py
@dataclass
class Anime:
    name: str  
    # The name of the anime.
    
    producer: str  
    # The producer/studio of the anime.

    tags: list  
    # The tags associated with the anime, according to MAL.

    image_url: str  
    # The cover image for the anime.

    score: float  
    # The score associated with the anime. The value ranges from 0-10. 
    # Score is based on MAL users.

    mal_members: int  
    # The number of MAL members that watch or like this anime.

    synopsis: str  
    # The description of this anime, according to MAL.

    metadata: dict  
    # The metadata associated with this anime. 
    # Can contain various attributes, including Demographic, Theme, Licensor (where you can watch it), etc. 
    # Not all are available therefore not present.

    estimated_rating: str
    # Represents a view rating as if it were rated by the MPAA.
    # G (General Audience); If `metadata["Demographic"]` is for "Kids".
    # PG (Parental Guidence); If none of the other determining factors are met.
    # PG-13 (Strong Parental Guidence); If "Romance" is present in `tags`.
    # R (Restricted); If "Ecchi" is present in `tags` .
    # NC-17 (Adults Only); If "Hentai" or "Erotica" are present in `tags`.
```