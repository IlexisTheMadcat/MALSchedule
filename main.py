from classes import MALSchedule

if __name__ == "__main__":
    scheduler = MALSchedule()
    schedule = scheduler.request_schedule()
    for day, animes in schedule.items():
        print(f"-------------------- {day} --------------------")
        for anime in animes:
            print(
                f"Name: {anime.name}\n"
                f"Producer: {anime.producer}\n"
                f"Tags: {', '.join(anime.tags)}\n"
                f"Rating: {anime.score}/10\n"
                f"Metadata: {', '.join([key+': '+value for key, value in anime.metadata.items()])}\n"
                f"Viewer discretion: {anime.estimated_rating}\n"
                f"\n"
                f"Synopsis:\n"
                f"{anime.synopsis}\n"
                f"Image url: {anime.image_url}\n"
                f"----------\n"
                f"\n"
            )

    anime = schedule["Thursday"][0]  # Currently Komi Can't Communicate
    print(
        f"# SINGLE ANIME\n"
        f"Name: {anime.name}\n"
        f"Producer: {anime.producer}\n"
        f"Tags: {', '.join(anime.tags)}\n"
        f"Rating: {anime.score}/10\n"
        f"Metadata: {', '.join([key+': '+value for key, value in anime.metadata.items()])}\n"
        f"Viewer discretion: {anime.estimated_rating}\n"
        f"\n"
        f"Synopsis:\n"
        f"{anime.synopsis}\n"
        f"Image url: {anime.image_url}\n"
        f"----------\n"
        f"\n"
    )