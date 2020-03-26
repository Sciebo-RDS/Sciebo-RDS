# lib.Port

## Port
```python
Port(self, portName, fileStorage=False, metadata=False)
```

### setProperty
```python
Port.setProperty(self, portType, value)
```

Returns True, if portType was found and set to value. Otherwise false.

portType has to be a string, value has to be boolean.

# lib.Project

## Project
```python
Project(self, user, portIn=None, portOut=None)
```

### addPort
```python
Project.addPort(port, portList)
```

Adds port (type `Port`) to given portList.

### removePort
```python
Project.removePort(port, portList)
```

Remove port from portList.
Port can be `int` as index or an object with type `Port`.

### nextStatus
```python
Project.nextStatus(self)
```

Set the next status and returns the new value.
It returns the same value, if you already at the last state.

# lib.ProjectService

## ProjectService
```python
ProjectService(self)
```

### addProject
```python
ProjectService.addProject(self, userOrProject, portIn=None, portOut=None)
```

If parameter `userOrProject is an project object, this method adds the given project to the storage.

If parameter `userOrProject` is a string, it first creates an project object for you.
As a convenient parameter, you can set portIn and portOut also, which are used as parameters in project initialization.

### getProject
```python
ProjectService.getProject(self, user='', projectIndex:int=None, projectId:int=None)
```

This method returns all projects, if no parameters were set.
If the parameter `user` is set, it returns all projects, which belongs to the user.
If the `projectIndex` is set, it returns the corresponding project.
**Beware:** *You start counting at Zero!*

If you set the parameter `user` and `projectIndex`, it returns the project relative to all user specific projects.

Raises ValueError if parameter `user` or `projectIndex` are wrong types and IndexError, when you try to access lists and index is to big.

### removeProject
```python
ProjectService.removeProject(self, user:str=None, projectIndex:int=None, projectId:int=None)
```

This method removes the projects for given user.

If projectIndex was given, only the corresponding projectIndex will be removed (no user required, but it is faster).
Returns True if it is successful or raise an exception if user or projectIndex not found. Else returns false.

### getDict
```python
ProjectService.getDict(self)
```

Returns a dict of all projects with a new attribute "id", which symbolize the project projectIndex in the system.

# Status
```python
Status(self, /, *args, **kwargs)
```

The order represents the workflow through the states. So the successor of each status is the next in line.

## CREATED

The order represents the workflow through the states. So the successor of each status is the next in line.

## DELETED

The order represents the workflow through the states. So the successor of each status is the next in line.

## DONE

The order represents the workflow through the states. So the successor of each status is the next in line.

## WORK

The order represents the workflow through the states. So the successor of each status is the next in line.

# NotFoundIDError
```python
NotFoundIDError(self, user, id, msg=None)
```

# NotFoundUserError
```python
NotFoundUserError(self, user, id, msg=None)
```

