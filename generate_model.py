#
# generate model script
#

import argparse
import tornado.template as template
import os
from conf.config import templates
from lib.powlib import pluralize

def camel_case(name):
    """
        converts this_is_new to ThisIsNew
        and this in This
    """
    return "".join([x.capitalize() for x in name.split("_")])

def generate_model(model_name=None, model_type=None, appname=None, reflect=False):
    """ generates a small model with the given modelname
        also sets the right db and table settings and further boilerplate configuration.
        Template engine = tornado.templates
    """
    #
    # set some attributes
    #
    print(40*"-")
    print(" generating model: " + model_name)
    print(40*"-")
    try:
        loader = template.Loader(templates["stubs_path"])
        model_class_name = camel_case(model_name)
        print("model_class_name: " + model_class_name)
        model_name_plural = pluralize(model_name)
        print("model_name_plural: " + model_name_plural)
        #
        # create the model
        #
        ofilePath = os.path.join(templates["model_path"], model_type)
        ofile = open(os.path.join(ofilePath, model_name+".py"), "wb")
        
        filename = model_type + "_model_template.py"
        if str.lower(model_type) == "sql" and reflect:
            filename = "sql_model_reflection_template.py"
        
        res = loader.load(filename).generate( 
            model_name=model_name, 
            model_name_plural=model_name_plural, 
            model_class_name=model_class_name,
            appname=appname,
            model_type=model_type
        )
        ofile.write(res)
        ofile.close()
    except:
        return False
    print("... generated: " + model_type + " DB Model")
    print(40*"-")
    print("... in : " + ofile.name)
    print(40*"-")
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', "--name", action="store", 
                        dest="name", help='-n modelname',
                        required=True)
    parser.add_argument('-t', "--type", action="store", 
                        dest="type", help='-d dbtype   -> Example: -d sql  OR -d tinydb ...',
                        default="sql", required=True)
                    
    parser.add_argument('-r', "--reflect", action="store_true", 
                        dest="reflect", help="-r | --reflect to generate a model prepared for SQL DB reflection. ",
                        default=False, required=False)
    #
    # db type
    # 
    # parser.add_argument('-d', "--db", action="store", 
    #                     dest="db", help='-d which_db (mongo || tiny || peewee_sqlite) default = tiny',
    #                     default="tiny", required=True)
    args = parser.parse_args()
    #
    # show some args
    #
    #print("all args: ", args)
    #print(dir(args))
    #print("pluralized model name: ", pluralize(args.name))
    generate_model(model_name = args.name, model_type = args.type, appname="assessment", reflect=args.reflect)

if __name__ == "__main__":
    main()