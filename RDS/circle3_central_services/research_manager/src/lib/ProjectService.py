from lib.Project import Project
import logging
import requests, os
from lib.EnumStatus import Status
from RDS import Util

logger = logging.getLogger()


def keys(self):
    prefix = self.prefixer("")
    for k in self._keys():
        val = k.replace(prefix, "", 1)
        yield val


class ProjectService:
    def __init__(self, rc=None, use_in_memory_on_failure=True):
        # format: {user: [<type project>]}
        try:
            from redis_pubsub_dict import RedisDict
            import redis_pubsub_dict, functools, json

            redis_pubsub_dict.dumps = lambda x: json.dumps(x)
            redis_pubsub_dict.loads = lambda x: Util.try_function_on_dict(
                [Project.fromJSON]
            )(x)
            redis_pubsub_dict.RedisDict.to_json = lambda x: dict(x.items())
            redis_pubsub_dict.RedisDict.__eq__ = (
                lambda x, other: dict(x.items()) == other
            )
            redis_pubsub_dict.RedisDict.keys = keys

            # runs in RDS ecosystem

            if rc is None:
                logger.debug("No redis client was given. Create one.")
                startup_nodes = [
                    {
                        "host": os.getenv("REDIS_HOST", "localhost"),
                        "port": os.getenv("REDIS_PORT", "6379"),
                    }
                ]

                try:
                    logger.debug("first try cluster")
                    from rediscluster import RedisCluster

                    rc = RedisCluster(
                        startup_nodes=startup_nodes, decode_responses=True,
                    )
                except Exception as e:
                    logger.error(e)
                    logger.debug("Cluster has an error, try standardalone redis")
                    from redis import Redis

                    rc = Redis(**(startup_nodes[0]), db=0, decode_responses=True,)
                    rc.info()  # provoke an error message

            logger.debug("set redis backed dict")
            self.projects = RedisDict(rc, "researchmanager_projects")
        except Exception as e:
            logger.error(e)
            logger.info("no redis found.")

            if not use_in_memory_on_failure:
                logger.info("exit...")
                import sys

                sys.exit()

            logger.info("use in-memory")
            self.projects = {}

    @property
    def highest_index(self):
        index = 0
        for user in self.projects.values():
            index += len(user)

        return index

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

        self.projects[userOrProject.user] = listProject

        return userOrProject

    def setProject(self, user, project):
        try:
            projects = self.projects[user.username]
        except:
            projects = self.projects.get(user)

        if projects is None:
            self.projects[user] = [project]
        else:
            projects[project.researchIndex] = project
            self.projects[user] = projects

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
                    projects = self.projects[user]
                    projects[rmv_id].status = Status.DELETED
                    self.projects[user] = projects
                    # del self.projects[user][rmv_id]
                except:
                    logger.debug(
                        "id {} not found for user {}, try to find researchIndex as index".format(
                            researchIndex, user
                        )
                    )

                    try:
                        projects = self.projects[user]
                        projects[researchIndex].status = Status.DELETED
                        self.projects[user] = projects
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
                    projects = self.projects[user]
                    for proj in projects:
                        if proj.status != Status.DELETED:
                            proj.status = Status.DELETED
                            found = True

                    self.projects[user] = projects

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
                    projects = self.projects[user]
                    projects[rmv_id].status = Status.DELETED
                    self.projects[user] = projects
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
