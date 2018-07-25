# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pymongo


import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web


#from tornado.options import define, options

#define("port", default=8888, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r"/",AdminHandler),(r"/login",AdminHandler),("/home4.html",AdminHandler),("/insertindex.html",InsertHandler),
                    (r"/insertdetails",InsertHandler),("/updateindex.html",UpdateHandler),(r"/updateoneid",UpdateHandler),
            ("/deleteindex2.html",DeleteHandler),(r"/deleteid",DeleteHandler)
        ]
        #handlers = [(r"/",IndexHandler),("/insertindex.html",InsertHandler),(r"/insertdetails",InsertHandler),
         #           ("/updateindex.html",UpdateHandler),(r"/updateoneid",UpdateHandler),
         #   ("/deleteindex2.html",DeleteHandler),(r"/deleteid",DeleteHandler)
        #]

        settings = dict(
            autoescape=None,
        )
        tornado.web.Application.__init__(self, handlers, **settings)

        client = pymongo.MongoClient("localhost", 27017)
        self.database = client["myfirstdb"]

class AdminHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('adminindex.html')
    def post(self):
        data_exist=False
        db=self.application.database
        username = self.get_argument('username')
        password = self.get_argument('password')
        data=db.admin.find({"password":password})
        for each in data:
            if(each["password"]==password and each["username"]==username):
                data_exist=True
                break
        if data_exist==True:
            #self.render('adminindex.html')
            self.write("Hello, Azar. Data Authenticated")
            self.render("home4.html")
        else:
            self.write("Incorrect Username and Password")
            self.render('adminindex.html')
      
#class IndexHandler(tornado.web.RequestHandler):
   # def get (self):
       # self.render('home4.html')
        
class InsertHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("insertindex.html")
    
    def post(self):
        data_exist=False
        db=self.application.database
        name = self.get_argument('name')
        empid = self.get_argument('empid')
        new_comment = {
            "name" : name,
            "empid" : empid,
            }
        data=db.tata.find({"empid":empid})
        for each in data:
            if(each["empid"]==empid):
                data_exist=True
                break
        if data_exist==False:
            db.tata.insert(new_comment)
            self.write("Hello, Azar. Data Inserted in the database")
            self.render("insertsuccess.html",name=name,empid=empid)
        else:
            self.write("Data Already Exists")
            #self.render("/dataexists.html",empid=empid)
            
           


'''
class DetailsHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("getdetails.html")
    def get2(self):
        db=self.application.database
        get_details=db.tata.find().sort({"empid":-1})
        
        for each in get_details:
            self.write("<br/>")
            self.write(each["name"])
            self.write(str(each["empid"]))
          
        #comments = db["tata"].find()

        #self.render('etable.html',name=empname,idd=empid,mail=email)
        # self.render('emptable456.html',name=name,empid=empid)
        

'''



class DeleteHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("deleteindex2.html")
    def post(self):
        data_delete=False
        db=self.application.database
        #name = self.get_argument('name')
        empid = self.get_argument('empid')
        data=db.tata.find({"empid":empid})
        
        for each in data:
            if(str(each["empid"]==empid)):
                data_delete=True
                break
        if data_delete==True:
            deleteid={"empid":empid}
            db.tata.remove(deleteid)
            self.render('deletesuccess1.html',empid=empid)    
        else: 
             self.write("Employee ID not found")
            
        

class UpdateHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("updateindex.html")
    def post(self):
        db=self.application.database
        name = self.get_argument('name')
        empid = self.get_argument('empid')
        db.tata.update({"empid":empid},{"$set":{"name":name}})
        self.render('updatesuccess.html',empid=empid,name=name)
        self.write("Data updated Successfully")


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(6845)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()


 

