import zipfile
from dataclasses import dataclass
from pathlib import Path
import typing as tp

import pytest

from .simple_selects import DataBaseHandler


@pytest.fixture(scope="session")
def handler() -> tp.Generator[DataBaseHandler, None, None]:
    with zipfile.ZipFile(Path(__file__).parent / 'chinook.zip', 'r') as zip_ref:
        zip_ref.extractall(Path(__file__).parent)
    handler = DataBaseHandler(str(Path(__file__).parent / 'chinook.db'))
    try:
        yield handler
    finally:
        handler.teardown()
        (Path(__file__).parent / 'chinook.db').unlink()


@dataclass
class TrackByTypes:
    media_types: tp.Sequence[str]
    results: tp.Sequence[tuple[str]]
    number_of_tracks: int


@dataclass
class TracksByPlaylistName:
    name_needle: str
    results: tp.Sequence[tuple[str, str]]


TrackByGenresCases = [
    TrackByTypes(
        media_types=['Metal'],
        results=[('The Hellion',), ('Soldier Side - Intro',), ('My World',), ('The Awakening',), ('Bite The Bullet',), ('FX',), ('Intro',), ("This Cocaine Makes Me Feel Like I'm On This Song",), ('Cigaro',), ('Stone Cold Crazy',)],  # noqa
        number_of_tracks=10
    ),
    TrackByTypes(
        media_types=['Reggae', 'Blues'],
        results=[('Too Many Ways (Alternate)',), ('She Suits Me To A Tee',), ('First Time I Met The Blues',), ('Travis Walk',), ("The House Is Rockin'",), ('Scratch-N-Sniff',), ('Badge',), ('Let Me Love You Baby',), ('Keep It To Myself (Aka Keep It To Yourself)',), ('Strange Brew',), ('Pensamento',), ('I Feel Free',), ('Let Me Love You Baby',), ('Doutor',), ('Promises',)],  # noqa
        number_of_tracks=15
    ),
    TrackByTypes(
        media_types=['Comedy', 'Comedy'],
        results=[('Product Recall',), ('Safety Training',), ("Phyllis's Wedding",), ('Back from Vacation',), ('Ben Franklin',), ('Cocktails',), ('The Convict',), ('Traveling Salesmen',), ('Business School',), ('Beach Games',), ("Producer's Cut: The Return",), ('The Return',), ("Women's Appreciation",), ('The Negotiation',), ('Branch Closing',), ('A Benihana Christmas, Pts. 1 & 2',), ('The Job',)],  # noqa
        number_of_tracks=25
    ),
    TrackByTypes(
        media_types=['unexistent genre', 'yet another'],
        results=[],
        number_of_tracks=100
    )
]

TracksPlaylistsCases = [
    TracksByPlaylistName(
        name_needle='Metal',
        results=[('For Those About To Rock (We Salute You)', 'Heavy Metal Classic'), ('Balls to the Wall', 'Heavy Metal Classic'), ('Fast As a Shark', 'Heavy Metal Classic'), ('Restless and Wild', 'Heavy Metal Classic'), ('Princess of the Dawn', 'Heavy Metal Classic'), ('N.I.B.', 'Heavy Metal Classic'), ('Supernaut', 'Heavy Metal Classic'), ('Wrathchild', 'Heavy Metal Classic'), ('Killers', 'Heavy Metal Classic'), ('Where Eagles Dare', 'Heavy Metal Classic'), ('2 Minutes To Midnight', 'Heavy Metal Classic'), ('Wasted Years', 'Heavy Metal Classic'), ('Run to the Hills', 'Heavy Metal Classic'), ('Enter Sandman', 'Heavy Metal Classic'), ('The Four Horsemen', 'Heavy Metal Classic'), ('Seek & Destroy', 'Heavy Metal Classic'), ('Master Of Puppets', 'Heavy Metal Classic'), ('For Whom The Bell Tolls', 'Heavy Metal Classic'), ('Creeping Death', 'Heavy Metal Classic'), ('Ace Of Spades', 'Heavy Metal Classic'), ('Live To Win', 'Heavy Metal Classic'), ('Looks That Kill', 'Heavy Metal Classic'), ("I Don't Know", 'Heavy Metal Classic'), ('Crazy Train', 'Heavy Metal Classic'), ('Flying High Again', 'Heavy Metal Classic'), ('The Zoo', 'Heavy Metal Classic')]  # noqa
    ),
    TracksByPlaylistName(
        name_needle='Classical 101',
        results=[('Intoitus: Adorate Deum', 'Classical 101 - The Basics'), ('Miserere mei, Deus', 'Classical 101 - The Basics'), ('Canon and Gigue in D Major: I. Canon', 'Classical 101 - The Basics'), ('Concerto No. 1 in E Major, RV 269 "Spring": I. Allegro', 'Classical 101 - The Basics'), ('Concerto for 2 Violins in D Minor, BWV 1043: I. Vivace', 'Classical 101 - The Basics'), ('Aria Mit 30 Veränderungen, BWV 988 "Goldberg Variations": Aria', 'Classical 101 - The Basics'), ('Suite for Solo Cello No. 1 in G Major, BWV 1007: I. Prélude', 'Classical 101 - The Basics'), ('The Messiah: Behold, I Tell You a Mystery... The Trumpet Shall Sound', 'Classical 101 - The Basics'), ('Solomon HWV 67: The Arrival of the Queen of Sheba', 'Classical 101 - The Basics'), ('"Eine Kleine Nachtmusik" Serenade In G, K. 525: I. Allegro', 'Classical 101 - The Basics'), ('Concerto for Clarinet in A Major, K. 622: II. Adagio', 'Classical 101 - The Basics'), ('Symphony No. 104 in D Major "London": IV. Finale: Spiritoso', 'Classical 101 - The Basics'), ('Symphony No.5 in C Minor: I. Allegro con brio', 'Classical 101 - The Basics'), ('Ave Maria', 'Classical 101 - The Basics'), ('Nabucco: Chorus, "Va, Pensiero, Sull\'ali Dorate"', 'Classical 101 - The Basics'), ('Die Walküre: The Ride of the Valkyries', 'Classical 101 - The Basics'), ('Requiem, Op.48: 4. Pie Jesu', 'Classical 101 - The Basics'), ('The Nutcracker, Op. 71a, Act II: Scene 14: Pas de deux: Dance of the Prince & the Sugar-Plum Fairy', 'Classical 101 - The Basics'), ('Nimrod (Adagio) from Variations On an Original Theme, Op. 36 "Enigma"', 'Classical 101 - The Basics'), ('Madama Butterfly: Un Bel Dì Vedremo', 'Classical 101 - The Basics'), ('Jupiter, the Bringer of Jollity', 'Classical 101 - The Basics'), ('Turandot, Act III, Nessun dorma!', 'Classical 101 - The Basics'), ('Adagio for Strings from the String Quartet, Op. 11', 'Classical 101 - The Basics'), ('Carmina Burana: O Fortuna', 'Classical 101 - The Basics'), ('Fanfare for the Common Man', 'Classical 101 - The Basics'), ('Toccata and Fugue in D Minor, BWV 565: I. Toccata', 'Classical 101 - Next Steps'), ('Symphony No.1 in D Major, Op.25 "Classical", Allegro Con Brio', 'Classical 101 - Next Steps'), ("Scheherazade, Op. 35: I. The Sea and Sindbad's Ship", 'Classical 101 - Next Steps'), ('Concerto No.2 in F Major, BWV1047, I. Allegro', 'Classical 101 - Next Steps'), ('Concerto for Piano No. 2 in F Minor, Op. 21: II. Larghetto', 'Classical 101 - Next Steps'), ('Cavalleria Rusticana \\ Act \\ Intermezzo Sinfonico', 'Classical 101 - Next Steps'), ('Karelia Suite, Op.11: 2. Ballade (Tempo Di Menuetto)', 'Classical 101 - Next Steps'), ('Piano Sonata No. 14 in C Sharp Minor, Op. 27, No. 2, "Moonlight": I. Adagio sostenuto', 'Classical 101 - Next Steps'), ('Fantasia On Greensleeves', 'Classical 101 - Next Steps'), ('Das Lied Von Der Erde, Von Der Jugend', 'Classical 101 - Next Steps'), ('Concerto for Cello and Orchestra in E minor, Op. 85: I. Adagio - Moderato', 'Classical 101 - Next Steps'), ('Two Fanfares for Orchestra: II. Short Ride in a Fast Machine', 'Classical 101 - Next Steps'), ("Wellington's Victory or the Battle Symphony, Op.91: 2. Symphony of Triumph", 'Classical 101 - Next Steps'), ('Missa Papae Marcelli: Kyrie', 'Classical 101 - Next Steps'), ('Romeo et Juliette: No. 11 - Danse des Chevaliers', 'Classical 101 - Next Steps'), ('On the Beautiful Blue Danube', 'Classical 101 - Next Steps'), ("Symphonie Fantastique, Op. 14: V. Songe d'une nuit du sabbat", 'Classical 101 - Next Steps'), ('Carmen: Overture', 'Classical 101 - Next Steps'), ('Lamentations of Jeremiah, First Set \\ Incipit Lamentatio', 'Classical 101 - Next Steps'), ('Music for the Royal Fireworks, HWV351 (1749): La Réjouissance', 'Classical 101 - Next Steps'), ('Peer Gynt Suite No.1, Op.46: 1. Morning Mood', 'Classical 101 - Next Steps'), ('Die Zauberflöte, K.620: "Der Hölle Rache Kocht in Meinem Herze"', 'Classical 101 - Next Steps'), ('SCRIABIN: Prelude in B Major, Op. 11, No. 11', 'Classical 101 - Next Steps'), ('Pavan, Lachrimae Antiquae', 'Classical 101 - Next Steps'), ('Symphony No. 41 in C Major, K. 551, "Jupiter": IV. Molto allegro', 'Classical 101 - Next Steps'), ('Prometheus Overture, Op. 43', 'Classical 101 - Deep Cuts'), ('Sonata for Solo Violin: IV: Presto', 'Classical 101 - Deep Cuts'), ("A Midsummer Night's Dream, Op.61 Incidental Music: No.7 Notturno", 'Classical 101 - Deep Cuts'), ('Suite No. 3 in D, BWV 1068: III. Gavotte I & II', 'Classical 101 - Deep Cuts'), ('Concert pour 4 Parties de V**les, H. 545: I. Prelude', 'Classical 101 - Deep Cuts'), ('Adios nonino', 'Classical 101 - Deep Cuts'), ('Symphony No. 3 Op. 36 for Orchestra and Soprano "Symfonia Piesni Zalosnych" \\ Lento E Largo - Tranquillissimo', 'Classical 101 - Deep Cuts'), ('Act IV, Symphony', 'Classical 101 - Deep Cuts'), ('3 Gymnopédies: No.1 - Lent Et Grave, No.3 - Lent Et Douloureux', 'Classical 101 - Deep Cuts'), ('Music for the Funeral of Queen Mary: VI. "Thou Knowest, Lord, the Secrets of Our Hearts"', 'Classical 101 - Deep Cuts'), ('Symphony No. 2: III. Allegro vivace', 'Classical 101 - Deep Cuts'), ('Partita in E Major, BWV 1006A: I. Prelude', 'Classical 101 - Deep Cuts'), ('Le Sacre Du Printemps: I.iv. Spring Rounds', 'Classical 101 - Deep Cuts'), ('Sing Joyfully', 'Classical 101 - Deep Cuts'), ('Metopes, Op. 29: Calypso', 'Classical 101 - Deep Cuts'), ('Symphony No. 2, Op. 16 -  "The Four Temperaments": II. Allegro Comodo e Flemmatico', 'Classical 101 - Deep Cuts'), ('24 Caprices, Op. 1, No. 24, for Solo Violin, in A Minor', 'Classical 101 - Deep Cuts'), ('Étude 1, In C Major - Preludio (Presto) - Liszt', 'Classical 101 - Deep Cuts'), ('Erlkonig, D.328', 'Classical 101 - Deep Cuts'), ('Concerto for Violin, Strings and Continuo in G Major, Op. 3, No. 9: I. Allegro', 'Classical 101 - Deep Cuts'), ('Pini Di Roma (Pinien Von Rom) \\ I Pini Della Via Appia', 'Classical 101 - Deep Cuts'), ('String Quartet No. 12 in C Minor, D. 703 "Quartettsatz": II. Andante - Allegro assai', 'Classical 101 - Deep Cuts'), ("L'orfeo, Act 3, Sinfonia (Orchestra)", 'Classical 101 - Deep Cuts'), ('Quintet for Horn, Violin, 2 Violas, and Cello in E Flat Major, K. 407/386c: III. Allegro', 'Classical 101 - Deep Cuts'), ('Koyaanisqatsi', 'Classical 101 - Deep Cuts')]  # noqa
    ),
    TracksByPlaylistName(
        name_needle='should be empty',
        results=[]
    ),
    TracksByPlaylistName(
        name_needle='%\'OR 1=1 OR Name LIKE\'%haha, gotcha!',
        results=[]
    )
]


def test_most_expensive_tracks(handler: DataBaseHandler) -> None:
    res = handler.get_most_expensive_track_names(10)
    assert res == [('Battlestar Galactica: The Story So Far',), ('Occupation / Precipice',), ('Exodus, Pt. 1',), ('Exodus, Pt. 2',), ('Collaborators',), ('Torn',), ('A Measure of Salvation',), ('Hero',), ('Unfinished Business',), ('The Passage',)]  # noqa


@pytest.mark.parametrize('case', TrackByGenresCases)
def test_track_by_type(handler: DataBaseHandler, case: TrackByTypes) -> None:
    result = handler.get_tracks_of_given_genres(case.media_types, case.number_of_tracks)
    assert result == case.results


@pytest.mark.parametrize('case', TracksPlaylistsCases)
def test_track_by_playlist_name(handler: DataBaseHandler, case: TracksByPlaylistName) -> None:
    result = handler.get_tracks_that_belong_to_playlist_found_by_name(case.name_needle)
    assert result == case.results
