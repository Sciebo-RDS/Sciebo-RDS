from lib.Project import Project
import logging
import requests, os
from lib.EnumStatus import Status

logger = logging.getLogger()


class ProjectService:
    def __init__(self):
        # format: {user: [<type project>]}
        if os.getenv("RDS_OAUTH_REDIRECT_URI") is not None:
            from redis_pubsub_dict import RedisDict
            from rediscluster import StrictRedisCluster
            # runs in RDS ecosystem
            rc = StrictRedisCluster(startup_nodes=[{"host": "redis", "port": "6379"}])
            self.projects = RedisDict(rc, 'researchmanager_projects')
        else:
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
                "The parameter `userOrProject` is not of type `str` or `Project`."
            )

        if isinstance(userOrProject, str):
            userOrProject = Project(userOrProject, portIn=portIn, portOut=portOut)

        researchId = self.highest_index
        self.highest_index += 1

        if userOrProject.user not in self.projects:
            self.projects[userOrProject.user] = []

        listProject = self.projects[userOrProject.user]

        userOrProject.researchId = researchId
        userOrProject.researchIndex = len(listProject)

        def getDict():
            nonlocal userOrProject, listProject
            d = userOrProject.dict
            d["researchId"] = userOrProject.researchId
            d["researchIndex"] = userOrProject.researchIndex
            return d

        userOrProject.getDict = getDict
        listProject.append(userOrProject)

        return userOrProject

    def getProject(self, user="", researchIndex: int = None, researchId: int = None):
        """
        This method returns all projects, if no parameters were set.
        If the parameter `user` is set, it returns all projects, which belongs to the user.
        If the `researchIndex` is set, it returns the corresponding project.
        **Beware:** *You start counting at Zero!*

        If you set the parameter `user` and `researchIndex`, it returns the project relative to all user specific projects.

        Raises ValueError if parameter `user` or `researchIndex` are wrong types and IndexError, when you try to access lists and index is to big.
        """

        if not isinstance(user, str):
            raise ValueError("Parameter `user` is not of type string.")

        if not isinstance(researchIndex, (int, type(None))):
            raise ValueError("Parameter researchIndex` is not of type int.")

        if not user:
            if researchId is None:
                return self.getAllProjects()
            elif researchId >= 0:
                for proj in self.getAllProjects():
                    if proj.researchId is researchId:
                        return proj

        if user:
            listOfProjects = self.projects.get(user, None)
            if listOfProjects is None:
                from lib.Exceptions.ProjectServiceExceptions import NotFoundUserError

                raise NotFoundUserError(user, researchIndex)

            if researchIndex is None:
                return listOfProjects

            # this assumes, that researchIndex could also be a researchId
            # for proj in listOfProjects:
            #     if proj.researchId == researchIndex:
            #         return proj

            if researchIndex < len(listOfProjects):
                return listOfProjects[researchIndex]

        from lib.Exceptions.ProjectServiceExceptions import NotFoundIDError

        raise NotFoundIDError(user, researchIndex)

    def removeProject(
        self, user: str = None, researchIndex: int = None, researchId: int = None
    ):
        """
        This method removes the projects for given user. 

        If researchIndex was given, only the corresponding researchIndex will be removed (no user required, but it is faster).
        Returns True if it is successful or raise an exception if user or researchIndex not found. Else returns false.
        """
        if user is not None:
            if researchIndex is not None:
                rmv_id = None

                for index, proj in enumerate(self.getProject(user)):
                    if proj.researchIndex == researchIndex:
                        rmv_id = index

                try:
                    self.projects[user][rmv_id].status = Status.DELETED
                    # del self.projects[user][rmv_id]
                except:
                    logger.debug(
                        "id {} not found for user {}, try to find researchIndex as index".format(
                            researchIndex, user
                        )
                    )

                    try:
                        self.projects[user][researchIndex].status = Status.DELETED
                        # del self.projects[user][researchIndex]
                        return True
                    except:
                        from lib.Exceptions.ProjectServiceExceptions import (
                            NotFoundIDError,
                        )

                        raise NotFoundIDError(user, researchIndex)

            else:
                try:
                    found = False
                    for proj in self.projects[user]:
                        if proj.status != Status.DELETED:
                            proj.status = Status.DELETED
                            found = True

                    if not found:
                        raise Exception
                    # del self.projects[user]

                except:
                    from lib.Exceptions.ProjectServiceExceptions import (
                        NotFoundUserError,
                    )

                    raise NotFoundUserError(user, researchIndex)
            return True

        if researchId is not None:
            for user, listOfProjects in self.projects.items():
                rmv_id = None
                for index, proj in enumerate(listOfProjects):
                    if proj.researchId is researchId:
                        rmv_id = index

                try:
                    self.projects[user][rmv_id].status = Status.DELETED
                    # del self.projects[user][rmv_id]
                except:
                    from lib.Exceptions.ProjectServiceExceptions import NotFoundIDError

                    raise NotFoundIDError(user, researchId)
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
        Returns a dict of all projects with a new attribute "id", which symbolize the project researchIndex in the system.
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

        return self.getDict() == obj.getDict()

    def removeUser(self, user: str):
        """Removes user and all projects.

        Args:
            user (str): The username, which should be removed.
        """
        if self.projects.get(user) is not None:
            del self.projects[user]
            return True

        return False
