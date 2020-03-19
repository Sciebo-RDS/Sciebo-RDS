from lib.Project import Project
import logging
from lib.EnumStatus import Status

logger = logging.getLogger()


class ProjectService():
    def __init__(self):
        # format: {user: [<type project>]}
        self.projects = {}
        self.highest_index = 0

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

        projectId = self.highest_index
        self.highest_index += 1

        if userOrProject.user not in self.projects:
            self.projects[userOrProject.user] = []

        listProject = self.projects[userOrProject.user]

        userOrProject.projectId = projectId
        userOrProject.projectIndex = len(listProject)

        def getDict():
            nonlocal userOrProject, listProject
            d = userOrProject.dict
            d["projectId"] = userOrProject.projectId
            d["projectIndex"] = userOrProject.projectIndex
            return d

        userOrProject.getDict = getDict
        listProject.append(userOrProject)

        return userOrProject

    def getProject(self, user="", projectIndex: int = None, projectId: int = None):
        """
        This method returns all projects, if no parameters were set.
        If the parameter `user` is set, it returns all projects, which belongs to the user.
        If the `projectIndex` is set, it returns the corresponding project.
        **Beware:** *You start counting at Zero!*

        If you set the parameter `user` and `projectIndex`, it returns the project relative to all user specific projects.

        Raises ValueError if parameter `user` or `projectIndex` are wrong types and IndexError, when you try to access lists and index is to big.
        """

        if not isinstance(user, str):
            raise ValueError("Parameter `user` is not of type string.")

        if not isinstance(projectIndex, (int, type(None))):
            raise ValueError("Parameter projectIndex` is not of type int.")

        if not user:
            if projectId is None:
                return self.getAllProjects()
            elif projectId >= 0:
                for proj in self.getAllProjects():
                    if proj.projectId is projectId:
                        return proj

        if user:
            listOfProjects = self.projects.get(user, None)
            if listOfProjects is None:
                from lib.Exceptions.ProjectServiceExceptions import NotFoundUserError
                raise NotFoundUserError(user, projectIndex)

            if projectIndex is None:
                return listOfProjects

            # this assumes, that projectIndex could also be a projectId
            # for proj in listOfProjects:
            #     if proj.projectId == projectIndex:
            #         return proj

            if projectIndex < len(listOfProjects):
                return listOfProjects[projectIndex]

        from lib.Exceptions.ProjectServiceExceptions import NotFoundIDError
        raise NotFoundIDError(user, projectIndex)

    def removeProject(self, user: str = None, projectIndex: int = None, projectId: int = None):
        """
        This method removes the projects for given user. 

        If projectIndex was given, only the corresponding projectIndex will be removed (no user required, but it is faster).
        Returns True if it is successful or raise an exception if user or projectIndex not found. Else returns false.
        """
        if user is not None:
            if projectIndex is not None:
                rmv_id = None

                for index, proj in enumerate(self.getProject(user)):
                    if proj.projectIndex == projectIndex:
                        rmv_id = index

                try:
                    self.projects[user][rmv_id].status = Status.DELETED
                    #del self.projects[user][rmv_id]
                except:
                    logger.debug("id {} not found for user {}, try to find projectIndex as index".format(
                        projectIndex, user))

                    try:
                        self.projects[user][projectIndex].status = Status.DELETED
                        #del self.projects[user][projectIndex]
                        return True
                    except:
                        from lib.Exceptions.ProjectServiceExceptions import NotFoundIDError
                        raise NotFoundIDError(user, projectIndex)

            else:
                try:
                    found = False
                    for proj in self.projects[user]:
                        if proj.status != Status.DELETED:
                            proj.status = Status.DELETED
                            found = True

                    if not found:
                        raise Exception
                    #del self.projects[user]
                    
                except:
                    from lib.Exceptions.ProjectServiceExceptions import NotFoundUserError
                    raise NotFoundUserError(user, projectIndex)
            return True

        if projectId is not None:
            for user, listOfProjects in self.projects.items():
                rmv_id = None
                for index, proj in enumerate(listOfProjects):
                    if proj.projectId is projectId:
                        rmv_id = index

                try:
                    self.projects[user][rmv_id].status = Status.DELETED
                    #del self.projects[user][rmv_id]
                except:
                    from lib.Exceptions.ProjectServiceExceptions import NotFoundIDError
                    raise NotFoundIDError(user, projectId)
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
        Returns a dict of all projects with a new attribute "id", which symbolize the project projectIndex in the system.
        """
        returnList = []

        for listProjects in self.projects.values():
            for index, proj in enumerate(listProjects):
                d = proj.getDict()
                returnList.append(d)

        return returnList

    def __eq__(self, obj):
        if not isinstance(obj, Project):
            return False

        return (self.getDict() == obj.getDict())
