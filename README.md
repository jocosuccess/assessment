
# The quick and easy generative Webframework for python3. Ready to go!

> Based on the ruby on rails principles. Generators for models/controllers/views/migrations..., convention  over configuration, and PoW gets out of the way if you want it.

# Based on a very Strong foundation:
* python 3.x
* [tornado](http://www.tornadoweb.org/en/stable/) webserver
* Supported SQL Databases
* SQL: [sqlalchemy](https://www.sqlalchemy.org/) ORM (SQLite, MySQL, PostgreSQL, MS-SQL, Oracle, and more ..)
* Database Migrations onboard (based on alembic) generated behind the scenes
* NoSQL: [tinyDB](https://tinydb.readthedocs.io/en/latest/index.html), [MongoDB](https://www.mongodb.com/), [elasticsearch](https://www.elastic.co/products/elasticsearch)
* [cerberus](http://docs.python-cerberus.org/en/stable/) schemas and validation on board
* tornado templates
* css Frameworks: [bootstrap4](https://getbootstrap.com/) and [semanticUI](https://semantic-ui.com/)

# Probably the most simple SQL relations out there! 
Based on sqlalchemy.
With PythonOnWheels you simply add a class decorator like 

~~~~
@relation.has_many("comments")
class Widget(Base):
    # All your Widget model code below here ..
    .....
~~~~

to your SQL Widget-model and every Widget can have comments. It will be automatically mapped to the DB (SQLite, Postgres, MySQL, MariaDb, Oracle, MSSQL ...) and to all related comment Models. DB Migrations are created automatically in the background.

## supported relation types are:

* has_many("comments")(decorated class has many comments.)
* many_to_many("comments")(decorated class has many to many with comments)
* belongs_to("comments")(decorated class belongs to comments.)
* one_to_one("comments")(decorated class has one to one with comments)
* tree() (decorated class has adjacence list (is a tree)

# All pow models (SQL or NoSQL) use a [cerberus](http://docs.python-cerberus.org/en/stable/) schema as definition. 
## This means you have validation on board for every model and you can easily switch from SQL to NoSQL

* the @relation.setup_schema() decorator will map this schema to a vaild sqlalchemy (or specific NoSQL) column definition set.
* SQL only: model will also automatically get all the right Foreign_Keys and python attributes to create a has_many relationship to the comments model. This is all done for you with the @relation.has_many("comments")
@relation.has_many("comments")
@relation.setup_schema()

~~~~
class Widget(Base):
#
# Schema definition with the new (cerberus) schema style
# which offer you immediate validation
#
schema = {
    # string sqltypes can be TEXT or UNICODE or nothing
    'Name' :   { 'type' : 'string', 'maxlength' : 64 },
    "Number of parts" :   { "type" : "integer", "default" : 0 }
}

# init
def __init__(self, **kwargs):
    self.init_on_load(**kwargs)

# your methods down here
~~~~

# Probably the most simple RESTrouting out there! One decorator. Done!
## With PythonOnWheels you simply add a class decorator like 
~~~~
@app.add_rest_routes("basename") 
~~~~
to your handler and you get all the typical REST routes mapped to the according CRUD methods of your handler class.

## By the way: this is what generate_handler generates for you when you use the --rest parameter:
~~~~
@app.add_rest_routes("rest_test")
class RestTest(BaseHandler):
    # 
    # every pow handler automatically gets these RESTful routes
    # when you add the : app.add_rest_routes() decorator.
    #
    # 1  GET    /resttest                           #=> list
    # 2  GET    /resttest/<uuid:identifier>         #=> show
    # 3  GET    /resttest/new                       #=> new
    # 4  GET    /resttest/<uuid:identifier>/edit    #=> edit 
    # 5  GET    /resttest/page/<uuid:identifier>    #=> page
    # 6  GET    /resttest/search                    #=> search
    # 7  PUT    /resttest/<uuid:identifier>         #=> update
    # 8  PUT    /resttest                           #=> update (You have to send the id as json payload)
    # 9  POST   /resttest                           #=> create
    # 10 DELETE /resttest/<uuid:identifier>         #=> destroy
    # ...
~~~~



## Example for Flask like routing:
~~~~
@app.make_method_routes()
class HelloHandler(BaseHandler):
    @route(r'/hello/<int:identifier>', dispatch=["get"])
    def hello(self, identifier=None):
        self.write("Hello world! " + str(identifier))
~~~~
## For Regex routes:
~~~~
@app.add_route("/test/([0-9]+)*", dispatch={"get" : "test"})
~~~~
to add a direct route: matching the regular expression : /test/([0-9+]) and then calling the given method of your handler class. The regex group ([0-9+]) will be handed as the first parameter to test(self, index)

# Model Validation on board with cerberus schemas. 
All Model Schemas are Cerberus schemas automatically.
So thats easy. 
~~~~
    model.validate() => executes cerberus validator
~~~~

And finally: a super easy workflow. 
Quick to start, all the basics on board and easy to expand:
generative approach (but not noisy)

* generate_app script
* generate_models script (You probably want to store some data)
* Optionally generate_migrations script (only needed for SQL DBs)
* generate_handlers (aka controllers to define your logic and API)
* start the server (python server.py) done

# The vision:
>If you want start to develop your web-application and focus on the App, instead of the frameworks, you are in the right place. PythonOnWheels feels right if you do not recognize that you use it.
>

# Enjoy! 
See [getting started](http://www.pythononwheels.org/article/7de74cc6-8af2-45ac-b619-eea61e4da44f) or go to the [documentation](http://www.pythononwheels.org/article/2160fdfd-fc9f-4380-aeb3-bc13d2c201e0)

## For more check: [The PythonOnWheels Homepage](http://www.pythononwheels.org)


    