from src.lib.Project import Project


class MetadataService():
    def __init__(self):
        self.projects = []

    def addProject(self, userOrProject, portIn=[], portOut=[]):
        """
        If parameter `userOrProject is an project object, this method adds the given project to the storage.

        If parameter `userOrProject` is a string, it first creates an project object for you. 
        As a convenient parameter, you can set portIn and portOut also, which are used as parameters in project initialization.
        """

        if not isinstance(userOrProject, (Project, str)):
            raise ValueError(
                "The parameter `userOrProject` is not of type `str` or `Project`.")

        if isinstance(userOrProject, str):
            userOrProject = Project(
                userOrProject, portIn=portIn, portOut=portOut)

        self.projects.append = userOrProject

    def getProject(self, user="", id=-1):
        """
        This method returns all projects, if no parameters were set.
        If the parameter `user` is set, it returns all projects, which belongs to the user.
        If the `id` is set, it returns the corresponding project.

        If you set the parameter `user` and `id`, it returns the project relative to all user specific projects.

        Raises ValueError if parameter `user` or `id` are wrong types and IndexError, when you try to access lists and index is to big.
        """

        if not isinstance(user, str):
            raise ValueError("Parameter `user` is not of type string.")

        if not isinstance(id, int):
            raise ValueError("Parameter `id` is not of type int.")

        if not user:
            if id < 0:
                return self.projects
            elif id >= 0:
                return self.projects[id]

        if user:
            listOfProjects = []
            for proj in self.projects:
                if proj.user is user:
                    listOfProjects.append(proj)

            if id < 0:
                return listOfProjects
            elif id >= 0:
                return listOfProjects[id]

    def getJSON(self):
        import json
        return json.dumps(self.getDict())

    def getDict(self):
        """
        Returns a dict of all projects with a new attribute "id", which symbolize the project id in the system.
        """
        obj = []
        for i, project in enumerate(self.projects):
            d = project.getDict()
            d["id"] = i
            obj.append(d)

        return obj
