
# lib.Metadata


## Metadata
```python
Metadata(self, testing: str = None)
```


### getResearchId
```python
Metadata.getResearchId(userId, researchIndex)
```

This method returns the corresponding researchId to the given userId and researchIndex.


### getMetadataForResearch
```python
Metadata.getMetadataForResearch(userId: str = None,
                                researchIndex: int = None,
                                researchId: int = None,
                                metadataFields=None)
```

This method returns the metadata from all available ports for specified researchId.


### getMetadataForProjectFromPort
```python
Metadata.getMetadataForProjectFromPort(port: str,
                                       projectId: int,
                                       apiKeyMetadata=None)
```

This method returns the metadata from given port for specified projectId.
Beware that the projectId comes from the service, which is connected throug the port.
Returns a dict, which was described in the metadata api endpoint "/metadata/research/{research-id}" or an empty one.

Be careful to use apiKeyMetadata only with the struct: {apiKey: userAPIKey, metadata: metadata}


### updateMetadataForResearch
```python
Metadata.updateMetadataForResearch(researchId: int,
                                   updateMetadata: dict)
```

This method changes the metadata in all available ports to the given metadata values in given dict for specified researchId.


### updateMetadataForResearchFromPort
```python
Metadata.updateMetadataForResearchFromPort(port: str, projectId: int,
                                           updateMetadata: dict)
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

The struct of a metadata model have to be the same as described in the metadata api with the following addition.

Be careful to use updateMetadata only with the struct: {apiKey: userAPIKey, metadata: metadata}


# lib.Research


## Research
```python
Research(self,
         userId: str = None,
         researchIndex: int = None,
         researchId: int = None,
         testing: str = None)
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
Research.getPorts(metadata=True)
```

This method returns only the ports with metadata as type. No duplicates.
Set parameter `metadata` to False to get all ports. Duplicates ports, which are set as input and output.


### getPortsWithProjectId
```python
Research.getPortsWithProjectId(metadata=True)
```

This method returns a list of tuple with (port, projectId) with metadata as type. No duplicates.
Set parameter `metadata` to False to get all ports. Duplicates ports, which are set as input and output.
If no projectId was found, it is None.

This method is useful, if you want to redirect a call to all ports which are configured for a research project in RDS.


### reload
```python
Research.reload(userId: str = None,
                researchIndex: int = None,
                researchId: int = None)
```

This method catches the research information from the central service research manager.
userId and researchIndex are only used together. You can provide researchId,
so you do not need to enter userId and researchIndex for convenience.

