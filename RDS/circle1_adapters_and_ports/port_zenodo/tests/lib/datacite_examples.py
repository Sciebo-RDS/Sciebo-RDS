import json


class Examples:
    @staticmethod
    def getDataCiteExample1():
        return {
            "id": "https://doi.org/10.5072/datacollector_datecollected_geolocationbox",
            "doi": "10.5072/datacollector_datecollected_geolocationbox",
            "types": {
                "resourceTypeGeneral": "Text",
                "resourceType": "report",
                "schemaOrg": "ScholarlyArticle",
                "citeproc": "report",
                "bibtex": "article",
                "ris": "RPRT"
            },
            "creators": [
                {
                    "nameType": "Personal",
                    "name": "Peach, A.",
                    "givenName": "A.",
                    "familyName": "Peach"
                }
            ],
            "titles": [
                {
                    "title": "Temperature and Humidity in School Classrooms, Ponhook Lake, N.S., 1961-1962",
                    "lang": "en"
                }
            ],
            "publisher": "National Research Council Canada",
            "container": {},
            "subjects": [
                {
                    "subject": "Temperature",
                    "subjectScheme": "LCCN",
                    "schemeUri": "http://lccn.loc.gov/sh85062931",
                    "lang": "en"
                },
                {
                    "subject": "Humidity",
                    "subjectScheme": "LCCN",
                    "schemeUri": "http://lccn.loc.gov/sh85133712",
                    "lang": "en"
                },
                {
                    "subject": "Classrooms",
                    "subjectScheme": "LCCN",
                    "schemeUri": "http://lccn.loc.gov/sh88003345",
                    "lang": "en"
                },
                {
                    "subject": "Ponhook Lake (N.S.)",
                    "lang": "en"
                }
            ],
            "contributors": [
                {
                    "nameType": "Personal",
                    "name": "Pomegranate, B.",
                    "givenName": "B.",
                    "familyName": "Pomegranate",
                    "contributorType": "DataCollector"
                }
            ],
            "dates": [
                {
                    "date": "1961-06-01/1962-10-12",
                    "dateType": "Collected"
                },
                {
                    "date": "1963",
                    "dateType": "Issued"
                }
            ],
            "publicationYear": "1963",
            "language": "en",
            "identifiers": [
                {
                    "identifierType": "DOI",
                    "identifier": "10.5072/datacollector_datecollected_geolocationbox"
                }
            ],
            "sizes": [
                "10 p."
            ],
            "formats": [],
            "rightsList": [],
            "descriptions": [
                {
                    "description": "The Division has been taking records of temperatures and humidities in groups of houses at various locations in Canada over the past several years. This survey has more recently been extended to include schools. Records obtained from classrooms in\\n      six schools in Ponhook Lake, Nova Scotia from June 1, 1961-October 12, 1962 are now reported.",
                    "descriptionType": "Abstract",
                    "lang": "en"
                }
            ],
            "geoLocations": [
                {
                    "geoLocationBox": {
                        "westBoundLongitude": -64.2,
                        "eastBoundLongitude": -63.8,
                        "southBoundLatitude": 44.7167,
                        "northBoundLatitude": 44.9667
                    },
                    "geoLocationPlace": "Ponhook Lake, Nova Scotia"
                }
            ],
            "fundingReferences": [],
            "relatedIdentifiers": [],
            "schemaVersion": "http://datacite.org/schema/kernel-4",
            "agency": "DataCite",
            "state": "findable"
        }

    @classmethod
    def getZenodoExample1(cls):
        zenodo = json.loads("""{
  "files": [
    {
      "links": {
        "self": "https://zenodo.org/api/files/deff9397-dece-4206-9964-963beb518c33/covid19.ttl"
      }, 
      "checksum": "md5:4abfc39f28bbca394b9201708ae27b4b", 
      "bucket": "deff9397-dece-4206-9964-963beb518c33", 
      "key": "covid19.ttl", 
      "type": "ttl", 
      "size": 9190269
    }
  ], 
  "owners": [
    28686
  ], 
  "doi": "10.5281/zenodo.3763271", 
  "stats": {
    "version_unique_downloads": 28.0, 
    "unique_views": 0.0, 
    "views": 0.0, 
    "version_views": 265.0, 
    "unique_downloads": 0.0, 
    "version_unique_views": 205.0, 
    "volume": 0.0, 
    "version_downloads": 32.0, 
    "downloads": 0.0, 
    "version_volume": 286418256.0
  }, 
  "links": {
    "doi": "https://doi.org/10.5281/zenodo.3763271", 
    "conceptdoi": "https://doi.org/10.5281/zenodo.3757279", 
    "bucket": "https://zenodo.org/api/files/deff9397-dece-4206-9964-963beb518c33", 
    "conceptbadge": "https://zenodo.org/badge/doi/10.5281/zenodo.3757279.svg", 
    "html": "https://zenodo.org/record/3763271", 
    "latest_html": "https://zenodo.org/record/3763271", 
    "badge": "https://zenodo.org/badge/doi/10.5281/zenodo.3763271.svg", 
    "latest": "https://zenodo.org/api/records/3763271"
  }, 
  "conceptdoi": "10.5281/zenodo.3757279", 
  "created": "2020-04-23T12:06:43.947322+00:00", 
  "updated": "2020-04-23T12:17:34.033949+00:00", 
  "conceptrecid": "3757279", 
  "revision": 3, 
  "id": 3763271, 
  "metadata": {
    "access_right_category": "success", 
    "doi": "10.5281/zenodo.3763271", 
    "description": "<p>Linked COVID-19 Data derived from</p>\\n\\n<p><strong>Johns Hopkins University</strong></p>\\n\\n<p>and</p>\\n\\n<p><strong>European Centre for Disease Prevention and Control</strong></p>\\n\\n<p>using the COVID-19 Ontology</p>\\n\\n<p><a href=\\"https://doi.org/10.5281/zenodo.3757828\\">10.5281/zenodo.3757828</a></p>\\n\\n<p>developed for the Linked COVID-19 Data&nbsp;Dashboard:&nbsp;<a href=\\"http://covid19data.link/\\">http://covid19data.link</a></p>\\n\\n<p>&nbsp;</p>\\n\\n<p>This files include data for</p>\\n\\n<ul>\\n\\t<li>covid19.ttl - COVID-19 data collected by the JHU and ECDC</li>\\n</ul>\\n\\n<p>This RDF files are based on</p>\\n\\n<ul>\\n\\t<li>https://pomber.github.io/covid19/timeseries.json</li>\\n\\t<li>https://opendata.ecdc.europa.eu/covid19/casedistribution/json/</li>\\n</ul>\\n\\n<p>&nbsp;</p>", 
    "license": {
      "id": "CC-BY-4.0"
    }, 
    "title": "Linked COVID-19 Data: Johns Hopkins University (JHU) and European Centre for Disease Prevention and Control (ECDC)", 
    "relations": {
      "version": [
        {
          "count": 5, 
          "index": 4, 
          "parent": {
            "pid_type": "recid", 
            "pid_value": "3757279"
          }, 
          "is_last": true, 
          "last_child": {
            "pid_type": "recid", 
            "pid_value": "3763271"
          }
        }
      ]
    }, 
    "communities": [
      {
        "id": "covid-19"
      }, 
      {
        "id": "researchsquirrelengineers"
      }, 
      {
        "id": "zenodo"
      }
    ], 
    "subjects": [
      {
        "term": "COVID-19", 
        "scheme": "url", 
        "identifier": "http://www.wikidata.org/entity/Q84263196"
      }, 
      {
        "term": "2019\\u201320 COVID-19 pandemic", 
        "scheme": "url", 
        "identifier": "http://www.wikidata.org/entity/Q81068910"
      }, 
      {
        "term": "Linked COVID-19 Data", 
        "scheme": "url", 
        "identifier": "http://www.wikidata.org/entity/Q91205721"
      }
    ], 
    "keywords": [
      "Linked Data", 
      "COVID-19", 
      "Johns Hopkins University", 
      "European Centre for Disease Prevention and Control"
    ], 
    "publication_date": "2020-04-23", 
    "creators": [
      {
        "orcid": "0000-0002-3246-3531", 
        "affiliation": "Research Squirrel Engineers", 
        "name": "Florian Thiery"
      }
    ], 
    "access_right": "open", 
    "resource_type": {
      "type": "dataset", 
      "title": "Dataset"
    }, 
    "related_identifiers": [
      {
        "scheme": "doi", 
        "identifier": "10.5281/zenodo.3757279", 
        "relation": "isVersionOf"
      }
    ]
  }
}""")

        # taken from https://api.datacite.org/dois/10.5281/zenodo.3763274
        datacite = json.loads("""{"data":{"id":"10.5281/zenodo.3763271","type":"dois","attributes":{"doi":"10.5281/zenodo.3763271","prefix":"10.5281","suffix":"zenodo.3763271","identifiers":[{"identifier":"https://doi.org/10.5281/zenodo.3763271","identifierType":"DOI"},{"identifier":"https://zenodo.org/record/3763271","identifierType":"URL"}],"creators":[{"name":"Thiery, Florian","nameType":"Personal","givenName":"Florian","familyName":"Thiery","affiliation":["Research Squirrel Engineers"],"nameIdentifiers":[{"schemeUri":"https://orcid.org","nameIdentifier":"https://orcid.org/0000-0002-3246-3531","nameIdentifierScheme":"ORCID"}]}],"titles":[{"title":"Linked COVID-19 Data: Johns Hopkins University (JHU) and European Centre for Disease Prevention and Control (ECDC)"}],"publisher":"Zenodo","container":{"type":"DataRepository","identifier":"https://zenodo.org/communities/covid-19","identifierType":"URL"},"publicationYear":2020,"subjects":[{"subject":"Linked Data"},{"subject":"COVID-19"},{"subject":"Johns Hopkins University"},{"subject":"European Centre for Disease Prevention and Control"},{"subject":"http://www.wikidata.org/entity/Q84263196","subjectScheme":"url"},{"subject":"http://www.wikidata.org/entity/Q81068910","subjectScheme":"url"},{"subject":"http://www.wikidata.org/entity/Q91205721","subjectScheme":"url"}],"contributors":[],"dates":[{"date":"2020-04-23","dateType":"Issued"}],"language":null,"types":{"ris":"DATA","bibtex":"misc","citeproc":"dataset","schemaOrg":"Dataset","resourceTypeGeneral":"Dataset"},"relatedIdentifiers":[{"relationType":"IsVersionOf","relatedIdentifier":"10.5281/zenodo.3757279","relatedIdentifierType":"DOI"},{"relationType":"IsPartOf","relatedIdentifier":"https://zenodo.org/communities/covid-19","relatedIdentifierType":"URL"},{"relationType":"IsPartOf","relatedIdentifier":"https://zenodo.org/communities/researchsquirrelengineers","relatedIdentifierType":"URL"},{"relationType":"IsPartOf","relatedIdentifier":"https://zenodo.org/communities/zenodo","relatedIdentifierType":"URL"}],"sizes":[],"formats":[],"version":null,"rightsList":[{"rights":"Creative Commons Attribution 4.0 International","rightsUri":"http://creativecommons.org/licenses/by/4.0/legalcode"},{"rights":"Open Access","rightsUri":"info:eu-repo/semantics/openAccess"}],"descriptions":[{"description":"Linked COVID-19 Data derived from <strong>Johns Hopkins University</strong> and <strong>European Centre for Disease Prevention and Control</strong> using the COVID-19 Ontology 10.5281/zenodo.3757828 developed for the Linked COVID-19 Data Dashboard: http://covid19data.link This files include data for covid19.ttl - COVID-19 data collected by the JHU and ECDC This RDF files are based on https://pomber.github.io/covid19/timeseries.json https://opendata.ecdc.europa.eu/covid19/casedistribution/json/","descriptionType":"Abstract"}],"geoLocations":[],"fundingReferences":[],"xml":"PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0idXRmLTgiPz4KPHJlc291cmNlIHhtbG5zOnhzaT0iaHR0cDovL3d3dy53My5vcmcvMjAwMS9YTUxTY2hlbWEtaW5zdGFuY2UiIHhtbG5zPSJodHRwOi8vZGF0YWNpdGUub3JnL3NjaGVtYS9rZXJuZWwtNCIgeHNpOnNjaGVtYUxvY2F0aW9uPSJodHRwOi8vZGF0YWNpdGUub3JnL3NjaGVtYS9rZXJuZWwtNCBodHRwOi8vc2NoZW1hLmRhdGFjaXRlLm9yZy9tZXRhL2tlcm5lbC00LjEvbWV0YWRhdGEueHNkIj4KICA8aWRlbnRpZmllciBpZGVudGlmaWVyVHlwZT0iRE9JIj4xMC41MjgxL1pFTk9ETy4zNzYzMjcxPC9pZGVudGlmaWVyPgogIDxjcmVhdG9ycz4KICAgIDxjcmVhdG9yPgogICAgICA8Y3JlYXRvck5hbWU+RmxvcmlhbiBUaGllcnk8L2NyZWF0b3JOYW1lPgogICAgICA8bmFtZUlkZW50aWZpZXIgbmFtZUlkZW50aWZpZXJTY2hlbWU9Ik9SQ0lEIiBzY2hlbWVVUkk9Imh0dHA6Ly9vcmNpZC5vcmcvIj4wMDAwLTAwMDItMzI0Ni0zNTMxPC9uYW1lSWRlbnRpZmllcj4KICAgICAgPGFmZmlsaWF0aW9uPlJlc2VhcmNoIFNxdWlycmVsIEVuZ2luZWVyczwvYWZmaWxpYXRpb24+CiAgICA8L2NyZWF0b3I+CiAgPC9jcmVhdG9ycz4KICA8dGl0bGVzPgogICAgPHRpdGxlPkxpbmtlZCBDT1ZJRC0xOSBEYXRhOiBKb2hucyBIb3BraW5zIFVuaXZlcnNpdHkgKEpIVSkgYW5kIEV1cm9wZWFuIENlbnRyZSBmb3IgRGlzZWFzZSBQcmV2ZW50aW9uIGFuZCBDb250cm9sIChFQ0RDKTwvdGl0bGU+CiAgPC90aXRsZXM+CiAgPHB1Ymxpc2hlcj5aZW5vZG88L3B1Ymxpc2hlcj4KICA8cHVibGljYXRpb25ZZWFyPjIwMjA8L3B1YmxpY2F0aW9uWWVhcj4KICA8c3ViamVjdHM+CiAgICA8c3ViamVjdD5MaW5rZWQgRGF0YTwvc3ViamVjdD4KICAgIDxzdWJqZWN0PkNPVklELTE5PC9zdWJqZWN0PgogICAgPHN1YmplY3Q+Sm9obnMgSG9wa2lucyBVbml2ZXJzaXR5PC9zdWJqZWN0PgogICAgPHN1YmplY3Q+RXVyb3BlYW4gQ2VudHJlIGZvciBEaXNlYXNlIFByZXZlbnRpb24gYW5kIENvbnRyb2w8L3N1YmplY3Q+CiAgICA8c3ViamVjdCBzdWJqZWN0U2NoZW1lPSJ1cmwiPmh0dHA6Ly93d3cud2lraWRhdGEub3JnL2VudGl0eS9RODQyNjMxOTY8L3N1YmplY3Q+CiAgICA8c3ViamVjdCBzdWJqZWN0U2NoZW1lPSJ1cmwiPmh0dHA6Ly93d3cud2lraWRhdGEub3JnL2VudGl0eS9RODEwNjg5MTA8L3N1YmplY3Q+CiAgICA8c3ViamVjdCBzdWJqZWN0U2NoZW1lPSJ1cmwiPmh0dHA6Ly93d3cud2lraWRhdGEub3JnL2VudGl0eS9ROTEyMDU3MjE8L3N1YmplY3Q+CiAgPC9zdWJqZWN0cz4KICA8ZGF0ZXM+CiAgICA8ZGF0ZSBkYXRlVHlwZT0iSXNzdWVkIj4yMDIwLTA0LTIzPC9kYXRlPgogIDwvZGF0ZXM+CiAgPHJlc291cmNlVHlwZSByZXNvdXJjZVR5cGVHZW5lcmFsPSJEYXRhc2V0Ii8+CiAgPGFsdGVybmF0ZUlkZW50aWZpZXJzPgogICAgPGFsdGVybmF0ZUlkZW50aWZpZXIgYWx0ZXJuYXRlSWRlbnRpZmllclR5cGU9InVybCI+aHR0cHM6Ly96ZW5vZG8ub3JnL3JlY29yZC8zNzYzMjcxPC9hbHRlcm5hdGVJZGVudGlmaWVyPgogIDwvYWx0ZXJuYXRlSWRlbnRpZmllcnM+CiAgPHJlbGF0ZWRJZGVudGlmaWVycz4KICAgIDxyZWxhdGVkSWRlbnRpZmllciByZWxhdGVkSWRlbnRpZmllclR5cGU9IkRPSSIgcmVsYXRpb25UeXBlPSJJc1ZlcnNpb25PZiI+MTAuNTI4MS96ZW5vZG8uMzc1NzI3OTwvcmVsYXRlZElkZW50aWZpZXI+CiAgICA8cmVsYXRlZElkZW50aWZpZXIgcmVsYXRlZElkZW50aWZpZXJUeXBlPSJVUkwiIHJlbGF0aW9uVHlwZT0iSXNQYXJ0T2YiPmh0dHBzOi8vemVub2RvLm9yZy9jb21tdW5pdGllcy9jb3ZpZC0xOTwvcmVsYXRlZElkZW50aWZpZXI+CiAgICA8cmVsYXRlZElkZW50aWZpZXIgcmVsYXRlZElkZW50aWZpZXJUeXBlPSJVUkwiIHJlbGF0aW9uVHlwZT0iSXNQYXJ0T2YiPmh0dHBzOi8vemVub2RvLm9yZy9jb21tdW5pdGllcy9yZXNlYXJjaHNxdWlycmVsZW5naW5lZXJzPC9yZWxhdGVkSWRlbnRpZmllcj4KICAgIDxyZWxhdGVkSWRlbnRpZmllciByZWxhdGVkSWRlbnRpZmllclR5cGU9IlVSTCIgcmVsYXRpb25UeXBlPSJJc1BhcnRPZiI+aHR0cHM6Ly96ZW5vZG8ub3JnL2NvbW11bml0aWVzL3plbm9kbzwvcmVsYXRlZElkZW50aWZpZXI+CiAgPC9yZWxhdGVkSWRlbnRpZmllcnM+CiAgPHJpZ2h0c0xpc3Q+CiAgICA8cmlnaHRzIHJpZ2h0c1VSST0iaHR0cDovL2NyZWF0aXZlY29tbW9ucy5vcmcvbGljZW5zZXMvYnkvNC4wL2xlZ2FsY29kZSI+Q3JlYXRpdmUgQ29tbW9ucyBBdHRyaWJ1dGlvbiA0LjAgSW50ZXJuYXRpb25hbDwvcmlnaHRzPgogICAgPHJpZ2h0cyByaWdodHNVUkk9ImluZm86ZXUtcmVwby9zZW1hbnRpY3Mvb3BlbkFjY2VzcyI+T3BlbiBBY2Nlc3M8L3JpZ2h0cz4KICA8L3JpZ2h0c0xpc3Q+CiAgPGRlc2NyaXB0aW9ucz4KICAgIDxkZXNjcmlwdGlvbiBkZXNjcmlwdGlvblR5cGU9IkFic3RyYWN0Ij4mbHQ7cCZndDtMaW5rZWQgQ09WSUQtMTkgRGF0YSBkZXJpdmVkIGZyb20mbHQ7L3AmZ3Q7CgombHQ7cCZndDsmbHQ7c3Ryb25nJmd0O0pvaG5zIEhvcGtpbnMgVW5pdmVyc2l0eSZsdDsvc3Ryb25nJmd0OyZsdDsvcCZndDsKCiZsdDtwJmd0O2FuZCZsdDsvcCZndDsKCiZsdDtwJmd0OyZsdDtzdHJvbmcmZ3Q7RXVyb3BlYW4gQ2VudHJlIGZvciBEaXNlYXNlIFByZXZlbnRpb24gYW5kIENvbnRyb2wmbHQ7L3N0cm9uZyZndDsmbHQ7L3AmZ3Q7CgombHQ7cCZndDt1c2luZyB0aGUgQ09WSUQtMTkgT250b2xvZ3kmbHQ7L3AmZ3Q7CgombHQ7cCZndDsmbHQ7YSBocmVmPSJodHRwczovL2RvaS5vcmcvMTAuNTI4MS96ZW5vZG8uMzc1NzgyOCImZ3Q7MTAuNTI4MS96ZW5vZG8uMzc1NzgyOCZsdDsvYSZndDsmbHQ7L3AmZ3Q7CgombHQ7cCZndDtkZXZlbG9wZWQgZm9yIHRoZSBMaW5rZWQgQ09WSUQtMTkgRGF0YSZhbXA7bmJzcDtEYXNoYm9hcmQ6JmFtcDtuYnNwOyZsdDthIGhyZWY9Imh0dHA6Ly9jb3ZpZDE5ZGF0YS5saW5rLyImZ3Q7aHR0cDovL2NvdmlkMTlkYXRhLmxpbmsmbHQ7L2EmZ3Q7Jmx0Oy9wJmd0OwoKJmx0O3AmZ3Q7JmFtcDtuYnNwOyZsdDsvcCZndDsKCiZsdDtwJmd0O1RoaXMgZmlsZXMgaW5jbHVkZSBkYXRhIGZvciZsdDsvcCZndDsKCiZsdDt1bCZndDsKCSZsdDtsaSZndDtjb3ZpZDE5LnR0bCAtIENPVklELTE5IGRhdGEgY29sbGVjdGVkIGJ5IHRoZSBKSFUgYW5kIEVDREMmbHQ7L2xpJmd0OwombHQ7L3VsJmd0OwoKJmx0O3AmZ3Q7VGhpcyBSREYgZmlsZXMgYXJlIGJhc2VkIG9uJmx0Oy9wJmd0OwoKJmx0O3VsJmd0OwoJJmx0O2xpJmd0O2h0dHBzOi8vcG9tYmVyLmdpdGh1Yi5pby9jb3ZpZDE5L3RpbWVzZXJpZXMuanNvbiZsdDsvbGkmZ3Q7CgkmbHQ7bGkmZ3Q7aHR0cHM6Ly9vcGVuZGF0YS5lY2RjLmV1cm9wYS5ldS9jb3ZpZDE5L2Nhc2VkaXN0cmlidXRpb24vanNvbi8mbHQ7L2xpJmd0OwombHQ7L3VsJmd0OwoKJmx0O3AmZ3Q7JmFtcDtuYnNwOyZsdDsvcCZndDs8L2Rlc2NyaXB0aW9uPgogIDwvZGVzY3JpcHRpb25zPgo8L3Jlc291cmNlPg==","url":"https://zenodo.org/record/3763271","contentUrl":null,"metadataVersion":1,"schemaVersion":null,"source":"mds","isActive":true,"state":"findable","reason":null,"viewCount":0,"viewsOverTime":[],"downloadCount":0,"downloadsOverTime":[],"referenceCount":0,"citationCount":0,"citationsOverTime":[],"partCount":0,"partOfCount":0,"versionCount":0,"versionOfCount":0,"created":"2020-04-23T12:06:50.000Z","registered":"2020-04-23T12:06:51.000Z","published":"2020","updated":"2020-04-23T12:17:36.000Z"},"relationships":{"client":{"data":{"id":"cern.zenodo","type":"clients"}},"media":{"data":{"id":"10.5281/zenodo.3763271","type":"media"}},"references":{"data":[]},"citations":{"data":[]},"parts":{"data":[]},"partOf":{"data":[]},"versions":{"data":[]},"versionOf":{"data":[]}}}}""")
        return zenodo["metadata"], datacite["data"]["attributes"]
