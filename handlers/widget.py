#from assessment.handlers.base import BaseHandler
from handlers.powhandler import PowHandler
from models.sql.widget import Widget as Model
from conf.config import myapp, database
from lib.application import app, route, authenticated_with_role
import simplejson as json
import tornado.web


#@app.make_routes()
@app.add_rest_routes("widget")
class Widget(PowHandler):
    """
    every pow handler automatically gets these RESTful routes
    when you add the : app.add_rest_routes() decorator.
    
    1  GET    /widget                           #=> list
    2  GET    /widget/<uuid:identifier>         #=> show
    3  GET    /widget/new                       #=> new
    4  GET    /widget/<uuid:identifier>/edit    #=> edit 
    5  GET    /widget/page/<uuid:identifier>    #=> page
    6  GET    /widget/search                    #=> search
    7  PUT    /widget/<uuid:identifier>         #=> update
    8  PUT    /widget                           #=> update (You have to send the id as json payload)
    9  POST   /widget                           #=> create
    10 DELETE /widget/<uuid:identifier>         #=> destroy
    
    Standard supported http methods are:
    SUPPORTED_METHODS = ("GET", "HEAD", "POST", "DELETE", "PATCH", "PUT", "OPTIONS")
    you can overwrite any of those directly or leave the @add_rest_routes out to have a basic 
    handler.

    curl tests:
    for windows: (the quotes need to be escape in cmd.exe)
      (You must generate a post model andf handler first... update the db...)
      POST:   curl -H "Content-Type: application/json" -X POST -d "{ \"title\" : \"first widget\" }" http://localhost:8080/widget
      GET:    curl -H "Content-Type: application/json" -X GET http://localhost:8080/widget
      PUT:    curl -H "Content-Type: application/json" -X PUT -d "{ \"id\" : \"1\", \"text\": \"lalala\" }" http://localhost:8080/widget
      DELETE: curl -H "Content-Type: application/json" -X DELETE -d "{ \"id\" : \"1\" }" http://localhost:8080/widget
    """
    model=Model()
    
    # these fields will be hidden by scaffolded views:
    hide_list=["id", "created_at", "last_updated"]

    def show(self, id=None):
        m=Model()
        res=m.find_by_id(id)
        self.success(message="widget show", data=res)
        
    def list(self):
        m=Model()
        res = m.get_all()  
        self.success(message="widget, index", data=res)         
    
    def page(self, page=0):
        m=Model()
        res=m.page(page=int(page), page_size=myapp["page_size"])
        self.success(message="widget page: #" +str(page), data=res )  
        
    @tornado.web.authenticated
    def edit(self, id=None):
        m=Model()
        try:
            print("  .. GET Edit Data (ID): " + id)
            res = m.find_by_id(id)
            self.success(message="widget, edit id: " + str(id), data=res)
        except Exception as e:
            self.error(message="widget, edit id: " + str(id) + "msg: " + str(e) , data=None)

    @tornado.web.authenticated
    def new(self):
        m=Model()
        self.success(message="widget, new",data=m)

    @tornado.web.authenticated
    def create(self):
        try:
            data_json = self.request.body
            m=Model()
            m.init_from_json(data_json, simple_conversion=True)
            m.upsert()
            self.success(message="widget, successfully created " + str(m.id), 
                data=m, format="json")
        except Exception as e:
            self.error(message="widget, error updating " + str(m.id) + "msg: " + str(e), 
                data=m, format="json")
    
    @tornado.web.authenticated
    def update(self, id=None):
        data_json = self.request.body
        m=Model()
        res = m.find_by_id(id)
        res.init_from_json(data_json, simple_conversion=True)
        try:
            #res.tags= res.tags.split(",")
            res.upsert()
            self.success(message="widget, successfully updated " + str(res.id), 
                data=res, format="json")
        except Exception as e:
            self.error(message="widget, error updating: " + str(m.id) + "msg: " + str(e), data=data_json, format="json")


    #@authenticated_with_role("admin") => example: only admins can delete items. Make sure user-model has attribute "role"
    @tornado.web.authenticated
    def destroy(self, id=None):
        try:
            data_json = self.request.body
            print("  .. DELETE Data: ID:" + str(data_json))
            m=Model()
            m.init_from_json(data_json)
            res = m.find_by_id(m.id)
            res.delete()
            self.success(message="widget, destroy id: " + str(m.id))
        except Exception as e:
            self.error(message="widget, destroy id: " + str(e))
    
    def search(self):
        m=Model()
        return self.error(message="widget search: not implemented yet ")