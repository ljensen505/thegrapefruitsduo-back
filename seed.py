from dotenv import load_dotenv

from app.db import connect_db
from app.models import Musician, User

margarite: Musician = Musician(
    name="Margarite Waddell",
    bio="French hornist Margarite Waddell holds positions with the Eugene Symphony, Sarasota Opera, Boise Philharmonic, Rogue Valley Symphony, and Newport Symphony. As a freelancer, Margarite has played with ensembles throughout the West Coast including the Oregon Symphony, Portland Opera, Santa Rosa Symphony, Marin Symphony, and Symphony San Jose. She has performed with popular artists such as The Who, Josh Groban, and Sarah Brightman. Margarite can be heard on Kamyar Mohajer’s album “Pictures of the Hidden” on Navona Records. She appeared as a soloist with the Silicon Valley Philharmonic in 2016. Margarite cares deeply about music education and has taught private lessons, sectionals, and masterclasses throughout the Bay Area, Southwestern Oregon, Eugene, and Corvallis since 2013. She also performed in the San Francisco Symphony's Adventures in Music program for the 2016-2017 season. Margarite received her bachelor’s degree from the University of Oregon, and her master’s degree from the San Francisco Conservatory of Music.",
    headshot_id="margarite_copy_a4oxty",
)

coco: Musician = Musician(
    name="Coco Bender",
    bio="Coco Bender is a pianist residing in the Pacific Northwest. She recently performed with Cascadia Composers, recorded original film scores by Portland composer Christina Rusnak for the Pioneers: First Woman Filmmakers Project, and during the pandemic presented a series of outdoor recitals featuring music by H. Leslie Adams, William Grant Still, Bartok, and others. Coco is a founding member of the Eugene based horn and piano duo, The Grapefruits, as well as a co-artistic director and musical director of an all-women circus, Girl Circus. She has taken master classes with Inna Faliks, Tamara Stefanovich, and Dr. William Chapman Nyaho. Coco currently studies with Dr. Thomas Otten. In addition to performing regularly, she teaches a large studio of students in the Pacific Northwest, from Seattle WA to Eugene OR. Coco was the accompanist for Portland treble choir Aurora Chorus, during their 2021-2022, season under the conductorship of Kathleen Hollingsworth, Margaret Green, Betty Busch, and Joan Szymko.",
    headshot_id="coco_copy_jywbxm",
)

coco_user: User = User(
    auth0_id="google-oauth2|110044702811943457315",
    email="cocobender.piano@gmail.com",
    name="Coco Bender",
)

margarite_user: User = User(
    auth0_id="google-oauth2|109109812131608294748",
    email="mgwaddell@gmail.com",
    name="Margarite Waddell",
)

lucas_user: User = User(
    auth0_id="google-oauth2|103593642272149633528",
    email="lucas.p.jensen10@gmail.com",
    name="Lucas Jensen",
)

tgd_user: User = User(
    auth0_id="google-oauth2|116470512398914344676",
    email="thegrapefruitsduo@gmail.com",
    name="The Grapefruits Duo",
)


def seed():
    print("Seeding database")
    add_musicians()
    add_users()


def add_users():
    print("Adding users")
    table = "users"
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(
        f"DROP TABLE IF EXISTS {table};",
    )
    cursor.execute(
        f"""
        CREATE TABLE {table} (
            id INT NOT NULL AUTO_INCREMENT,
            auth0_id VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            name VARCHAR(255) NOT NULL,
            PRIMARY KEY (id)
        );
        """
    )
    for u in [coco_user, margarite_user, lucas_user, tgd_user]:
        cursor.execute(
            f"INSERT INTO {table} (auth0_id, email, name) VALUES (%s, %s, %s);",
            (u.auth0_id, u.email, u.name),
        )

    db.commit()
    cursor.close()


def add_musicians():
    print("Adding musicians")
    table = "musicians"
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(
        f"DROP TABLE IF EXISTS {table};",
    )
    cursor.execute(
        f"""
        CREATE TABLE {table} (
            id INT NOT NULL AUTO_INCREMENT,
            name VARCHAR(255) NOT NULL,
            bio TEXT NOT NULL,
            headshot_id VARCHAR(255) NOT NULL,
            PRIMARY KEY (id)
        );
        """
    )
    for m in [margarite, coco]:
        cursor.execute(
            f"INSERT INTO {table} (name, bio, headshot_id) VALUES (%s, %s, %s);",
            (m.name, m.bio, m.headshot_id),
        )

    db.commit()
    cursor.close()


if __name__ == "__main__":
    load_dotenv()
    seed()
