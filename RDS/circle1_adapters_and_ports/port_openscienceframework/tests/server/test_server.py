import unittest
import sys
import os, json
from pactman import Consumer, Provider

# from .example import node_json, _build_node

api_key = os.getenv("OPENSCIENCEFRAMEWORK_API_KEY", default=None)

node_json = """
{
  "data": {
    "relationships": {
      "files": {
        "links": {
          "related": {
            "href": "https://api.osf.io/v2/nodes/f3szh/files/",
            "meta": {}
          }
        }
      },
      "view_only_links": {
        "links": {
          "related": {
            "href": "https://api.osf.io/v2/nodes/f3szh/view_only_links/",
            "meta": {}
          }
        }
      },
      "citation": {
        "links": {
          "related": {
            "href": "https://api.osf.io/v2/nodes/f3szh/citation/",
            "meta": {}
          }
        }
      },
      "license": {
        "links": {
          "related": {
            "href": "https://api.osf.io/v2/licenses/563c1ffbda3e240129e72c03/",
            "meta": {}
          }
        }
      },
      "contributors": {
        "links": {
          "related": {
            "href": "https://api.osf.io/v2/nodes/f3szh/contributors/",
            "meta": {}
          }
        }
      },
      "forks": {
        "links": {
          "related": {
            "href": "https://api.osf.io/v2/nodes/f3szh/forks/",
            "meta": {}
          }
        }
      },
      "root": {
        "links": {
          "related": {
            "href": "https://api.osf.io/v2/nodes/f3szh/",
            "meta": {}
          }
        }
      },
      "identifiers": {
        "links": {
          "related": {
            "href": "https://api.osf.io/v2/nodes/f3szh/identifiers/",
            "meta": {}
          }
        }
      },
      "comments": {
        "links": {
          "related": {
            "href": "https://api.osf.io/v2/nodes/f3szh/comments/?filter%5Btarget%5D=f3szh",
            "meta": {}
          }
        }
      },
      "registrations": {
        "links": {
          "related": {
            "href": "https://api.osf.io/v2/nodes/f3szh/registrations/",
            "meta": {}
          }
        }
      },
      "logs": {
        "links": {
          "related": {
            "href": "https://api.osf.io/v2/nodes/f3szh/logs/",
            "meta": {}
          }
        }
      },
      "node_links": {
        "links": {
          "related": {
            "href": "https://api.osf.io/v2/nodes/f3szh/node_links/",
            "meta": {}
          }
        }
      },
      "linked_nodes": {
        "links": {
          "self": {
            "href": "https://api.osf.io/v2/nodes/f3szh/relationships/linked_nodes/",
            "meta": {}
          },
          "related": {
            "href": "https://api.osf.io/v2/nodes/f3szh/linked_nodes/",
            "meta": {}
          }
        }
      },
      "wikis": {
        "links": {
          "related": {
            "href": "https://api.osf.io/v2/nodes/f3szh/wikis/",
            "meta": {}
          }
        }
      },
      "affiliated_institutions": {
        "links": {
          "self": {
            "href": "https://api.osf.io/v2/nodes/f3szh/relationships/institutions/",
            "meta": {}
          },
          "related": {
            "href": "https://api.osf.io/v2/nodes/f3szh/institutions/",
            "meta": {}
          }
        }
      },
      "children": {
        "links": {
          "related": {
            "href": "https://api.osf.io/v2/nodes/f3szh/children/",
            "meta": {}
          }
        }
      },
      "preprints": {
        "links": {
          "related": {
            "href": "https://api.osf.io/v2/nodes/f3szh/preprints/",
            "meta": {}
          }
        }
      },
      "draft_registrations": {
        "links": {
          "related": {
            "href": "https://api.osf.io/v2/nodes/f3szh/draft_registrations/",
            "meta": {}
          }
        }
      }
    },
    "links": {
      "self": "https://api.osf.io/v2/nodes/f3szh/",
      "html": "https://osf.io/f3szh/"
    },
    "attributes": {
      "category": "project",
      "fork": false,
      "preprint": true,
      "description": "this is a test for preprint citations",
      "current_user_permissions": [
        "read"
      ],
      "date_modified": "2017-03-17T16:11:35.721000",
      "title": "Preprint Citations Test",
      "collection": false,
      "registration": false,
      "date_created": "2017-03-17T16:09:14.864000",
      "current_user_can_comment": false,
      "node_license": {
        "copyright_holders": [],
        "year": "2017"
      },
      "public": true,
      "tags": [
        "qatest"
      ]
    },
    "type": "{type}",
    "id": "f3szh"
  }
}
"""

def _build_node(type_):
    node = json.loads(node_json)
    node["data"]["type"] = type_
    return node

project_node = _build_node("nodes")

def create_app():
    from src import bootstrap

    # creates a test client
    app = bootstrap(use_default_error=True, address="http://localhost:3000").app
    # propagate the exceptions to the test client
    app.config.update({"TESTING": True})

    return app


pact = Consumer("PortOSF").has_pact_with(Provider("OSF"), port=3000)

unittest.TestCase.maxDiff = None


class TestPortOSF(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_metric(self):
        self.assertTrue(True)

    @unittest.skip("not implemented")
    def test_project_index(self):
        pass

    @unittest.skip("not implemented")
    def test_project_get(self):
        pass

    @unittest.skip("not implemented")
    def test_project_post(self):
        pass

    @unittest.skip("not implemented")
    def test_project_put(self):
        pass

    @unittest.skip("not implemented")
    def test_project_patch(self):
        pass

    @unittest.skip("not implemented")
    def test_project_delete(self):
        pass

    @unittest.skip("not implemented")
    def test_files_index(self):
        pass

    @unittest.skip("not implemented")
    def test_files_get(self):
        pass

    @unittest.skip("not implemented")
    def test_files_post(self):
        pass

    @unittest.skip("not implemented")
    def test_files_delete(self):
        pass

    def test_metadata_update_jsonld_complete(self):
        return
        import json

        metadata = {
            "https://schema.org/creator": [
                {
                    "https://schema.org/affiliation": "Zenodo",
                    "https://schema.org/name": "Doe, John",
                }
            ],
            "https://schema.org/description": "This is my first upload",
            "https://schema.org/identifier": 1234,
            "https://schema.org/publicAccess": True,
            "https://schema.org/name": "My first upload",
            "https://www.research-data-services.org/jsonld/zenodocategory": "poster",
            "https://www.research-data-services.org/jsonld/doi": "10.5072/zenodo.1234",
        }

        projectId = 5

        expected_body = project_node

        pact.given("access token is valid").upon_receiving(
            "the corresponding user has an updated deposit with"
        ).with_request(
            "PUT", f"/api/deposit/depositions/{projectId}"
        ).will_respond_with(
            200, body=expected_body
        )

        expected_body["metadata"] = metadata

        with pact:
            data = {"metadata": metadata, "apiKey": "ASD123GANZSICHA"}
            result = self.client.patch(f"/metadata/project/{projectId}", json=data)
            self.assertEqual(result.status_code, 200)
            self.assertEqual(result.json, expected_body["metadata"])


if __name__ == "__main__":
    unittest.main()
