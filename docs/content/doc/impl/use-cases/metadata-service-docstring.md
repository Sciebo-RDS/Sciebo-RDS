# lib.Metadata

## Metadata
```python
Metadata(self, testing:str=None)
```

### getProjectId
```python
Metadata.getProjectId(self, userId, projectIndex)
```

This method returns the corresponding projectId to the given userId and projectIndex.

### getMetadataForProject
```python
Metadata.getMetadataForProject(self, userId:str=None, projectIndex:int=None, projectId:int=None)
```

This method returns the metadata from all available ports for specified projectId.

### getMetadataForProjectFromPort
```python
Metadata.getMetadataForProjectFromPort(self, port:str, projectId:int)
```

This method returns the metadata from given port for specified projectId.
Returns a dict, which was described in the metadata api endpoint "/metadata/project/{project-id}" or an empty one.

### updateMetadataForProject
```python
Metadata.updateMetadataForProject(self, projectId:int, updateMetadata:dict)
```

This method changes the metadata in all available ports to the given metadata values in given dict for specified projectId.

### updateMetadataForProjectFromPort
```python
Metadata.updateMetadataForProjectFromPort(self, port:str, projectId:int, updateMetadata:dict)
```

This method changes the metadata in given port to the given metadata values in given dict for specified projectId.
Returns the current metadata data, so you can check, if the update was successful or not.

The given updateMetadata has to be a dict with the following struct:
{
    "Creator": [{
        "creatorName": "Max Mustermann",
        ...
    }],
    "Publisher": {
            "publisher": "Lorem Ipsum"
    },
    ...
}

The struct of a metadata model have to be the same as described in the metadata api.

# lib.Project

## Project
```python
Project(self, userId:str=None, projectIndex:int=None, projectId:int=None, testing:str=None)
```

This class enables metadataservice to reuse requests and let it easier to use.
*Currently* only for get requests.

### portIn

This property returns all ports, which functions as input in RDS.

### portOut

This property returns all ports, which functions as output in RDS.

### ports

This property returns only the ports with metadata as type. No duplicates.

### getPorts
```python
Project.getPorts(self, metadata=True)
```

This method returns only the ports with metadata as type. No duplicates.
You can set the parameter `metadata` to False to get all ports. Duplicates ports, which are set as input and output.

### reload
```python
Project.reload(self, userId:str=None, projectIndex:int=None, projectId:int=None)
```

This method catches the project information from the central service project manager.
userId and projectIndex are only used together. You can provide projectId,
so you do not need to enter userId and projectIndex for convenience.

