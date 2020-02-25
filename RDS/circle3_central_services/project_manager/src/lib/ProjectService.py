from src.lib.Project import Project


class ProjectService():
    def __init__(self):
        # format: {user: []}
        self.projects = {}

    def addProject(self, userOrProject, portIn=None, portOut=None):
        """
        If parameter `userOrProject is an project object, this method adds the given project to the storage.

        If parameter `userOrProject` is a string, it first creates an project object for you. 
        As a convenient parameter, you can set portIn and portOut also, which are used as parameters in project initialization.
        """
        if portIn is None:
            portIn = []

        if portOut is None:
            portOut = []

        if not isinstance(userOrProject, (Project, str)):
            raise ValueError(
                "The parameter `userOrProject` is not of type `str` or `Project`.")

        if isinstance(userOrProject, str):
            userOrProject = Project(
                userOrProject, portIn=portIn, portOut=portOut)

        projectId = len(self.getAllProjects())

        userOrProject.projectId = projectId
        userOrProject.getDict = monkeypatch_getDict(
            userOrProject.getDict, userOrProject)

        if userOrProject.user not in self.projects:
            self.projects[userOrProject.user] = []

        self.projects.get(userOrProject.user).append(userOrProject)

        return userOrProject

    def getProject(self, user="", id=None):
        """
        This method returns all projects, if no parameters were set.
        If the parameter `user` is set, it returns all projects, which belongs to the user.
        If the `id` is set, it returns the corresponding project.
        **Beware:** *You start counting at Zero!*

        If you set the parameter `user` and `id`, it returns the project relative to all user specific projects.

        Raises ValueError if parameter `user` or `id` are wrong types and IndexError, when you try to access lists and index is to big.
        """

        if not isinstance(user, str):
            raise ValueError("Parameter `user` is not of type string.")

        if not isinstance(id, (int, type(None))):
            raise ValueError("Parameter `id` is not of type int.")

        if not user:
            if id is None:
                return self.getAllProjects()
            elif id >= 0:
                for proj in self.getAllProjects():
                    if proj.projectId is id:
                        return proj

        if user:
            listOfProjects = self.projects.get(user)
            if listOfProjects is None:
                from src.lib.Exceptions.ProjectServiceExceptions import NotFoundUserError
                raise NotFoundUserError(user, id)

            if id is None:
                return listOfProjects

            for proj in listOfProjects:
                if proj.projectId is id:
                    return listOfProjects[id]

            if id < len(listOfProjects):
                return listOfProjects[id]

        from src.lib.Exceptions.ProjectServiceExceptions import NotFoundIDError
        raise NotFoundIDError(user, id)

    def removeProject(self, user: str = None, id: int = None):
        """
        This method removes the projects for given user. If id was given, only the corresponding id will be removed (no user required, but it is faster).
        Returns True if it is successful or raise an exception if user or id not found. Else returns false.
        """
        if user is not None:
            if id is not None:
                rmv_id = None
                for index, proj in enumerate(self.getProject(user)):
                    if proj.projectId is id:
                        rmv_id = index
                try:
                    del self.projects.get(user)[rmv_id]
                except:
                    try:
                        del self.projects.get(user)[id]
                    except:
                        from src.lib.Exceptions.ProjectServiceExceptions import NotFoundIDError
                        raise NotFoundIDError(user, id)
            else:
                try:
                    del self.projects[user]
                except:
                    from src.lib.Exceptions.ProjectServiceExceptions import NotFoundUserError
                    raise NotFoundUserError(user, id)
            return True

        if id is not None:
            for user, listOfProjects in self.projects.items():
                rmv_id = None
                for index, proj in enumerate(listOfProjects):
                    if proj.projectId is id:
                        rmv_id = index

                try:
                    del self.projects[user][rmv_id]
                except:
                    from src.lib.Exceptions.ProjectServiceExceptions import NotFoundIDError
                    raise NotFoundIDError(user, id)
                return True

        return False

    def getJSON(self):
        import json
        return json.dumps(self.getDict())

    def getAllProjects(self):
        listOfProjects = []
        for proj in self.projects.values():
            listOfProjects += proj
        return listOfProjects

    def getDict(self):
        """
        Returns a dict of all projects with a new attribute "id", which symbolize the project id in the system.
        """
        return [proj.getDict() for proj in self.projects]

    def __eq__(self, obj):
        if not isinstance(obj, Project):
            return False

        return (self.getDict() == obj.getDict())


def monkeypatch_getDict(getDictFunc, obj):
    """
    Returns a dict of all projects with a new attribute "id", which symbolize the project id in the system.
    """

    def getDict():
        d = getDictFunc()
        d["projectId"] = obj.projectId
        return d

    return getDict
