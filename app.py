from uuid import UUID, uuid4
from pony.orm import *


db = Database()

db.bind(provider='sqlite', filename=':memory:')


class Fact(db.Entity):
    """Description of a discrete thing"""
    id = PrimaryKey(UUID, auto=True)
    simple_id = Required(int, unique=True)  # User facing ID
    text = Required(str)  # Text description
    game = Required('Game')  # The game the fact is linked to
    notes = Set('Note')  # Linked notes
    tags = Set('Tag')


class Game(db.Entity):
    id = PrimaryKey(UUID, auto=True)
    name = Required(str, unique=True)
    facts = Set(Fact)
    tasks = Set('Task')


class Tag(db.Entity):
    id = PrimaryKey(UUID, auto=True)
    text = Required(str, unique=True)
    facts = Set(Fact)
    tasks = Set('Task')


class Task(db.Entity):
    id = PrimaryKey(UUID, auto=True)
    simple_id = Required(int, unique=True)
    text = Required(str)
    done = Required(bool, default=False)
    game = Required(Game)
    notes = Set('Note')
    tags = Set(Tag)


class Note(db.Entity):
    id = PrimaryKey(UUID, auto=True)
    text = Optional(str)
    fact = Optional(Fact)
    task = Optional(Task)



db.generate_mapping(create_tables=True)

with db_session as session:
    set_sql_debug(True)

    # Set up a couple of games
    g1 = Game(name="Strahd")
    g2 = Game(name="L5R")

    # Set up some facts
    f1 = Fact(simple_id=1, text="These hills are cursed", game=g1)
    f2 = Fact(simple_id=2, text="Murakami is a drunk", game=g2)

    # Set up some tasks
    t1 = Task(simple_id=1, text="Kill Strahd", game=g1)
    t2 = Task(simple_id=2, text="Survive the upcoming battle", game=g2)

    # Commit
    commit()

    show(g for g in Game)
    show(f for f in Fact)
    show(t for t in Task)
