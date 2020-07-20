
# lib.ExporterService


# lib.Research


## Research
```python
Research(self,
         userId=None,
         researchIndex=None,
         researchId=None,
         testing=False)
```


### getServices
```python
Research.getServices()
```

Returns all services, which are currently configured in the research project.


### getServicesImport
```python
Research.getServicesImport()
```

Returns all services, which are currently configured as import in the research project.


### getServicesExport
```python
Research.getServicesExport()
```

Returns all services, which are currently configured as export in the research project.


### synchronization
```python
Research.synchronization()
```

Synchronize all files between import services and export services.


### addFile
```python
Research.addFile(*args, **kwargs)
```

Wrapper function to call addFile in all export services objects with parameters.

folderInFolder (bool): Only if folderInFolder is True, then it will be checked, if service needs a zip for folders in folder upload.

Returns:
    list: Returns list of booleans, if it succeeds or not. The order follows the self.exportServices order.


### removeAllFiles
```python
Research.removeAllFiles()
```

Remove all files in export services.

Returns a boolean.


### removeFile
```python
Research.removeFile(filepath)
```

Remove file with given filepath in all export services.


### removeFileFromService
```python
Research.removeFileFromService(file_id, service)
```

Remove file with id in export service.


# lib.Service


## Service
```python
Service(self,
        servicename,
        userId,
        researchIndex,
        fileStorage=False,
        metadata=False,
        customProperties: list = None,
        testing=False)
```


### getZipStatusForFolders
```python
Service.getZipStatusForFolders()
```
Returns True, if you have to send zip files, when there are folder in folders. Otherwise False.

Returns:
    bool: True, if you have to send zip for folder in folders.


### getFiles
```python
Service.getFiles(getContent=False)
```

Returns a generator to iterate over.

Returns the filepath string and the content of the file in the current used service.


### addFile
```python
Service.addFile(filename, fileContent)
```
Adds given file with filename to this service.

Args:
    filename (str): Set the filename of this file.
    fileContent (io.BytesIO): Set the content of this file.

Returns:
    bool: Return True, if the file was uploaded successfully, otherwise False.

