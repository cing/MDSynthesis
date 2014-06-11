"""
Classes for datafile syncronization. 

"""

import Aggregators
import Workers
import yaml
import pickle
from uuid import uuid4

class File(object):
    """File object base class. Implements file locking and syncronization.
    
    """
    def __init__(self, filename, reader, writer, datastruct=None, logger=None):
        """Create File instance for interacting with file on disk.

        The File object keeps its own cached version of a data structure
        written to file in sync with the file itself. It does this by
        consistently applying locks to files before reading and writing. 
        
        At all times, reading and modifying the data structure is the same as
        reading and writing to the file. Accessing an element of the data
        structure results in locking, reading, and unlocking the file each
        time. Modifying an element results in locking, reading, writing, and
        unlocking. All operations are performed atomically to ensure unintended
        overwrites are avoided.

        :Arguments:
           *filename*
              name of file on disk object synchronizes with
           *reader*
              function used to translate file into data structure;
              must take one argument: file stream to read from
           *writer*
              function used to translate data structure into file;
              must take two arguments: the data structure to write and the 
              file stream to write to
           *datastruct*
              data structure to store; overrides definition in :meth:`create`
              this allows for custom data structures without a pre-defined
              definition 
           *logger*
              logger to send warnings and errors to

        """
        self.filename = filename
        self.lockname = "{}.lock".format(self.file.name) 

        self.reader = reader
        self.writer = writer

        # if given, use data structure and write to file
        # if none given, check existence of file and read it in if present
        # else create a new data structure and file from definition
        if datastruct:
            self.data = datastruct
            self.write()
        elif self.check_existence():
            self.read()
        else:
            self.create()
            self.write()

    def create(self):
        """Build data structure.

        This is a placeholder function, since each specific File use-case
        will have a different data structure definition.

        """
        self.data = None

    def read(self):
        """Read contents of file into data structure.

        :Returns:
           *success*
              True if write successful
        """
        # keep attempting lock until successful (failsafe)
        while not self.lock():
            continue

        # keep reading until unlock gives success (only if synchronized)
        while not self.unlock()
            with open(self.filename, 'r') as f:
                self.data = self.reader(f)
        
        return True

    def write(self):
        """Write data structure to file.
    
        :Returns:
           *success*
              True if write successful
        """
        # keep attempting lock until successful (failsafe)
        while not self.lock():
            continue

        # keep writing until unlock gives success (only if synchronized)
        while not self.unlock()
            with open(self.filename, 'w') as f:
                self.writer(self.data, f)

        return True

    def lock(self):
        """Get exclusive lock on file.

        The lock is just a symlink of the target file, since making a symlink
        appears to be an atomic operation on most platforms. This is important,
        since creating a symlink also serves to check if one is already present
        all in one operation.

        :Returns:
           *success*
              True if lockfile successfully created
        """
        # if lockfile already present, wait until it disappears; make lock
        while True:
            try:
                os.symlink(self.filename, self.lockname):
                break
            except OSError:
                time.sleep(1)

        # return lockfile existence
        return os.path.exists(self.lockname)

    def unlock(self):
        """Remove exclusive lock on file.

        Before removing the lock, checks that the data structure is
        the same as what is on file.

        :Returns:
           *success*
              True if comparison successful 
        """
        # check that python representation matches file
        success = self.compare()

        if success:
            os.remove(self.lockname)

        return success

    def compare(self):
        """Compare data structure with file contents.

        :Returns:
           *same*
              True if file synchronized with data structure
        """
        with open(self.filename, 'r') as f:
            datatemp = self.reader(f)
        
        return self.data == datatemp
    
    def check_existence(self):
        """Check for existence of file.
    
        """
        return os.path.exists(self.filename)

class ContainerFile(File):
    """Container file object; syncronized access to Container data.

    """
    def __init__(self, location, logger, classname, name=None, categories=None, tags=None,
            details=None): 
        """Initialize Container state file.

        This is the base class for all Container state files. It generates 
        data structure elements common to all Containers.

        :Arguments:
           *location*
              directory that represents the Container
           *logger*
              Container's logger instance
           *classname*
              Container's class name
           *name*
              user-given name of Container object
           *categories*
              user-given dictionary

        """
        super(ContainerFile, self).__init__(filename, reader=yaml.load, writer=yaml.dump, logger=logger)

    def create(self):
        """Build common data structure elements.

        """
        self.data = {}

        self.data['location'] = 
        self.data['uuid'] = str(uuid4())

        if name:
            self.data['name'] = name
        else:
            self.data['name'] = classname

        self.data['data'] = list()
        self.data['class'] = classname

        if isinstance(categories, dict):
            self.data['categories'] = categories
        else:
            self.data['categories'] = dict()
            
        if isinstance(tags, list):
            self.data['tags'] = tags
        else:
            self.data['tags'] = list()

        if isinstance(details, basestring):
            self.data['details'] = details
        else:
            self.data['details'] = str()


    def _generate_uuid(self):
        """Generate a 'unique' identifier.

        """
        return str(uuid4())

class SimFile(ContainerFile):
    """Main Sim state file.

    This file contains all the information needed to store the state of a
    Sim object. It includes accessors, setters, and modifiers for all
    elements of the data structure, as well the data structure definition.
    It also defines the format of the file, i.e. the writer and reader
    used to manage it.
    
    """
    def __init__(self, filename, logger):
        """Initialize Sim state file.

        :Arguments:
           *filename*
              name of file on disk object synchronizes with
           *logger*
              logger to send warnings and errors to

        """
        super(SimFile, self).__init__(filename, reader=yaml.load, writer=yaml.dump, logger=logger)
    
    def create(self):
        """Build Sim data structure.

        """
        super(SimFile, self).create()

        attributes = {'uuid': uuid,
                      'name': kwargs.pop('name', self.__class__.__name__),
                      'data': list(),
                      'class': self.__class__.__name__,
                      'categories': kwargs.pop('categories', dict()),
                      'tags': kwargs.pop('tags', list()),
                      'details': kwargs.pop('details', str())
                      }





        self.data


class DatabaseFile(File):
    """Database file object; syncronized access to Database data.

    """

class DataFile(object):
    """Universal datafile interface.

    Allows for safe reading and writing of datafiles, which can be of a wide
    array of formats. Handles the details of conversion from pythonic data
    structure to persistent file form.

    """
