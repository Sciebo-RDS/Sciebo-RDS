config = {
    "modules": [
        # if you add a module here please also add it to the root level Makefile
        "accounts",
        "glauth",
        "graph-explorer",
        "graph",
        "idp",
        "ocis-pkg",
        "ocis",
        "ocs",
        "onlyoffice",
        "proxy",
        "settings",
        "storage",
        "store",
        "thumbnails",
        "web",
        "webdav",
    ],
    "localApiTests": {
        "skip": False,
        "earlyFail": True,
    },
    "apiTests": {
        "numberOfParts": 10,
        "skip": False,
        "skipExceptParts": [],
        "earlyFail": True,
    },
    "uiTests": {
        "filterTags": "@ocisSmokeTest",
        "skip": False,
        "skipExceptParts": [],
        "earlyFail": True,
    },
    "accountsUITests": {
        "skip": False,
        "earlyFail": True,
    },
    "settingsUITests": {
        "skip": False,
        "earlyFail": True,
    },
    "rocketchat": {
        "channel": "ocis-internal",
        "from_secret": "private_rocketchat",
    },
    "binaryReleases": {
        "os": ["linux", "darwin", "windows"],
    },
    "dockerReleases": {
        "architectures": ["arm", "arm64", "amd64"],
    },
}

# volume for steps to cache Go dependencies between steps of a pipeline
# GOPATH must be set to /go inside the image, which is the case
stepVolumeGo = \
    {
        "name": "gopath",
        "path": "/go",
    }

# volume for pipeline to cache Go dependencies between steps of a pipeline
# to be used in combination with stepVolumeGo
pipelineVolumeGo = \
    {
        "name": "gopath",
        "temp": {},
    }

stepVolumeOC10Tests = \
    {
        "name": "oC10Tests",
        "path": "/srv/app",
    }

pipelineVolumeOC10Tests = \
    {
        "name": "oC10Tests",
        "temp": {},
    }

def pipelineDependsOn(pipeline, dependant_pipelines):
    if "depends_on" in pipeline.keys():
        pipeline["depends_on"] = pipeline["depends_on"] + getPipelineNames(dependant_pipelines)
    else:
        pipeline["depends_on"] = getPipelineNames(dependant_pipelines)
    return pipeline

def pipelinesDependsOn(pipelines, dependant_pipelines):
    pipes = []
    for pipeline in pipelines:
        pipes.append(pipelineDependsOn(pipeline, dependant_pipelines))

    return pipes

def getPipelineNames(pipelines = []):
    """getPipelineNames returns names of pipelines as a string array

    Args:
      pipelines: array of drone pipelines

    Returns:
      names of the given pipelines as string array
    """
    names = []
    for pipeline in pipelines:
        names.append(pipeline["name"])
    return names

def main(ctx):
    """main is the entrypoint for drone

    Args:
      ctx: drone passes a context with information which the pipeline can be adapted to

    Returns:
      none
    """

    pipelines = []

    test_pipelines = \
        [buildOcisBinaryForTesting(ctx)] + \
        testOcisModules(ctx) + \
        testPipelines(ctx)

    build_release_pipelines = \
        dockerReleases(ctx) + \
        [dockerEos(ctx)] + \
        binaryReleases(ctx) + \
        [releaseSubmodule(ctx)]

    build_release_helpers = [
        changelog(ctx),
        docs(ctx),
    ]

    if ctx.build.event == "cron":
        pipelines = test_pipelines + [
            pipelineDependsOn(
                purgeBuildArtifactCache(ctx, "ocis-binary-amd64"),
                testPipelines(ctx),
            ),
        ] + example_deploys(ctx)

    elif (ctx.build.event == "pull_request" and "[docs-only]" in ctx.build.title) or \
         (ctx.build.event != "pull_request" and "[docs-only]" in (ctx.build.title + ctx.build.message)):
        # [docs-only] is not taken from PR messages, but from commit messages
        pipelines = [docs(ctx)]

    else:
        test_pipelines.append(
            pipelineDependsOn(
                purgeBuildArtifactCache(ctx, "ocis-binary-amd64"),
                testPipelines(ctx),
            ),
        )

        pipelines = test_pipelines + build_release_pipelines + build_release_helpers

        pipelines = \
            pipelines + \
            pipelinesDependsOn(
                example_deploys(ctx),
                pipelines,
            )

    # always append notification step
    pipelines.append(
        pipelineDependsOn(
            notify(ctx),
            pipelines,
        ),
    )

    pipelines += checkStarlark()
    pipelineSanityChecks(ctx, pipelines)
    return pipelines

def testOcisModules(ctx):
    pipelines = []
    for module in config["modules"]:
        pipelines.append(testOcisModule(ctx, module))

    scan_result_upload = uploadScanResults(ctx)
    scan_result_upload["depends_on"] = getPipelineNames(pipelines)

    return pipelines + [scan_result_upload]

def testPipelines(ctx):
    pipelines = []
    if "skip" not in config["localApiTests"] or not config["localApiTests"]["skip"]:
        pipelines = [
            localApiTests(ctx, "owncloud", "apiBugDemonstration"),
            localApiTests(ctx, "ocis", "apiBugDemonstration"),
            localApiTests(ctx, "owncloud", "apiAccountsHashDifficulty", "default"),
            localApiTests(ctx, "ocis", "apiAccountsHashDifficulty", "default"),
        ]

    if "skip" not in config["apiTests"] or not config["apiTests"]["skip"]:
        pipelines += apiTests(ctx)

    if "skip" not in config["uiTests"] or not config["uiTests"]["skip"]:
        pipelines += uiTests(ctx)

    if "skip" not in config["accountsUITests"] or not config["accountsUITests"]["skip"]:
        pipelines.append(accountsUITests(ctx))

    if "skip" not in config["settingsUITests"] or not config["settingsUITests"]["skip"]:
        pipelines.append(settingsUITests(ctx))

    return pipelines

def testOcisModule(ctx, module):
    steps = makeGenerate(module) + [
        {
            "name": "golangci-lint",
            "image": "owncloudci/golang:1.16",
            "pull": "always",
            "commands": [
                "mkdir -p cache/checkstyle",
                "make -C %s ci-golangci-lint" % (module),
                "mv %s/checkstyle.xml cache/checkstyle/%s_checkstyle.xml" % (module, module),
            ],
            "volumes": [stepVolumeGo],
        },
        {
            "name": "test",
            "image": "owncloudci/golang:1.16",
            "pull": "always",
            "commands": [
                "mkdir -p cache/coverage",
                "make -C %s test" % (module),
                "mv %s/coverage.out cache/coverage/%s_coverage.out" % (module, module),
            ],
            "volumes": [stepVolumeGo],
        },
        {
            "name": "scan-result-cache",
            "image": "plugins/s3:1",
            "settings": {
                "endpoint": {
                    "from_secret": "cache_s3_endpoint",
                },
                "bucket": "cache",
                "source": "cache/**/*",
                "target": "%s/%s" % (ctx.repo.slug, ctx.build.commit + "-${DRONE_BUILD_NUMBER}"),
                "path_style": True,
                "access_key": {
                    "from_secret": "cache_s3_access_key",
                },
                "secret_key": {
                    "from_secret": "cache_s3_secret_key",
                },
            },
        },
    ]

    return {
        "kind": "pipeline",
        "type": "docker",
        "name": "linting&unitTests-%s" % (module),
        "platform": {
            "os": "linux",
            "arch": "amd64",
        },
        "steps": steps,
        "trigger": {
            "ref": [
                "refs/heads/master",
                "refs/tags/v*",
                "refs/tags/%s/v*" % (module),
                "refs/pull/**",
            ],
        },
        "volumes": [pipelineVolumeGo],
    }

def buildOcisBinaryForTesting(ctx):
    return {
        "kind": "pipeline",
        "type": "docker",
        "name": "build_ocis_binary_for_testing",
        "platform": {
            "os": "linux",
            "arch": "amd64",
        },
        "steps": makeGenerate("") +
                 build() +
                 rebuildBuildArtifactCache(ctx, "ocis-binary-amd64", "ocis/bin/ocis"),
        "trigger": {
            "ref": [
                "refs/heads/master",
                "refs/tags/v*",
                "refs/pull/**",
            ],
        },
        "volumes": [pipelineVolumeGo],
    }

def uploadScanResults(ctx):
    sonar_env = {
        "SONAR_TOKEN": {
            "from_secret": "sonar_token",
        },
    }
    if ctx.build.event == "pull_request":
        sonar_env.update({
            "SONAR_PULL_REQUEST_BASE": "%s" % (ctx.build.target),
            "SONAR_PULL_REQUEST_BRANCH": "%s" % (ctx.build.source),
            "SONAR_PULL_REQUEST_KEY": "%s" % (ctx.build.ref.replace("refs/pull/", "").split("/")[0]),
        })

    repo_slug = ctx.build.source_repo if ctx.build.source_repo else ctx.repo.slug

    return {
        "kind": "pipeline",
        "type": "docker",
        "name": "upload-scan-results",
        "platform": {
            "os": "linux",
            "arch": "amd64",
        },
        "clone": {
            "disable": True,  # Sonarcloud does not apply issues on already merged branch
        },
        "steps": [
            {
                "name": "clone",
                "image": "alpine/git:latest",
                "commands": [
                    "git clone https://github.com/%s.git ." % (repo_slug),
                    "git checkout $DRONE_COMMIT",
                ],
            },
            {
                "name": "sync-from-cache",
                "image": "minio/mc:RELEASE.2021-03-23T05-46-11Z",
                "environment": {
                    "MC_HOST_cachebucket": {
                        "from_secret": "cache_s3_connection_url",
                    },
                },
                "commands": [
                    "mkdir -p cache",
                    "mc mirror cachebucket/cache/%s/%s/cache cache/" % (ctx.repo.slug, ctx.build.commit + "-${DRONE_BUILD_NUMBER}"),
                ],
            },
            {
                "name": "codacy",
                "image": "plugins/codacy:1",
                "pull": "always",
                "settings": {
                    "token": {
                        "from_secret": "codacy_token",
                    },
                },
            },
            {
                "name": "sonarcloud",
                "image": "sonarsource/sonar-scanner-cli:latest",
                "pull": "always",
                "environment": sonar_env,
            },
            {
                "name": "purge-cache",
                "image": "minio/mc:RELEASE.2021-03-23T05-46-11Z",
                "environment": {
                    "MC_HOST_cachebucket": {
                        "from_secret": "cache_s3_connection_url",
                    },
                },
                "commands": [
                    "mc rm --recursive --force cachebucket/cache/%s/%s/cache" % (ctx.repo.slug, ctx.build.commit + "-${DRONE_BUILD_NUMBER}"),
                ],
            },
        ],
        "trigger": {
            "ref": [
                "refs/heads/master",
                "refs/tags/v*",
                "refs/pull/**",
            ],
        },
    }

def localApiTests(ctx, storage = "owncloud", suite = "apiBugDemonstration", accounts_hash_difficulty = 4):
    earlyFail = config["localApiTests"]["earlyFail"] if "earlyFail" in config["localApiTests"] else False

    if ("full-ci" in ctx.build.title.lower()):
        earlyFail = False

    return {
        "kind": "pipeline",
        "type": "docker",
        "name": "localApiTests-%s-%s" % (suite, storage),
        "platform": {
            "os": "linux",
            "arch": "amd64",
        },
        "steps": restoreBuildArtifactCache(ctx, "ocis-binary-amd64", "ocis/bin/ocis") +
                 ocisServer(storage, accounts_hash_difficulty, [stepVolumeOC10Tests]) +
                 cloneCoreRepos() + [
            {
                "name": "localApiTests-%s-%s" % (suite, storage),
                "image": "owncloudci/php:7.4",
                "pull": "always",
                "environment": {
                    "TEST_SERVER_URL": "https://ocis-server:9200",
                    "OCIS_REVA_DATA_ROOT": "%s" % ("/srv/app/tmp/ocis/owncloud/data/" if storage == "owncloud" else ""),
                    "SKELETON_DIR": "/srv/app/tmp/testing/data/apiSkeleton",
                    "OCIS_SKELETON_STRATEGY": "%s" % ("copy" if storage == "owncloud" else "upload"),
                    "TEST_OCIS": "true",
                    "STORAGE_DRIVER": storage,
                    "BEHAT_SUITE": suite,
                    "BEHAT_FILTER_TAGS": "~@skip&&~@skipOnOcis-%s-Storage" % ("OC" if storage == "owncloud" else "OCIS"),
                    "PATH_TO_CORE": "/srv/app/testrunner",
                    "UPLOAD_DELETE_WAIT_TIME": "1" if storage == "owncloud" else 0,
                },
                "commands": [
                    "make test-acceptance-api",
                ],
                "volumes": [stepVolumeOC10Tests],
            },
        ] + buildGithubCommentForBuildStopped("localApiTests-%s-%s" % (suite, storage), earlyFail) + githubComment(earlyFail) + stopBuild(earlyFail),
        "services": redisForOCStorage(storage),
        "depends_on": getPipelineNames([buildOcisBinaryForTesting(ctx)]),
        "trigger": {
            "ref": [
                "refs/heads/master",
                "refs/tags/v*",
                "refs/pull/**",
            ],
        },
        "volumes": [pipelineVolumeOC10Tests],
    }

def coreApiTests(ctx, part_number = 1, number_of_parts = 1, storage = "owncloud", accounts_hash_difficulty = 4):
    earlyFail = config["apiTests"]["earlyFail"] if "earlyFail" in config["apiTests"] else False

    if ("full-ci" in ctx.build.title.lower()):
        earlyFail = False

    return {
        "kind": "pipeline",
        "type": "docker",
        "name": "Core-API-Tests-%s-storage-%s" % (storage, part_number),
        "platform": {
            "os": "linux",
            "arch": "amd64",
        },
        "steps": restoreBuildArtifactCache(ctx, "ocis-binary-amd64", "ocis/bin/ocis") +
                 ocisServer(storage, accounts_hash_difficulty, [stepVolumeOC10Tests]) +
                 cloneCoreRepos() + [
            {
                "name": "oC10ApiTests-%s-storage-%s" % (storage, part_number),
                "image": "owncloudci/php:7.4",
                "pull": "always",
                "environment": {
                    "TEST_SERVER_URL": "https://ocis-server:9200",
                    "OCIS_REVA_DATA_ROOT": "%s" % ("/srv/app/tmp/ocis/owncloud/data/" if storage == "owncloud" else ""),
                    "SKELETON_DIR": "/srv/app/tmp/testing/data/apiSkeleton",
                    "OCIS_SKELETON_STRATEGY": "%s" % ("copy" if storage == "owncloud" else "upload"),
                    "TEST_OCIS": "true",
                    "STORAGE_DRIVER": storage,
                    "BEHAT_FILTER_TAGS": "~@skipOnOcis&&~@notToImplementOnOCIS&&~@toImplementOnOCIS&&~comments-app-required&&~@federation-app-required&&~@notifications-app-required&&~systemtags-app-required&&~@local_storage&&~@skipOnOcis-%s-Storage" % ("OC" if storage == "owncloud" else "OCIS"),
                    "DIVIDE_INTO_NUM_PARTS": number_of_parts,
                    "RUN_PART": part_number,
                    "EXPECTED_FAILURES_FILE": "/drone/src/tests/acceptance/expected-failures-API-on-%s-storage.md" % (storage.upper()),
                    "UPLOAD_DELETE_WAIT_TIME": "1" if storage == "owncloud" else 0,
                },
                "commands": [
                    "make -C /srv/app/testrunner test-acceptance-api",
                ],
                "volumes": [stepVolumeOC10Tests],
            },
        ] + buildGithubCommentForBuildStopped("Core-API-Tests-%s-storage-%s" % (storage, part_number), earlyFail) + githubComment(earlyFail) + stopBuild(earlyFail),
        "services": redisForOCStorage(storage),
        "depends_on": getPipelineNames([buildOcisBinaryForTesting(ctx)]),
        "trigger": {
            "ref": [
                "refs/heads/master",
                "refs/tags/v*",
                "refs/pull/**",
            ],
        },
        "volumes": [pipelineVolumeOC10Tests],
    }

def apiTests(ctx):
    pipelines = []
    debugParts = config["apiTests"]["skipExceptParts"]
    debugPartsEnabled = (len(debugParts) != 0)
    for runPart in range(1, config["apiTests"]["numberOfParts"] + 1):
        if (not debugPartsEnabled or (debugPartsEnabled and runPart in debugParts)):
            pipelines.append(coreApiTests(ctx, runPart, config["apiTests"]["numberOfParts"], "owncloud"))
            pipelines.append(coreApiTests(ctx, runPart, config["apiTests"]["numberOfParts"], "ocis"))

    return pipelines

def uiTests(ctx):
    default = {
        "filterTags": "",
        "skip": False,
        "earlyFail": False,
        # only used if 'full-ci' is in build title
        "numberOfParts": 10,
        "skipExceptParts": [],
    }
    params = {}
    pipelines = []

    for item in default:
        params[item] = config["uiTests"][item] if item in config["uiTests"] else default[item]

    filterTags = params["filterTags"]
    earlyFail = params["earlyFail"]

    if ("full-ci" in ctx.build.title.lower()):
        earlyFail = False

    if ("full-ci" in ctx.build.title.lower() or ctx.build.event == "tag"):
        numberOfParts = params["numberOfParts"]
        skipExceptParts = params["skipExceptParts"]
        debugPartsEnabled = (len(skipExceptParts) != 0)

        for runPart in range(1, numberOfParts + 1):
            if (not debugPartsEnabled or (debugPartsEnabled and runPart in skipExceptParts)):
                pipelines.append(uiTestPipeline(ctx, "", earlyFail, runPart, numberOfParts))

    # For ordinary PRs, always run the "minimal" UI test pipeline
    # That has its own expected-failures file, and we always want to know that it is correct,
    if (ctx.build.event != "tag"):
        pipelines.append(uiTestPipeline(ctx, filterTags, earlyFail))

    return pipelines

def uiTestPipeline(ctx, filterTags, earlyFail, runPart = 1, numberOfParts = 1, storage = "ocis", accounts_hash_difficulty = 4):
    standardFilterTags = "not @skipOnOCIS and not @skip and not @notToImplementOnOCIS and not @federated-server-needed"
    if filterTags == "":
        finalFilterTags = standardFilterTags
        expectedFailuresFileFilterTags = ""
    else:
        finalFilterTags = filterTags + " and " + standardFilterTags
        expectedFailuresFileFilterTags = "-" + filterTags.lstrip("@")

    if numberOfParts == 1:
        pipelineName = "Web-Tests-ocis-%s-storage" % storage
    else:
        pipelineName = "Web-Tests-ocis-%s-storage-%s" % (storage, runPart)

    return {
        "kind": "pipeline",
        "type": "docker",
        "name": pipelineName,
        "platform": {
            "os": "linux",
            "arch": "amd64",
        },
        "steps": restoreBuildArtifactCache(ctx, "ocis-binary-amd64", "ocis/bin/ocis") +
                 ocisServer(storage, accounts_hash_difficulty, [stepVolumeOC10Tests]) + [
            {
                "name": "webUITests",
                "image": "owncloudci/nodejs:14",
                "pull": "always",
                "environment": {
                    "SERVER_HOST": "https://ocis-server:9200",
                    "BACKEND_HOST": "https://ocis-server:9200",
                    "RUN_ON_OCIS": "true",
                    "OCIS_REVA_DATA_ROOT": "/srv/app/tmp/ocis/owncloud/data",
                    "TESTING_DATA_DIR": "/srv/app/testing/data",
                    "WEB_UI_CONFIG": "/drone/src/tests/config/drone/ocis-config.json",
                    "TEST_TAGS": finalFilterTags,
                    "LOCAL_UPLOAD_DIR": "/uploads",
                    "NODE_TLS_REJECT_UNAUTHORIZED": 0,
                    "RUN_PART": runPart,
                    "DIVIDE_INTO_NUM_PARTS": numberOfParts,
                    "EXPECTED_FAILURES_FILE": "/drone/src/tests/acceptance/expected-failures-webUI-on-%s-storage%s.md" % (storage.upper(), expectedFailuresFileFilterTags),
                },
                "commands": [
                    ". /drone/src/.drone.env",
                    "git clone -b master --depth=1 https://github.com/owncloud/testing.git /srv/app/testing",
                    "git clone -b $WEB_BRANCH --single-branch --no-tags https://github.com/owncloud/web.git /srv/app/web",
                    "cd /srv/app/web",
                    "git checkout $WEB_COMMITID",
                    "cp -r tests/acceptance/filesForUpload/* /uploads",
                    "yarn install --all",
                    "yarn build",
                    "./tests/acceptance/run.sh",
                ],
                "volumes": [stepVolumeOC10Tests] +
                           [{
                               "name": "uploads",
                               "path": "/uploads",
                           }],
            },
        ] + buildGithubCommentForBuildStopped("Web-Tests-ocis-%s-storage-%s" % (storage, runPart), earlyFail) + githubComment(earlyFail) + stopBuild(earlyFail),
        "services": selenium(),
        "volumes": [pipelineVolumeOC10Tests] +
                   [{
                       "name": "uploads",
                       "temp": {},
                   }],
        "depends_on": getPipelineNames([buildOcisBinaryForTesting(ctx)]),
        "trigger": {
            "ref": [
                "refs/heads/master",
                "refs/tags/v*",
                "refs/pull/**",
            ],
        },
    }

def accountsUITests(ctx, storage = "ocis", accounts_hash_difficulty = 4):
    earlyFail = config["accountsUITests"]["earlyFail"] if "earlyFail" in config["accountsUITests"] else False

    if ("full-ci" in ctx.build.title.lower()):
        earlyFail = False

    return {
        "kind": "pipeline",
        "type": "docker",
        "name": "accountsUITests",
        "platform": {
            "os": "linux",
            "arch": "amd64",
        },
        "steps": restoreBuildArtifactCache(ctx, "ocis-binary-amd64", "ocis/bin/ocis") +
                 ocisServer(storage, accounts_hash_difficulty, [stepVolumeOC10Tests]) + [
            {
                "name": "WebUIAcceptanceTests",
                "image": "owncloudci/nodejs:14",
                "pull": "always",
                "environment": {
                    "SERVER_HOST": "https://ocis-server:9200",
                    "BACKEND_HOST": "https://ocis-server:9200",
                    "RUN_ON_OCIS": "true",
                    "OCIS_REVA_DATA_ROOT": "/srv/app/tmp/ocis/owncloud/data",
                    "OCIS_SKELETON_DIR": "/srv/app/testing/data/webUISkeleton",
                    "WEB_UI_CONFIG": "/drone/src/tests/config/drone/ocis-config.json",
                    "TEST_TAGS": "not @skipOnOCIS and not @skip",
                    "LOCAL_UPLOAD_DIR": "/uploads",
                    "NODE_TLS_REJECT_UNAUTHORIZED": 0,
                    "WEB_PATH": "/srv/app/web",
                    "FEATURE_PATH": "/drone/src/accounts/ui/tests/acceptance/features",
                },
                "commands": [
                    ". /drone/src/.drone.env",
                    "git clone -b master --depth=1 https://github.com/owncloud/testing.git /srv/app/testing",
                    "git clone -b $WEB_BRANCH --single-branch --no-tags https://github.com/owncloud/web.git /srv/app/web",
                    "cd /srv/app/web",
                    "git checkout $WEB_COMMITID",
                    "cp -r tests/acceptance/filesForUpload/* /uploads",
                    "yarn install --all",
                    "yarn build",
                    "cd /drone/src/accounts",
                    "yarn install --all",
                    "make test-acceptance-webui",
                ],
                "volumes": [stepVolumeOC10Tests] +
                           [{
                               "name": "uploads",
                               "path": "/uploads",
                           }],
            },
        ] + buildGithubCommentForBuildStopped("accountsUITests", earlyFail) + githubComment(earlyFail) + stopBuild(earlyFail),
        "services": selenium(),
        "volumes": [stepVolumeOC10Tests] +
                   [{
                       "name": "uploads",
                       "temp": {},
                   }],
        "depends_on": getPipelineNames([buildOcisBinaryForTesting(ctx)]),
        "trigger": {
            "ref": [
                "refs/heads/master",
                "refs/tags/v*",
                "refs/pull/**",
            ],
        },
    }

def settingsUITests(ctx, storage = "ocis", accounts_hash_difficulty = 4):
    earlyFail = config["settingsUITests"]["earlyFail"] if "earlyFail" in config["settingsUITests"] else False

    if ("full-ci" in ctx.build.title.lower()):
        earlyFail = False

    return {
        "kind": "pipeline",
        "type": "docker",
        "name": "settingsUITests",
        "platform": {
            "os": "linux",
            "arch": "amd64",
        },
        "steps": restoreBuildArtifactCache(ctx, "ocis-binary-amd64", "ocis/bin/ocis") +
                 ocisServer(storage, accounts_hash_difficulty, [stepVolumeOC10Tests]) + [
            {
                "name": "WebUIAcceptanceTests",
                "image": "owncloudci/nodejs:14",
                "pull": "always",
                "environment": {
                    "SERVER_HOST": "https://ocis-server:9200",
                    "BACKEND_HOST": "https://ocis-server:9200",
                    "RUN_ON_OCIS": "true",
                    "OCIS_REVA_DATA_ROOT": "/srv/app/tmp/ocis/owncloud/data",
                    "WEB_UI_CONFIG": "/drone/src/tests/config/drone/ocis-config.json",
                    "TEST_TAGS": "not @skipOnOCIS and not @skip",
                    "LOCAL_UPLOAD_DIR": "/uploads",
                    "NODE_TLS_REJECT_UNAUTHORIZED": 0,
                    "WEB_PATH": "/srv/app/web",
                    "FEATURE_PATH": "/drone/src/settings/ui/tests/acceptance/features",
                },
                "commands": [
                    ". /drone/src/.drone.env",
                    "git clone -b master --depth=1 https://github.com/owncloud/testing.git /srv/app/testing",
                    "git clone -b $WEB_BRANCH --single-branch --no-tags https://github.com/owncloud/web.git /srv/app/web",
                    "cp -r /srv/app/web/tests/acceptance/filesForUpload/* /uploads",
                    "cd /srv/app/web",
                    "git checkout $WEB_COMMITID",
                    "yarn install --all",
                    "cd /drone/src/settings",
                    "yarn install --all",
                    "make test-acceptance-webui",
                ],
                "volumes": [stepVolumeOC10Tests] +
                           [{
                               "name": "uploads",
                               "path": "/uploads",
                           }],
            },
        ] + buildGithubCommentForBuildStopped("settingsUITests", earlyFail) + githubComment(earlyFail) + stopBuild(earlyFail),
        "services": [
            {
                "name": "redis",
                "image": "redis:6-alpine",
                "pull": "always",
            },
        ] + selenium(),
        "volumes": [stepVolumeOC10Tests] +
                   [{
                       "name": "uploads",
                       "temp": {},
                   }],
        "depends_on": getPipelineNames([buildOcisBinaryForTesting(ctx)]),
        "trigger": {
            "ref": [
                "refs/heads/master",
                "refs/tags/v*",
                "refs/pull/**",
            ],
        },
    }

def stopBuild(earlyFail):
    if (earlyFail):
        return [{
            "name": "stop-build",
            "image": "drone/cli:alpine",
            "pull": "always",
            "environment": {
                "DRONE_SERVER": "https://drone.owncloud.com",
                "DRONE_TOKEN": {
                    "from_secret": "drone_token",
                },
            },
            "commands": [
                "drone build stop owncloud/ocis ${DRONE_BUILD_NUMBER}",
            ],
            "when": {
                "status": [
                    "failure",
                ],
                "event": [
                    "pull_request",
                ],
            },
        }]

    else:
        return []

def buildGithubCommentForBuildStopped(alternateSuiteName, earlyFail):
    if (earlyFail):
        return [{
            "name": "build-github-comment-buildStop",
            "image": "owncloud/ubuntu:16.04",
            "pull": "always",
            "commands": [
                'echo "<details><summary>:boom: Acceptance tests <strong>%s</strong> failed. The build is cancelled...</summary>\\n\\n" >> /drone/src/comments.file' % alternateSuiteName,
            ],
            "when": {
                "status": [
                    "failure",
                ],
                "event": [
                    "pull_request",
                ],
            },
        }]

    else:
        return []

def githubComment(earlyFail):
    if (earlyFail):
        return [{
            "name": "github-comment",
            "image": "jmccann/drone-github-comment:1",
            "pull": "if-not-exists",
            "settings": {
                "message_file": "/drone/src/comments.file",
            },
            "environment": {
                "GITHUB_TOKEN": {
                    "from_secret": "github_token",
                },
            },
            "when": {
                "status": [
                    "failure",
                ],
                "event": [
                    "pull_request",
                ],
            },
        }]

    else:
        return []

def dockerReleases(ctx):
    pipelines = []
    for arch in config["dockerReleases"]["architectures"]:
        pipelines.append(dockerRelease(ctx, arch))

    manifest = releaseDockerManifest(ctx)
    manifest["depends_on"] = getPipelineNames(pipelines)
    pipelines.append(manifest)

    readme = releaseDockerReadme(ctx)
    readme["depends_on"] = getPipelineNames(pipelines)
    pipelines.append(readme)

    return pipelines

def dockerRelease(ctx, arch):
    build_args = [
        "REVISION=%s" % (ctx.build.commit),
        "VERSION=%s" % (ctx.build.ref.replace("refs/tags/", "") if ctx.build.event == "tag" else "latest"),
    ]

    return {
        "kind": "pipeline",
        "type": "docker",
        "name": "docker-%s" % (arch),
        "platform": {
            "os": "linux",
            "arch": arch,
        },
        "steps": makeGenerate("") + [
            {
                "name": "build",
                "image": "owncloudci/golang:1.16",
                "pull": "always",
                "commands": [
                    "make -C ocis release-linux-docker",
                ],
            },
            {
                "name": "dryrun",
                "image": "plugins/docker:latest",
                "pull": "always",
                "settings": {
                    "dry_run": True,
                    "context": "ocis",
                    "tags": "linux-%s" % (arch),
                    "dockerfile": "ocis/docker/Dockerfile.linux.%s" % (arch),
                    "repo": ctx.repo.slug,
                    "build_args": build_args,
                },
                "when": {
                    "ref": {
                        "include": [
                            "refs/pull/**",
                        ],
                    },
                },
            },
            {
                "name": "docker",
                "image": "plugins/docker:latest",
                "pull": "always",
                "settings": {
                    "username": {
                        "from_secret": "docker_username",
                    },
                    "password": {
                        "from_secret": "docker_password",
                    },
                    "auto_tag": True,
                    "context": "ocis",
                    "auto_tag_suffix": "linux-%s" % (arch),
                    "dockerfile": "ocis/docker/Dockerfile.linux.%s" % (arch),
                    "repo": ctx.repo.slug,
                    "build_args": build_args,
                },
                "when": {
                    "ref": {
                        "exclude": [
                            "refs/pull/**",
                        ],
                    },
                },
            },
        ],
        "depends_on": getPipelineNames(testOcisModules(ctx) + testPipelines(ctx)),
        "trigger": {
            "ref": [
                "refs/heads/master",
                "refs/tags/v*",
                "refs/pull/**",
            ],
        },
        "volumes": [pipelineVolumeGo],
    }

def dockerEos(ctx):
    return {
        "kind": "pipeline",
        "type": "docker",
        "name": "docker-eos-ocis",
        "platform": {
            "os": "linux",
            "arch": "amd64",
        },
        "steps": makeGenerate("ocis") +
                 build() + [
            {
                "name": "dryrun-eos-ocis",
                "image": "plugins/docker:latest",
                "pull": "always",
                "settings": {
                    "dry_run": True,
                    "context": "ocis/docker/eos-ocis",
                    "tags": "linux-eos-ocis",
                    "dockerfile": "ocis/docker/eos-ocis/Dockerfile",
                    "repo": "owncloud/eos-ocis",
                },
                "when": {
                    "ref": {
                        "include": [
                            "refs/pull/**",
                        ],
                    },
                },
            },
            {
                "name": "docker-eos-ocis",
                "image": "plugins/docker:latest",
                "pull": "always",
                "settings": {
                    "username": {
                        "from_secret": "docker_username",
                    },
                    "password": {
                        "from_secret": "docker_password",
                    },
                    "auto_tag": True,
                    "context": "ocis/docker/eos-ocis",
                    "dockerfile": "ocis/docker/eos-ocis/Dockerfile",
                    "repo": "owncloud/eos-ocis",
                },
                "when": {
                    "ref": {
                        "exclude": [
                            "refs/pull/**",
                        ],
                    },
                },
            },
        ],
        "depends_on": getPipelineNames(testOcisModules(ctx) + testPipelines(ctx)),
        "trigger": {
            "ref": [
                "refs/heads/master",
                "refs/tags/v*",
                "refs/pull/**",
            ],
        },
        "volumes": [pipelineVolumeGo],
    }

def binaryReleases(ctx):
    pipelines = []
    for os in config["binaryReleases"]["os"]:
        pipelines.append(binaryRelease(ctx, os))

    return pipelines

def binaryRelease(ctx, name):
    # uploads binary to https://download.owncloud.com/ocis/ocis/testing/
    target = "/ocis/%s/testing" % (ctx.repo.name.replace("ocis-", ""))
    if ctx.build.event == "tag":
        # uploads binary to eg. https://download.owncloud.com/ocis/ocis/1.0.0-beta9/
        target = "/ocis/%s/%s" % (ctx.repo.name.replace("ocis-", ""), ctx.build.ref.replace("refs/tags/v", ""))

    settings = {
        "endpoint": {
            "from_secret": "s3_endpoint",
        },
        "access_key": {
            "from_secret": "aws_access_key_id",
        },
        "secret_key": {
            "from_secret": "aws_secret_access_key",
        },
        "bucket": {
            "from_secret": "s3_bucket",
        },
        "path_style": True,
        "strip_prefix": "ocis/dist/release/",
        "source": "ocis/dist/release/*",
        "target": target,
    }

    return {
        "kind": "pipeline",
        "type": "docker",
        "name": "binaries-%s" % (name),
        "platform": {
            "os": "linux",
            "arch": "amd64",
        },
        "steps": makeGenerate("") + [
            {
                "name": "build",
                "image": "owncloudci/golang:1.16",
                "pull": "always",
                "commands": [
                    "make -C ocis release-%s" % (name),
                ],
            },
            {
                "name": "finish",
                "image": "owncloudci/golang:1.16",
                "pull": "always",
                "commands": [
                    "make -C ocis release-finish",
                ],
                "when": {
                    "ref": [
                        "refs/heads/master",
                        "refs/tags/v*",
                    ],
                },
            },
            {
                "name": "upload",
                "image": "plugins/s3:1",
                "pull": "always",
                "settings": settings,
                "when": {
                    "ref": [
                        "refs/heads/master",
                        "refs/tags/v*",
                    ],
                },
            },
            {
                "name": "changelog",
                "image": "owncloudci/golang:1.16",
                "pull": "always",
                "commands": [
                    "make changelog CHANGELOG_VERSION=%s" % ctx.build.ref.replace("refs/tags/v", "").split("-")[0],
                ],
                "when": {
                    "ref": [
                        "refs/tags/v*",
                    ],
                },
            },
            {
                "name": "release",
                "image": "plugins/github-release:1",
                "pull": "always",
                "settings": {
                    "api_key": {
                        "from_secret": "github_token",
                    },
                    "files": [
                        "ocis/dist/release/*",
                    ],
                    "title": ctx.build.ref.replace("refs/tags/v", ""),
                    "note": "ocis/dist/CHANGELOG.md",
                    "overwrite": True,
                    "prerelease": len(ctx.build.ref.split("-")) > 1,
                },
                "when": {
                    "ref": [
                        "refs/tags/v*",
                    ],
                },
            },
        ],
        "depends_on": getPipelineNames(testOcisModules(ctx) + testPipelines(ctx)),
        "trigger": {
            "ref": [
                "refs/heads/master",
                "refs/tags/v*",
                "refs/pull/**",
            ],
        },
        "volumes": [pipelineVolumeGo],
    }

def releaseSubmodule(ctx):
    depends = []
    if len(ctx.build.ref.replace("refs/tags/", "").split("/")) == 2:
        depends = ["linting&unitTests-%s" % (ctx.build.ref.replace("refs/tags/", "").split("/")[0])]

    return {
        "kind": "pipeline",
        "type": "docker",
        "name": "release-%s" % (ctx.build.ref.replace("refs/tags/", "")),
        "platform": {
            "os": "linux",
            "arch": "amd64",
        },
        "steps": [
            {
                "name": "release-submodule",
                "image": "plugins/github-release:1",
                "pull": "always",
                "settings": {
                    "api_key": {
                        "from_secret": "github_token",
                    },
                    "files": [
                    ],
                    "title": ctx.build.ref.replace("refs/tags/", "").replace("/v", " "),
                    "note": "Release %s submodule" % (ctx.build.ref.replace("refs/tags/", "").replace("/v", " ")),
                    "overwrite": True,
                    "prerelease": len(ctx.build.ref.split("-")) > 1,
                },
                "when": {
                    "ref": [
                        "refs/tags/*/v*",
                    ],
                },
            },
        ],
        "depends_on": depends,
        "trigger": {
            "ref": [
                "refs/tags/*/v*",
            ],
        },
    }

def releaseDockerManifest(ctx):
    return {
        "kind": "pipeline",
        "type": "docker",
        "name": "manifest",
        "platform": {
            "os": "linux",
            "arch": "amd64",
        },
        "steps": [
            {
                "name": "execute",
                "image": "plugins/manifest:1",
                "pull": "always",
                "settings": {
                    "username": {
                        "from_secret": "docker_username",
                    },
                    "password": {
                        "from_secret": "docker_password",
                    },
                    "spec": "ocis/docker/manifest.tmpl",
                    "auto_tag": True,
                    "ignore_missing": True,
                },
            },
        ],
        "trigger": {
            "ref": [
                "refs/heads/master",
                "refs/tags/v*",
            ],
        },
    }

def changelog(ctx):
    return {
        "kind": "pipeline",
        "type": "docker",
        "name": "changelog",
        "platform": {
            "os": "linux",
            "arch": "amd64",
        },
        "steps": [
            {
                "name": "generate",
                "image": "owncloudci/golang:1.16",
                "pull": "always",
                "commands": [
                    "make -C ocis changelog",
                ],
            },
            {
                "name": "diff",
                "image": "owncloudci/alpine:latest",
                "pull": "always",
                "commands": [
                    "git diff",
                ],
            },
            {
                "name": "output",
                "image": "owncloudci/alpine:latest",
                "pull": "always",
                "commands": [
                    "cat CHANGELOG.md",
                ],
            },
            {
                "name": "publish",
                "image": "plugins/git-action:1",
                "pull": "always",
                "settings": {
                    "actions": [
                        "commit",
                        "push",
                    ],
                    "message": "Automated changelog update [skip ci]",
                    "branch": "master",
                    "author_email": "devops@owncloud.com",
                    "author_name": "ownClouders",
                    "netrc_machine": "github.com",
                    "netrc_username": {
                        "from_secret": "github_username",
                    },
                    "netrc_password": {
                        "from_secret": "github_token",
                    },
                },
                "when": {
                    "ref": {
                        "exclude": [
                            "refs/pull/**",
                        ],
                    },
                },
            },
        ],
        "trigger": {
            "ref": [
                "refs/heads/master",
                "refs/pull/**",
            ],
        },
    }

def releaseDockerReadme(ctx):
    return {
        "kind": "pipeline",
        "type": "docker",
        "name": "readme",
        "platform": {
            "os": "linux",
            "arch": "amd64",
        },
        "steps": [
            {
                "name": "execute",
                "image": "chko/docker-pushrm:1",
                "pull": "always",
                "environment": {
                    "DOCKER_USER": {
                        "from_secret": "docker_username",
                    },
                    "DOCKER_PASS": {
                        "from_secret": "docker_password",
                    },
                    "PUSHRM_TARGET": "owncloud/${DRONE_REPO_NAME}",
                    "PUSHRM_SHORT": "Docker images for %s" % (ctx.repo.name),
                    "PUSHRM_FILE": "README.md",
                },
            },
        ],
        "trigger": {
            "ref": [
                "refs/heads/master",
                "refs/tags/v*",
            ],
        },
    }

def docs(ctx):
    return {
        "kind": "pipeline",
        "type": "docker",
        "name": "docs",
        "platform": {
            "os": "linux",
            "arch": "amd64",
        },
        "steps": [
            {
                "name": "docs-generate",
                "image": "owncloudci/golang:1.16",
                "commands": ["make -C %s docs-generate" % (module) for module in config["modules"]],
            },
            {
                "name": "prepare",
                "image": "owncloudci/golang:1.16",
                "commands": [
                    "make -C docs docs-copy",
                ],
            },
            {
                "name": "test",
                "image": "owncloudci/golang:1.16",
                "commands": [
                    "make -C docs test",
                ],
            },
            {
                "name": "publish",
                "image": "plugins/gh-pages:1",
                "pull": "always",
                "settings": {
                    "username": {
                        "from_secret": "github_username",
                    },
                    "password": {
                        "from_secret": "github_token",
                    },
                    "pages_directory": "docs/hugo/content",
                    "target_branch": "docs",
                },
                "when": {
                    "ref": {
                        "exclude": [
                            "refs/pull/**",
                        ],
                    },
                },
            },
            {
                "name": "list and remove temporary files",
                "image": "owncloudci/alpine:latest",
                "commands": [
                    "tree docs/hugo/public",
                    "rm -rf docs/hugo",
                ],
            },
            {
                "name": "downstream",
                "image": "plugins/downstream:latest",
                "settings": {
                    "server": "https://drone.owncloud.com/",
                    "token": {
                        "from_secret": "drone_token",
                    },
                    "repositories": [
                        "owncloud/owncloud.github.io@source",
                    ],
                },
                "when": {
                    "ref": {
                        "exclude": [
                            "refs/pull/**",
                        ],
                    },
                },
            },
        ],
        "trigger": {
            "ref": [
                "refs/heads/master",
                "refs/pull/**",
            ],
        },
    }

def makeGenerate(module):
    if module == "":
        make = "make"
    else:
        make = "make -C %s" % (module)
    return [
        {
            "name": "generate nodejs",
            "image": "owncloudci/nodejs:14",
            "pull": "always",
            "commands": [
                "%s ci-node-generate" % (make),
            ],
            "volumes": [stepVolumeGo],
        },
        {
            "name": "generate go",
            "image": "owncloudci/golang:1.16",
            "pull": "always",
            "commands": [
                "%s ci-go-generate" % (make),
            ],
            "volumes": [stepVolumeGo],
        },
    ]

def notify(ctx):
    return {
        "kind": "pipeline",
        "type": "docker",
        "name": "chat-notifications",
        "clone": {
            "disable": True,
        },
        "steps": [
            {
                "name": "notify-rocketchat",
                "image": "plugins/slack:1",
                "pull": "always",
                "settings": {
                    "webhook": {
                        "from_secret": config["rocketchat"]["from_secret"],
                    },
                    "channel": config["rocketchat"]["channel"],
                },
            },
        ],
        "depends_on": [],
        "trigger": {
            "ref": [
                "refs/heads/master",
                "refs/heads/release*",
                "refs/tags/**",
            ],
            "status": [
                "failure",
            ],
        },
    }

def ocisServer(storage, accounts_hash_difficulty = 4, volumes = []):
    environment = {
        #'OCIS_LOG_LEVEL': 'debug',
        "OCIS_URL": "https://ocis-server:9200",
        "STORAGE_HOME_DRIVER": "%s" % (storage),
        "STORAGE_USERS_DRIVER": "%s" % (storage),
        "STORAGE_DRIVER_OCIS_ROOT": "/srv/app/tmp/ocis/storage/users",
        "STORAGE_DRIVER_LOCAL_ROOT": "/srv/app/tmp/ocis/local/root",
        "STORAGE_METADATA_ROOT": "/srv/app/tmp/ocis/metadata",
        "STORAGE_DRIVER_OWNCLOUD_DATADIR": "/srv/app/tmp/ocis/owncloud/data",
        "STORAGE_DRIVER_OWNCLOUD_REDIS_ADDR": "redis:6379" if storage == "owncloud" else "",
        "STORAGE_HOME_DATA_SERVER_URL": "http://ocis-server:9155/data",
        "STORAGE_USERS_DATA_SERVER_URL": "http://ocis-server:9158/data",
        "STORAGE_SHARING_USER_JSON_FILE": "/srv/app/tmp/ocis/shares.json",
        "PROXY_ENABLE_BASIC_AUTH": True,
        "WEB_UI_CONFIG": "/drone/src/tests/config/drone/ocis-config.json",
        "IDP_IDENTIFIER_REGISTRATION_CONF": "/drone/src/tests/config/drone/identifier-registration.yml",
        "OCIS_LOG_LEVEL": "error",
        "SETTINGS_DATA_PATH": "/srv/app/tmp/ocis/settings",
    }

    # Pass in "default" accounts_hash_difficulty to not set this environment variable.
    # That will allow OCIS to use whatever its built-in default is.
    # Otherwise pass in a value from 4 to about 11 or 12 (default 4, for making regular tests fast)
    # The high values cause lots of CPU to be used when hashing passwords, and really slow down the tests.
    if (accounts_hash_difficulty != "default"):
        environment["ACCOUNTS_HASH_DIFFICULTY"] = accounts_hash_difficulty

    return [
        {
            "name": "ocis-server",
            "image": "owncloudci/alpine:latest",
            "pull": "always",
            "detach": True,
            "environment": environment,
            "commands": [
                "apk add mailcap",  # install /etc/mime.types
                "ocis/bin/ocis server",
            ],
            "volumes": volumes,
        },
        {
            "name": "wait-for-ocis-server",
            "image": "owncloudci/wait-for:latest",
            "pull": "always",
            "commands": [
                "wait-for -it ocis-server:9200 -t 300",
            ],
        },
    ]

def cloneCoreRepos():
    return [
        {
            "name": "clone-core-repos",
            "image": "owncloudci/alpine:latest",
            "pull": "always",
            "commands": [
                "source /drone/src/.drone.env",
                "git clone -b master --depth=1 https://github.com/owncloud/testing.git /srv/app/tmp/testing",
                "git clone -b $CORE_BRANCH --single-branch --no-tags https://github.com/owncloud/core.git /srv/app/testrunner",
                "cd /srv/app/testrunner",
                "git checkout $CORE_COMMITID",
            ],
            "volumes": [stepVolumeOC10Tests],
        },
    ]

def redis():
    return [
        {
            "name": "redis",
            "image": "redis:6-alpine",
            "pull": "always",
        },
    ]

def redisForOCStorage(storage = "ocis"):
    if storage == "owncloud":
        return redis()
    else:
        return

def selenium():
    return [
        {
            "name": "selenium",
            "image": "selenium/standalone-chrome-debug:3.141.59",
            "pull": "always",
            "volumes": [{
                "name": "uploads",
                "path": "/uploads",
            }],
        },
    ]

def build():
    return [
        {
            "name": "build",
            "image": "owncloudci/golang:1.16",
            "pull": "always",
            "commands": [
                "make -C ocis build",
            ],
            "volumes": [stepVolumeGo],
        },
    ]

def example_deploys(ctx):
    latest_configs = [
        "cs3_users_ocis/latest.yml",
        "ocis_keycloak/latest.yml",
        "ocis_traefik/latest.yml",
        "ocis_wopi/latest.yml",
        "ocis_hello/latest.yml",
        "ocis_s3/latest.yml",
    ]
    released_configs = [
        "cs3_users_ocis/released.yml",
        "ocis_keycloak/released.yml",
        "ocis_traefik/released.yml",
        "ocis_wopi/released.yml",
    ]

    # if on master branch:
    configs = latest_configs
    rebuild = "false"

    if ctx.build.event == "tag":
        configs = released_configs
        rebuild = "false"

    if ctx.build.event == "cron":
        configs = latest_configs + released_configs
        rebuild = "true"

    deploys = []
    for config in configs:
        deploys.append(deploy(ctx, config, rebuild))

    return deploys

def deploy(ctx, config, rebuild):
    return {
        "kind": "pipeline",
        "type": "docker",
        "name": "deploy_%s" % (config),
        "platform": {
            "os": "linux",
            "arch": "amd64",
        },
        "steps": [
            {
                "name": "clone continuous deployment playbook",
                "image": "alpine/git:latest",
                "commands": [
                    "cd deployments/continuous-deployment-config",
                    "git clone https://github.com/owncloud-devops/continuous-deployment.git",
                ],
            },
            {
                "name": "deploy",
                "image": "owncloudci/drone-ansible:latest",
                "failure": "ignore",
                "environment": {
                    "CONTINUOUS_DEPLOY_SERVERS_CONFIG": "../%s" % (config),
                    "REBUILD": "%s" % (rebuild),
                    "HCLOUD_API_TOKEN": {
                        "from_secret": "hcloud_api_token",
                    },
                    "CLOUDFLARE_API_TOKEN": {
                        "from_secret": "cloudflare_api_token",
                    },
                },
                "settings": {
                    "playbook": "deployments/continuous-deployment-config/continuous-deployment/playbook-all.yml",
                    "galaxy": "deployments/continuous-deployment-config/continuous-deployment/requirements.yml",
                    "requirements": "deployments/continuous-deployment-config/continuous-deployment/py-requirements.txt",
                    "inventory": "localhost",
                    "private_key": {
                        "from_secret": "ssh_private_key",
                    },
                },
            },
        ],
        "trigger": {
            "ref": [
                "refs/heads/master",
                "refs/tags/v*",
            ],
        },
    }

def checkStarlark():
    return [{
        "kind": "pipeline",
        "type": "docker",
        "name": "check-starlark",
        "steps": [
            {
                "name": "format-check-starlark",
                "image": "owncloudci/bazel-buildifier",
                "pull": "always",
                "commands": [
                    "buildifier --mode=check .drone.star",
                ],
            },
            {
                "name": "show-diff",
                "image": "owncloudci/bazel-buildifier",
                "pull": "always",
                "commands": [
                    "buildifier --mode=fix .drone.star",
                    "git diff",
                ],
                "when": {
                    "status": [
                        "failure",
                    ],
                },
            },
        ],
        "depends_on": [],
        "trigger": {
            "ref": [
                "refs/pull/**",
            ],
        },
    }]

def genericCache(name, action, mounts, cache_key):
    rebuild = "false"
    restore = "false"
    if action == "rebuild":
        rebuild = "true"
        action = "rebuild"
    else:
        restore = "true"
        action = "restore"

    step = {
        "name": "%s_%s" % (action, name),
        "image": "meltwater/drone-cache:v1",
        "pull": "always",
        "environment": {
            "AWS_ACCESS_KEY_ID": {
                "from_secret": "cache_s3_access_key",
            },
            "AWS_SECRET_ACCESS_KEY": {
                "from_secret": "cache_s3_secret_key",
            },
        },
        "settings": {
            "endpoint": {
                "from_secret": "cache_s3_endpoint",
            },
            "bucket": "cache",
            "region": "us-east-1",  # not used at all, but fails if not given!
            "path_style": "true",
            "cache_key": cache_key,
            "rebuild": rebuild,
            "restore": restore,
            "mount": mounts,
        },
    }
    return step

def genericCachePurge(ctx, name, cache_key):
    return {
        "kind": "pipeline",
        "type": "docker",
        "name": "purge_%s" % (name),
        "platform": {
            "os": "linux",
            "arch": "amd64",
        },
        "steps": [
            {
                "name": "purge-cache",
                "image": "minio/mc:RELEASE.2021-03-23T05-46-11Z",
                "failure": "ignore",
                "environment": {
                    "MC_HOST_cache": {
                        "from_secret": "cache_s3_connection_url",
                    },
                },
                "commands": [
                    "mc rm --recursive --force cache/cache/%s/%s" % (ctx.repo.name, cache_key),
                ],
            },
        ],
        "trigger": {
            "ref": [
                "refs/heads/master",
                "refs/tags/v*",
                "refs/pull/**",
            ],
            "status": [
                "success",
                "failure",
            ],
        },
    }

def genericBuildArtifactCache(ctx, name, action, path):
    name = "%s_build_artifact_cache" % (name)
    cache_key = "%s/%s/%s" % (ctx.repo.slug, ctx.build.commit + "-${DRONE_BUILD_NUMBER}", name)
    if action == "rebuild" or action == "restore":
        return genericCache(name, action, [path], cache_key)
    if action == "purge":
        return genericCachePurge(ctx, name, cache_key)
    return []

def restoreBuildArtifactCache(ctx, name, path):
    return [genericBuildArtifactCache(ctx, name, "restore", path)]

def rebuildBuildArtifactCache(ctx, name, path):
    return [genericBuildArtifactCache(ctx, name, "rebuild", path)]

def purgeBuildArtifactCache(ctx, name):
    return genericBuildArtifactCache(ctx, name, "purge", [])

def pipelineSanityChecks(ctx, pipelines):
    """pipelineSanityChecks helps the CI developers to find errors before running it

    These sanity checks are only executed on when converting starlark to yaml.
    Error outputs are only visible when the conversion is done with the drone cli.

    Args:
      ctx: drone passes a context with information which the pipeline can be adapted to
      pipelines: pipelines to be checked, normally you should run this on the return value of main()

    Returns:
      none
    """

    # check if name length of pipeline and steps are exceeded.
    max_name_length = 50
    for pipeline in pipelines:
        pipeline_name = pipeline["name"]
        if len(pipeline_name) > max_name_length:
            print("Error: pipeline name %s is longer than 50 characters" % (pipeline_name))

        for step in pipeline["steps"]:
            step_name = step["name"]
            if len(step_name) > max_name_length:
                print("Error: step name %s in pipeline %s is longer than 50 characters" % (step_name, pipeline_name))

    # check for non existing depends_on
    possible_depends = []
    for pipeline in pipelines:
        possible_depends.append(pipeline["name"])

    for pipeline in pipelines:
        if "depends_on" in pipeline.keys():
            for depends in pipeline["depends_on"]:
                if not depends in possible_depends:
                    print("Error: depends_on %s for pipeline %s is not defined" % (depends, pipeline["name"]))

    # check for non declared volumes
    for pipeline in pipelines:
        pipeline_volumes = []
        if "volumes" in pipeline.keys():
            for volume in pipeline["volumes"]:
                pipeline_volumes.append(volume["name"])

        for step in pipeline["steps"]:
            if "volumes" in step.keys():
                for volume in step["volumes"]:
                    if not volume["name"] in pipeline_volumes:
                        print("Warning: volume %s for step %s is not defined in pipeline %s" % (volume["name"], step["name"], pipeline["name"]))

    # list used docker images
    print("")
    print("List of used docker images:")

    images = {}

    for pipeline in pipelines:
        for step in pipeline["steps"]:
            image = step["image"]
            if image in images.keys():
                images[image] = images[image] + 1
            else:
                images[image] = 1

    for image in images.keys():
        print(" %sx\t%s" % (images[image], image))
