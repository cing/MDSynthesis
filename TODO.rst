=============
TODO List
=============

2014.12.18
----------
Need selections to update instead of having to manually delete them.

2014.12.9
---------
We will need to do some kind of caching for Group members. Reloading them on
demand is fast on an SSD, but slow on a disk, and even slower on a network
drive. This should work fine; I don't foresee any problems, since members
always show their current state by reading from disk anyway...which begs the
question as to whether or not this will be significantly faster...

Nested datasets should be allowed. In other words, giving a handle such as
'geometry/zpos' for storing a dataset should store it in
'geometry/zpos/Data.h5'. This should cause any problems, though data discovery
will have to be reworked to use os.walk recursively.

We want to be able to store non-string tags and categories. We can achieve this
by including a dtype identifier for each category and tag added, which will
allow back-conversion from the string representation stored on disk back to the
numerical data type.

2014.11.25
----------
Although pandas is great, I think it would be very good if datasets can be
numpy arrays as well as pandas objects. Currently this is not implemented, but
one way of doing it might be to use the netcdf4-python module and build a
DataFile object specific to that format. If we make this DataFile object have
the same API as the existing one, then the only modification we'd need to the
Data aggregator is choosing which to use for a given dataset. Could be done by
extension of the datafile.

2014.11.25
----------
Been thinking about use of logging vs. exceptions to indicate something is
amiss with user input. My current thought is that exceptions should occur in
low-level objects (such as files), and logging should only happen in high-level
objects. This also removes the possibility of having duplicate log outputs from
low-level methods and higher-level wrappers.

2014.11.21
----------
Since logging does not really make sense to start up until AFTER a state file
has been attached, perhaps we should make a method of File to replace its
logger with another? This would avoid the current headache.

2014.11.18
----------
What if a Sim or Group's own information is moved during the course of its use?
Is there a way we can make Finder go looking? Perhaps as a wrapper to accessors?
Or would this be too much padding?

2014.11.18
----------
Should atom selections be regenerated every time they are called? Advantages?
Disadvantages? What would be the clearest and most useful implementation?

2014.11.09
----------
Revisiting the idea that Groups have a concept of order with respect to their
members. The way member information is stored inherently has order (they are
rows in a table), but should ordering and re-ordering be handled at the file
level or by higher level functionality? I'm leaning more toward it being
handled by higher level methods, if at all.

2014.10.29
----------
Perhaps add a decorator to File (or modify the write decorator) that stores
the method call before execution. This might allow recovery in the instance
that a write operation is disrupted.

2014.10.21
----------
Possibility for compressed Containers? They would need some kind of naming
rule in order to be discoverable by Finder. Could be useful if space is an
issue but performance is not.

2014.09.30
----------
Need to make it easy to add more data later for a trajectory that later becomes
extended.

Statement
---------
MDS integrates only as much as it needs for its core functionality (easy logistics). It
leaves other functionality to external modules. It will include conveniences
for the modules it requires as dependencies (e.g. pytables, pandas)

2014.08.31
----------
Lazy loading of Group members and DataSet instances will allow us to avoid
requiring explicit load machinery, and avoid slow speeds of full
initialization. The same can be done for universes in Sims.

2014.08.20
----------
Cons to merging data into state files:
    - when writing large data to file, this makes it impossible to get read
      lock on state information. This will slow down all processes making
      use of that Container, including Coordinator and Group actions.

Keeping files separate
    - can still keep information on data present in Sims and Groups in
      database, since this is updated by the Sims and Groups themselves when
      run
    - what if data deleted by user, then queries database for Sims that have
      data? Database will have stale entries; will need to add checker to
      ensure query results actually have data requested, and remove those that
      don't. Will have to optimize later.

In general I prefer keeping data files separate, as it retains the advantage
that MDS mimics much of what we already do manually. This is familiar, and
allows for work in the filesystem instead of in some obfuscating file format.

2014.08.19
----------
Mental vomit:
    - store MDS version in state files; this allows us to write conversion code
      to ensure state files are updated for new releases.
    - instead of storing data files separately, why not store all Container
      data in state file? This would allow us to avoid problems with file
      renaming and eschew the directory structure of Containers. Sims, Groups,
      and Coordinators will now be single files.
        - does not remove any flexibility on the part of the user.
        - ensures loaded Containers do not have stale data handles when data is
          deleted; avoids requiring machinery for detection of this.
        - Reduces number of files to deal with; perhaps therefore introduces
          file locking congestion in high throughput situations.

2014.08.13
----------
Because the ideas come faster than the implementation, I've come to jotting
down my ideas about various aspects of this project here. Better than nowhere.

Group object
    - can include a mechanism for forking a process for each member in ipython,
      allowing one to operate on multiple Sim objects simultaneously as if
      working on only one. Ipython may have built in mechanisms for
      communication between processes: http://ipython.org/ipython-doc/dev/parallel/

2014.08.12
----------
We will avoid multithreading at all costs. Instead, use separate processes.
Threads share the advisory lock of their process, which means that if an object
is using threads and these need to update the state file, the locks will mean
nothing.

Perhaps build an undo option into objects?
    - basically, revert to previous version of state file, since operations
      atomic
    - will need extra machinery in the case of changes to filesystem outside of
      state file

Thoughts for Groups:

Group takes any combination of Groups and Sims.

Items in a group have an order, and can be accessed via index like a list. Can
be rearranged by user.

Groups can be queried for members.
    - allows for generation of new groups or generation of data on members or
      within members. User is advised to structure their Groups, because this
      feature can encourage confusing practices.

Group has method to Group members. This will:
    - create the sub-Group's persistent form inside the Group. Won't be scraped
    by Data aggregator since no data file will be found immediately inside this
    directory.
    - add the Group to the list of members.
    - remove the given members from the list of members.
This will work fine so long as Finder knows that objects can live inside object
directory structures. The benefit is that manual labor is not needed to
structure a Group after it has been defined.

Groups can be flattened. Order number given to determine how much to flatten. 0
for Sim, 1 for Group, 2 for Group^2, etc. Flatten value is highest order object
present in group after flattenning.

Objects should be able to transfer data somehow (hopefully unnecessary, but
when needed, good to have). Add method could handle DataFile objects as well as
Data aggregators appropriately. It would then copy data through filesystem.

Store dataset data instances in single table in state file. Reprobe for these
on each load. This will allow queries based on existing data in Coordinator
and Groups.

2014.07.31
----------
Perhaps use PyTables directly for defining state files, and Pandas for handling
data. Example Sim state file:

HDF5 STRUCTURE
/
meta
coordinator
tags
categories
universes/
    main/
        topology
        trajectories
        selections

/
-------
meta : uuid, name, class, location
tags: tags
categories: category, value

universes/
----------
    main/ 
    -----
    topology: abspath, relhome, relSim
    trajectories: abspath, relhome, relSim
    selections: selection
    
We do not wish to store any information on user-generated data here, since this
will be stored in its own directory/HDF5 file. This allows one to delete these
directories without introducing inconsistencies.

Data aggregator will interface to individu

Be sure to use pytables flush method to ensure writes have finished before
removing exclusive lock.

For data access, will either need to wrap all access methods (including
indexing) with lock decorator, or require Sim.data.DATAINSTANCE.load prior to
use. Sim.data.DATAINSTANCE.unload will remove shared lock.
    + problem: will need separate mechanism for obtaining exclusive lock.
    + probably better to develop mechanism that applies shared lock before
      access, then removes it afterward. Likewise for modifiers. Can ponder
      this later; not necessary for usefulness when concurrent access not
      needed.
Need to play directly with pandas HDFStore interface. This will inform how we
go about applying the lock mechanisms. Possibly consider inheriting from
HDFStore and explicitly wrapping all functions appropriately.

For state files, can easily apply shared and exclusive locks using a decorator
on getters and setters, respectively. Access to these stored data will be
integrated into the Sim class. We have no need for pyTables query
functionality in this case (with perhaps exception of tags and categories).
    
Sim::
    add::
        universe()
        selection()
        data()
        tag()
        category()
        
    remove::
        universe()
        selection()
        data()
        tag()
        category()

    info?::

    attach::
        universe1

    universe -> Universe

    selections::
        selection1 -> atomgroup

    data::
        instance -> pandas HDFStore
        insance2
    
Overall scheme
==============
Sean Seyler and and I are collaborating to make this package work well as the
lower-level infrastructure for two different purposes. It will rock.

To make it easier to build, I propose we split the workload for now as follows:

    + Containers: I will focus on Container functionality. This is the most 
        well-developed at the moment, and there is a lot of existing code to
        wade through to improve them.

    + Operators: Sean is exceptional at optimization and algorithm design, and
        the Operators need plenty of design TLC. They are mostly just skeletons at
        present.  I suggest this be his area of expertise. Operators take in
        Containers as input, efficiently perform work on them, then give the
        Container the resulting data (in whatever form; python structures, plots,
        etc.) to store away.

    + Coordinator: This is basically the highest level Container of the whole scheme.
        It allows Containers to find each other when moved, and will allow the user
        to summon whole sets of Containers using selection queries (not implemented
        yet). I will focus on this, since it does not need to know anything about
        Operators but works intimately with Containers.

    + Core.Files: We will both need to brainstorm on building these file interfaces.
        The idea is that any change to a file class is immediately reflected in the
        file on disk, and vice-versa. The file class state should always
        reflect the file on disk's state, even if the file on disk is being
        altered by other instances of the file class at the same time. This
        will require some special magick.

    + Core.Aggregators: These classes serve as interfaces to file data, possibly
        from multiple files at once. I will focus my efforts on the Container-specific
        aggregators (Info and its derivatives), while Sean will need to consider how
        the Data operator behaves given the form of Operator-generated data files.
        This is a bit of a gray area, because in principle the Containers will "have
        a" Data aggregator that serves as the interface to loaded data, and Operators
        will interact with this in dumping their own results to the Container.

    + Core.Workers: These are the grab-bag classes. The ObjectCore is a mixin for
        all user-level objects (Containers and Operators). Finder will be a class
        that specializes in finding missing Databases and Containers in the filesystem.
        It will be called by these classes when a persistent object can't be found.
        Utilities contains functions used frequently by higher-level class methods;
        they should not ever be needed by a user; each object has one. Each
        Container will also "have a" Attributes object, which is a safe space
        for users to define their own attributes of a Container that guarantees
        functionality won't be broken.

Core
====

+ class `File` needs a rewrite.
    + turn it into an interface for an instance of an MDS file (metadata, database, datafile)
    + will allow atomic (modification of individaul elements with no stale overwrites) editing
    + synced with actual file every time object is accessed.

+ add class `Metadata` that serves as an interface to metadata files
    + we'd like to move away from manual edits of the metadata in-object
    + basically, atomize changes made to the metadata to ensure that it can be
      user-edited while still avoiding stale writes
    + along with this idea is full persistence: before an object ever writes out
      metadata, it refreshes its copy first

+ add class `DBFile` for database.
    + every time database calls for attribute, gets re-read.

+ add class `Datafile` for individual datafiles.

+ class `Data` to handle multiple datafile instances for Operators
    + we will abandon the 1-file-per-operator mindset, placing no restriction
      on the number of files one can store data in.
    + will serve as interface to all data instances
    + this new paradigm will mesh with another: that Operator base classes are
      built with few prescriptive methods but instead contain decorators that
      can be mixed and matched to get powerful functionality with little work.
