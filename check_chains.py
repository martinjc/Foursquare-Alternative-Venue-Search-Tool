from tables import *
from chain_decision import is_chain
from sqlalchemy.orm import sessionmaker, joinedload_all

Session = sessionmaker(bind=engine)
session = Session()

venues = session.query(Venue).options(joinedload_all('category')).all()

with open("venues_chains.csv", "w") as venue_file:

    for venue in venues[:1000]:

        chain = is_chain(venue.foursq_id)
        print "%s, %s" % (venue.name, chain)

        venue_file.write("%s,%s,%s\n" %(venue.foursq_id, venue.name, chain))

