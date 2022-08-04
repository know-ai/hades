from pyhades import PyHades
from pyhades.tags import CVTEngine

dbfile = "app.db"
app = PyHades()
app.set_mode('Development')
app.drop_db(dbfile=dbfile)
app.set_db(dbfile=dbfile)
db_worker = app.init_db()
tag_engine = CVTEngine()