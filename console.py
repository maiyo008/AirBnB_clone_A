#!/usr/bin/python3
# base_models.py

"""This module defines the HBNBCommand class"""
import cmd
from models.base_model import BaseModel
import models
import sys
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """
    Command interpreter for the HBNB project.
    """

    prompt = "(hbnb) "

    class_dict = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Place": Place
    }
    instances = {}

    def do_quit(self, line):
        """
        Quit command to exit the program.
        """
        sys.stderr.write("Quitting HBNB Console\n")
        return True

    def do_EOF(self, line):
        """
        Exit the console using EOF (Ctrl-D).
        """
        sys.stderr.write("\n")
        return True

    def emptyline(self):
        """
        Do nothing when an empty line is entered.
        """
        pass

    def do_create(self, line):
        """
        Creates a new instance of BaseModel, saves it (to the JSON file)
        and prints the id
        """
        lines = line.split()
        class_name = lines[0]
        if not line:
            print("** class name missing **")
            return
        elif class_name not in HBNBCommand.class_dict:
            print("** class doesn't exist **")
            return
        else:
            new_instance = HBNBCommand.class_dict[class_name]()
            new_instance.save()
            print(new_instance.id)
            try:
                if class_name in HBNBCommand.instances:
                    HBNBCommand.instances[class_name].append(new_instance)
                else:
                    HBNBCommand.instances[class_name] = [new_instance]
            except KeyError:
                print(f"Error: class {class_name} not found")

    def do_show(self, line):
        """
        Prints the string representation of an instance based
        on the class name and id
        """
        lines = line.split()
        if not line:
            print("** class name missing **")
            return
        elif lines[0] not in HBNBCommand.class_dict:
            print("** class doesn't exist **")
            return
        elif len(lines) < 2:
            print("** instance id missing **")
            return
        else:
            keys = lines[0] + "." + lines[1]
            for key, value in models.storage.all().items():
                if key == keys:
                    k = key.split(".")
                    output = "[{}] ({}) {}".format(k[0], k[1], value)
                    print(output)
                    break
            else:
                print("** no instance found **")

    def do_destroy(self, line):
        """
        Deletes an instance based on the class name and id
        """
        lines = line.split()
        if not line:
            print("** class name missing **")
            return
        elif lines[0] not in HBNBCommand.class_dict:
            print("** class doesn't exist **")
            return
        elif len(lines) < 2:
            print("** instance id missing **")
            return
        else:
            key = lines[0] + "." + lines[1]
            if key in models.storage.all():
                del models.storage.all()[key]
                models.storage.save()
            else:
                print("** no instance found **")

    def do_all(self, line):
        """
        Prints all string representation of all instances based
        or not on the class name
        """
        lines = line.split()
        if not line:
            for key, value in models.storage.all().items():
                k = key.split(".")
                output = "[{}] ({}) {}".format(k[0], k[1], value)
                print(output)
        elif lines[0] not in HBNBCommand.class_dict:
            print("** class doesn't exist **")
            return
        else:
            for key, value in models.storage.all().items():
                k = key.split(".")
                output = "[{}] ({}) {}".format(k[0], k[1], value)
                print(output)

    def do_update(self, line):
        """
        Updates an instance based on the class name
        and id by adding or updating attribute
        """
        lines = line.split()
        if not line:
            print("** class name missing **")
            return
        elif lines[0] not in HBNBCommand.class_dict:
            print("** class doesn't exist **")
            return
        elif len(lines) < 2:
            print("** instance id missing **")
            return
        else:
            keys = lines[0] + "." + lines[1]
            if keys not in models.storage.all():
                print("** no instance found **")
                return
            elif len(lines) < 3:
                print("** attribute name missing **")
                return
            elif len(lines) < 4:
                print("** value missing **")
                return
            else:
                keys = ".".join([lines[0], lines[1]])
                value = models.storage.all().get(keys)

                if value is not None:
                    try:
                        value[lines[2]] = int(lines[3])
                    except ValueError:
                        try:
                            value[lines[2]] = float(lines[3])
                        except ValueError:
                            value[lines[2]] = str(lines[3])
                    models.storage.save()

    def default(self, line):
        """
        Prints the number of instances of a specified class
        Usage: <class name>.count()
        """

        try:
            args = line.split('.')
            class_name = args[0]
            count = len(HBNBCommand.instances[class_name])
            print(count)
        except (KeyError, IndexError):
            print(f"Error: class {class_name} not found or invalid syntax")

if __name__ == '__main__':
    HBNBCommand().cmdloop()
