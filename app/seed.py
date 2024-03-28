from datetime import datetime

from dotenv import load_dotenv

from app.db.conn import connect_db
from app.models.event import EVENT_TABLE, Event, InsertionEvent, NewEvent
from app.models.group import GROUP_TABLE, Group
from app.models.musician import MUSICIAN_TABLE, NewMusician
from app.models.user import USER_TABLE, User

margarite: NewMusician = NewMusician(
    name="Margarite Waddell",
    bio="French hornist Margarite Waddell holds positions with the Eugene Symphony, Sarasota Opera, Boise Philharmonic, Rogue Valley Symphony, and Newport Symphony. As a freelancer, Margarite has played with ensembles throughout the West Coast including the Oregon Symphony, Portland Opera, Santa Rosa Symphony, Marin Symphony, and Symphony San Jose. She has performed with popular artists such as The Who, Josh Groban, and Sarah Brightman. Margarite can be heard on Kamyar Mohajer’s album “Pictures of the Hidden” on Navona Records. She appeared as a soloist with the Silicon Valley Philharmonic in 2016. Margarite cares deeply about music education and has taught private lessons, sectionals, and masterclasses throughout the Bay Area, Southwestern Oregon, Eugene, and Corvallis since 2013. She also performed in the San Francisco Symphony's Adventures in Music program for the 2016-2017 season. Margarite received her bachelor’s degree from the University of Oregon, and her master’s degree from the San Francisco Conservatory of Music.",
    headshot_id="zlpkcrvbdsicgj7qtslx",
)

coco: NewMusician = NewMusician(
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

test_user: User = User(
    auth0_id="WQrIbh4gPU7ypcMKxxQA18eBGCOGfNxH@clients",
    email="test@test.com",
    name="Test User",
)

tgd: Group = Group(
    bio="The Grapefruits, comprising of Coco Bender, piano, and Margarite Waddell, french horn, are a contemporary classical music duo. They perform frequently through out the PNW with the goal presenting traditional classical french horn repertoire, new 20th century works, and commissioned works by PNW composers. Our upcoming concert series features works by Jane Vignery, Tara Islas, Gliere, Prokofiev, and Oregon Composers Christina Rusnak and Mark Jacobs.",
    name="The Grapefruits Duo",
)

sample_event: InsertionEvent = InsertionEvent(
    name="Sample Event",
    location="Sample Location",
    description="Sample Description",
    time=datetime(2022, 1, 1, 12, 0, 0),
    poster="The_Grapefruits_Present_qhng6y",
)


def seed():
    confirmation = input(
        "Are you sure you want to seed the database? Date will be lost. [Y/n]: "
    )
    if confirmation.lower() not in ["y", "yes", ""]:
        print("Exiting")
        return
    print("Seeding database")
    add_musicians()
    add_users()
    add_group()
    add_events()


def add_group():
    print("Adding group")
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(
        f"DROP TABLE IF EXISTS {GROUP_TABLE};",
    )
    cursor.execute(
        f"""
        CREATE TABLE {GROUP_TABLE} (
            id INT NOT NULL AUTO_INCREMENT,
            name VARCHAR(255) NOT NULL,
            bio TEXT NOT NULL,
            PRIMARY KEY (id)
        );
        """
    )
    cursor.execute(
        f"INSERT INTO {GROUP_TABLE} (name, bio) VALUES (%s, %s);",
        (tgd.name, tgd.bio),
    )
    db.commit()
    cursor.close()


def add_users():
    print("Adding users")
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(
        f"DROP TABLE IF EXISTS {USER_TABLE};",
    )
    cursor.execute(
        f"""
        CREATE TABLE {USER_TABLE} (
            id INT NOT NULL AUTO_INCREMENT,
            auth0_id VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            name VARCHAR(255) NOT NULL,
            PRIMARY KEY (id)
        );
        """
    )
    for u in [coco_user, margarite_user, lucas_user, tgd_user, test_user]:
        cursor.execute(
            f"INSERT INTO {USER_TABLE} (auth0_id, email, name) VALUES (%s, %s, %s);",
            (u.auth0_id, u.email, u.name),
        )

    db.commit()
    cursor.close()


def add_musicians():
    print("Adding musicians")

    db = connect_db()
    cursor = db.cursor()
    cursor.execute(
        f"DROP TABLE IF EXISTS {MUSICIAN_TABLE};",
    )
    cursor.execute(
        f"""
        CREATE TABLE {MUSICIAN_TABLE} (
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
            f"INSERT INTO {MUSICIAN_TABLE} (name, bio, headshot_id) VALUES (%s, %s, %s);",
            (m.name, m.bio, m.headshot_id),
        )

    db.commit()
    cursor.close()


def add_events():
    print("Adding events")

    db = connect_db()
    cursor = db.cursor()
    cursor.execute(
        f"DROP TABLE IF EXISTS {EVENT_TABLE};",
    )
    cursor.execute(
        f"""
        CREATE TABLE {EVENT_TABLE} (
            id INT NOT NULL AUTO_INCREMENT,
            name VARCHAR(255) NOT NULL,
            location VARCHAR(255) NOT NULL,
            description TEXT NOT NULL,
            time DATETIME NOT NULL,
            poster VARCHAR(255) NOT NULL,
            PRIMARY KEY (id)
        );
        """
    )
    cursor.execute(
        f"INSERT INTO {EVENT_TABLE} (name, location, description, time, poster) VALUES (%s, %s, %s, %s, %s);",
        (
            sample_event.name,
            sample_event.location,
            sample_event.description,
            sample_event.time,
            sample_event.poster,
        ),
    )
    db.commit()
    cursor.close()


def main():
    load_dotenv()
    seed()


if __name__ == "__main__":
    main()
