# Database Handler

To implement a database for CVTEngine is necessary to specify the app mode with the new method *set_mode*.

By default, the app mode is "Development*. If the app mode is *Development* so the database used is SQLite.

For Sqlite Database you must define the db filename with the arg *dbfile* in the method *set_db*.

For Database in production you must define the data base type with *dbtype*. PyHades Support Postgres and MySQL.

Then, once you set the db you must set the tags that you want to log with the method *set_tag*

## SQLite Database

Usage

```python
>>> from pyhades import PyHades, PyHadesStateMachine, State
>>> from pyhades.models import IntegerType
>>> from pyhades.tags import CVTEngine, TagBinding

>>> app = PyHades()
>>> app.set_mode('Development')
# DB Definition
>>> app.set_db(dbfile="app.db")

# Tags Definition
>>> tag_engine = CVTEngine()
>>> tag_engine.set_tag('Counter', 'Adim.', 'int', 'Counter variable', 0, 30)

# Tag Definition on DB
interval = 0.5
app.set_dbtags(['Counter'], interval)
```

## Postgres Database (Production Mode)

Usage

```python
db_user = 'db_user'
db_password = 'db_password'
db_host = '127.0.0.1'
db_port = '5432'
db_name = 'db_name'
db_drop_table = False

DATABASE = {
    'user': db_user,
    'password': db_password,
    'host': db_host,
    'port': db_port,
    'name': db_name
    }

app.set_db(dbtype=POSTGRESQL, drop_table=db_drop_table, **DATABASE)

```

## Binding App with Database

```python
@app.define_machine(name='CounterSimulator', interval=interval, mode="async")
class CounterSimulator(PyHadesStateMachine):

    # states
    start  = State('starting', initial=True)
    run  = State('running')
    reset = State('resetting')

    # transitions
    start_to_run = start.to(run)
    run_to_reset = run.to(reset)
    reset_to_start = reset.to(start)

    # parameters
    max_counter = IntegerType()
    counter = TagBinding('Counter')
    counter_write = TagBinding('Counter', direction='write')

    def __init__(self, name):

        super().__init__(name)

    def while_start(self):
        self.max_counter = tag_engine.get_max_value('Counter')
        self.start_to_run()

    def while_run(self):

        self.counter_write = self.counter + 1
        
        if self.counter >= self.max_counter:

            self.run_to_reset()

        print(f"Counter: {self.counter}")

    def while_reset(self):

        self.counter_write = 0
        self.reset_to_start()

if __name__=='__main__':

    app.run()
```