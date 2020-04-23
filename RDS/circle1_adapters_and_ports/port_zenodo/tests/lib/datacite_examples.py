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
        "self": "https://zenodo.org/api/files/28fc146f-3387-4b38-bd9c-0aebba6cad17/covid19_rki1.ttl"
      }, 
      "checksum": "md5:bf6241b902c814f2f9ccb974eac8c12d", 
      "bucket": "28fc146f-3387-4b38-bd9c-0aebba6cad17", 
      "key": "covid19_rki1.ttl", 
      "type": "ttl", 
      "size": 20965550
    }, 
    {
      "links": {
        "self": "https://zenodo.org/api/files/28fc146f-3387-4b38-bd9c-0aebba6cad17/covid19_rki2.ttl"
      }, 
      "checksum": "md5:f131aa645dbca9a6e04fbac9387532ee", 
      "bucket": "28fc146f-3387-4b38-bd9c-0aebba6cad17", 
      "key": "covid19_rki2.ttl", 
      "type": "ttl", 
      "size": 20757838
    }, 
    {
      "links": {
        "self": "https://zenodo.org/api/files/28fc146f-3387-4b38-bd9c-0aebba6cad17/covid19_rki_cum.ttl"
      }, 
      "checksum": "md5:7837f23dd05e1415e6af8186ffa39182", 
      "bucket": "28fc146f-3387-4b38-bd9c-0aebba6cad17", 
      "key": "covid19_rki_cum.ttl", 
      "type": "ttl", 
      "size": 32644
    }, 
    {
      "links": {
        "self": "https://zenodo.org/api/files/28fc146f-3387-4b38-bd9c-0aebba6cad17/covid19_rki_fs.ttl"
      }, 
      "checksum": "md5:9ee7b71649d8922726711d2694457afe", 
      "bucket": "28fc146f-3387-4b38-bd9c-0aebba6cad17", 
      "key": "covid19_rki_fs.ttl", 
      "type": "ttl", 
      "size": 593739
    }
  ], 
  "owners": [
    28686
  ], 
  "doi": "10.5281/zenodo.3763274", 
  "stats": {
    "version_unique_downloads": 40.0, 
    "unique_views": 0.0, 
    "views": 0.0, 
    "version_views": 310.0, 
    "unique_downloads": 0.0, 
    "version_unique_views": 248.0, 
    "volume": 0.0, 
    "version_downloads": 86.0, 
    "downloads": 0.0, 
    "version_volume": 1138714520.0
  }, 
  "links": {
    "doi": "https://doi.org/10.5281/zenodo.3763274", 
    "conceptdoi": "https://doi.org/10.5281/zenodo.3757283", 
    "bucket": "https://zenodo.org/api/files/28fc146f-3387-4b38-bd9c-0aebba6cad17", 
    "conceptbadge": "https://zenodo.org/badge/doi/10.5281/zenodo.3757283.svg", 
    "html": "https://zenodo.org/record/3763274", 
    "latest_html": "https://zenodo.org/record/3763274", 
    "badge": "https://zenodo.org/badge/doi/10.5281/zenodo.3763274.svg", 
    "latest": "https://zenodo.org/api/records/3763274"
  }, 
  "conceptdoi": "10.5281/zenodo.3757283", 
  "created": "2020-04-23T12:14:08.361108+00:00", 
  "updated": "2020-04-23T12:14:11.677381+00:00", 
  "conceptrecid": "3757283", 
  "revision": 1, 
  "id": 3763274, 
  "metadata": {
    "access_right_category": "success", 
    "doi": "10.5281/zenodo.3763274", 
    "description": "<p>Linked COVID-19 Data derived from</p>\\n\\n<p><strong>Robert Koch Institute</strong></p>\\n\\n<p>using the COVID-19 Ontology</p>\\n\\n<p><a href=\\"https://doi.org/10.5281/zenodo.3757828\\">10.5281/zenodo.3757828</a></p>\\n\\n<p>developed for the Linked COVID-19 Data&nbsp;Dashboard:&nbsp;<a href=\\"http://covid19data.link/\\">http://covid19data.link</a></p>\\n\\n<p>&nbsp;</p>\\n\\n<p>This files include data for</p>\\n\\n<ul>\\n\\t<li>covid19_rki*.ttl - single COVID-19 cases per day, collected by the RKI\\n\\t<ul>\\n\\t\\t<li>https://www.arcgis.com/home/item.html?id=dd4580c810204019a7b8eb3e0b329dd6</li>\\n\\t\\t<li>&quot;confirmed&quot; is calcaulated by the column &quot;Refdatum&quot;</li>\\n\\t</ul>\\n\\t</li>\\n\\t<li>covid19_rki_cum.ttl - COVID-19 cases per day for Germany, collected by the RKI</li>\\n\\t<li>covid19_rki_fs.ttl - COVID-19 cases per day for the federal states in Germany, collected by the RKI</li>\\n</ul>\\n\\n<p>This RDF files are based on the&nbsp;NPGEO Corona Hub 2020</p>\\n\\n<ul>\\n\\t<li>https://opendata.arcgis.com/datasets/dd4580c810204019a7b8eb3e0b329dd6_0.geojson</li>\\n\\t<li>https://npgeo-corona-npgeo-de.hub.arcgis.com/datasets/dd4580c810204019a7b8eb3e0b329dd6_0/data</li>\\n</ul>", 
    "language": "eng", 
    "title": "Linked COVID-19 Data: Robert Koch-Institut (RKI)", 
    "license": {
      "id": "CC-BY-4.0"
    }, 
    "relations": {
      "version": [
        {
          "count": 5, 
          "index": 4, 
          "parent": {
            "pid_type": "recid", 
            "pid_value": "3757283"
          }, 
          "is_last": true, 
          "last_child": {
            "pid_type": "recid", 
            "pid_value": "3763274"
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
        "term": "2020 coronavirus pandemic in Germany", 
        "scheme": "url", 
        "identifier": "http://www.wikidata.org/entity/Q83889294"
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
      "Robert-Koch Insitute"
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
        "identifier": "10.5281/zenodo.3757283", 
        "relation": "isVersionOf"
      }
    ]
  }
}""")

        # taken from https://api.datacite.org/dois/10.5281/zenodo.3763274
        datacite = json.loads('{"data":{"id":"10.5281/zenodo.3763274","type":"dois","attributes":{"doi":"10.5281/zenodo.3763274","prefix":"10.5281","suffix":"zenodo.3763274","identifiers":[{"identifier":"https://doi.org/10.5281/zenodo.3763274","identifierType":"DOI"},{"identifier":"https://zenodo.org/record/3763274","identifierType":"URL"}],"creators":[{"name":"Thiery, Florian","nameType":"Personal","givenName":"Florian","familyName":"Thiery","affiliation":["Research Squirrel Engineers"],"nameIdentifiers":[{"schemeUri":"https://orcid.org","nameIdentifier":"https://orcid.org/0000-0002-3246-3531","nameIdentifierScheme":"ORCID"}]}],"titles":[{"title":"Linked COVID-19 Data: Robert Koch-Institut (RKI)"}],"publisher":"Zenodo","container":{"type":"DataRepository","identifier":"https://zenodo.org/communities/covid-19","identifierType":"URL"},"publicationYear":2020,"subjects":[{"subject":"Linked Data"},{"subject":"COVID-19"},{"subject":"Robert-Koch Insitute"},{"subject":"http://www.wikidata.org/entity/Q84263196","subjectScheme":"url"},{"subject":"http://www.wikidata.org/entity/Q81068910","subjectScheme":"url"},{"subject":"http://www.wikidata.org/entity/Q83889294","subjectScheme":"url"},{"subject":"http://www.wikidata.org/entity/Q91205721","subjectScheme":"url"}],"contributors":[],"dates":[{"date":"2020-04-23","dateType":"Issued"}],"language":"en","types":{"ris":"DATA","bibtex":"misc","citeproc":"dataset","schemaOrg":"Dataset","resourceTypeGeneral":"Dataset"},"relatedIdentifiers":[{"relationType":"IsVersionOf","relatedIdentifier":"10.5281/zenodo.3757283","relatedIdentifierType":"DOI"},{"relationType":"IsPartOf","relatedIdentifier":"https://zenodo.org/communities/covid-19","relatedIdentifierType":"URL"},{"relationType":"IsPartOf","relatedIdentifier":"https://zenodo.org/communities/researchsquirrelengineers","relatedIdentifierType":"URL"},{"relationType":"IsPartOf","relatedIdentifier":"https://zenodo.org/communities/zenodo","relatedIdentifierType":"URL"}],"sizes":[],"formats":[],"version":null,"rightsList":[{"rights":"Creative Commons Attribution 4.0 International","rightsUri":"http://creativecommons.org/licenses/by/4.0/legalcode"},{"rights":"Open Access","rightsUri":"info:eu-repo/semantics/openAccess"}],"descriptions":[{"description":"Linked COVID-19 Data derived from <strong>Robert Koch Institute</strong> using the COVID-19 Ontology 10.5281/zenodo.3757828 developed for the Linked COVID-19 Data Dashboard: http://covid19data.link This files include data for covid19_rki*.ttl - single COVID-19 cases per day, collected by the RKI https://www.arcgis.com/home/item.html?id=dd4580c810204019a7b8eb3e0b329dd6 \\"confirmed\\" is calcaulated by the column \\"Refdatum\\" covid19_rki_cum.ttl - COVID-19 cases per day for Germany, collected by the RKI covid19_rki_fs.ttl - COVID-19 cases per day for the federal states in Germany, collected by the RKI This RDF files are based on the NPGEO Corona Hub 2020 https://opendata.arcgis.com/datasets/dd4580c810204019a7b8eb3e0b329dd6_0.geojson https://npgeo-corona-npgeo-de.hub.arcgis.com/datasets/dd4580c810204019a7b8eb3e0b329dd6_0/data","descriptionType":"Abstract"}],"geoLocations":[],"fundingReferences":[],"xml":"PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0idXRmLTgiPz4KPHJlc291cmNlIHhtbG5zOnhzaT0iaHR0cDovL3d3dy53My5vcmcvMjAwMS9YTUxTY2hlbWEtaW5zdGFuY2UiIHhtbG5zPSJodHRwOi8vZGF0YWNpdGUub3JnL3NjaGVtYS9rZXJuZWwtNCIgeHNpOnNjaGVtYUxvY2F0aW9uPSJodHRwOi8vZGF0YWNpdGUub3JnL3NjaGVtYS9rZXJuZWwtNCBodHRwOi8vc2NoZW1hLmRhdGFjaXRlLm9yZy9tZXRhL2tlcm5lbC00LjEvbWV0YWRhdGEueHNkIj4KICA8aWRlbnRpZmllciBpZGVudGlmaWVyVHlwZT0iRE9JIj4xMC41MjgxL1pFTk9ETy4zNzYzMjc0PC9pZGVudGlmaWVyPgogIDxjcmVhdG9ycz4KICAgIDxjcmVhdG9yPgogICAgICA8Y3JlYXRvck5hbWU+RmxvcmlhbiBUaGllcnk8L2NyZWF0b3JOYW1lPgogICAgICA8bmFtZUlkZW50aWZpZXIgbmFtZUlkZW50aWZpZXJTY2hlbWU9Ik9SQ0lEIiBzY2hlbWVVUkk9Imh0dHA6Ly9vcmNpZC5vcmcvIj4wMDAwLTAwMDItMzI0Ni0zNTMxPC9uYW1lSWRlbnRpZmllcj4KICAgICAgPGFmZmlsaWF0aW9uPlJlc2VhcmNoIFNxdWlycmVsIEVuZ2luZWVyczwvYWZmaWxpYXRpb24+CiAgICA8L2NyZWF0b3I+CiAgPC9jcmVhdG9ycz4KICA8dGl0bGVzPgogICAgPHRpdGxlPkxpbmtlZCBDT1ZJRC0xOSBEYXRhOiBSb2JlcnQgS29jaC1JbnN0aXR1dCAoUktJKTwvdGl0bGU+CiAgPC90aXRsZXM+CiAgPHB1Ymxpc2hlcj5aZW5vZG88L3B1Ymxpc2hlcj4KICA8cHVibGljYXRpb25ZZWFyPjIwMjA8L3B1YmxpY2F0aW9uWWVhcj4KICA8c3ViamVjdHM+CiAgICA8c3ViamVjdD5MaW5rZWQgRGF0YTwvc3ViamVjdD4KICAgIDxzdWJqZWN0PkNPVklELTE5PC9zdWJqZWN0PgogICAgPHN1YmplY3Q+Um9iZXJ0LUtvY2ggSW5zaXR1dGU8L3N1YmplY3Q+CiAgICA8c3ViamVjdCBzdWJqZWN0U2NoZW1lPSJ1cmwiPmh0dHA6Ly93d3cud2lraWRhdGEub3JnL2VudGl0eS9RODQyNjMxOTY8L3N1YmplY3Q+CiAgICA8c3ViamVjdCBzdWJqZWN0U2NoZW1lPSJ1cmwiPmh0dHA6Ly93d3cud2lraWRhdGEub3JnL2VudGl0eS9RODEwNjg5MTA8L3N1YmplY3Q+CiAgICA8c3ViamVjdCBzdWJqZWN0U2NoZW1lPSJ1cmwiPmh0dHA6Ly93d3cud2lraWRhdGEub3JnL2VudGl0eS9RODM4ODkyOTQ8L3N1YmplY3Q+CiAgICA8c3ViamVjdCBzdWJqZWN0U2NoZW1lPSJ1cmwiPmh0dHA6Ly93d3cud2lraWRhdGEub3JnL2VudGl0eS9ROTEyMDU3MjE8L3N1YmplY3Q+CiAgPC9zdWJqZWN0cz4KICA8ZGF0ZXM+CiAgICA8ZGF0ZSBkYXRlVHlwZT0iSXNzdWVkIj4yMDIwLTA0LTIzPC9kYXRlPgogIDwvZGF0ZXM+CiAgPGxhbmd1YWdlPmVuPC9sYW5ndWFnZT4KICA8cmVzb3VyY2VUeXBlIHJlc291cmNlVHlwZUdlbmVyYWw9IkRhdGFzZXQiLz4KICA8YWx0ZXJuYXRlSWRlbnRpZmllcnM+CiAgICA8YWx0ZXJuYXRlSWRlbnRpZmllciBhbHRlcm5hdGVJZGVudGlmaWVyVHlwZT0idXJsIj5odHRwczovL3plbm9kby5vcmcvcmVjb3JkLzM3NjMyNzQ8L2FsdGVybmF0ZUlkZW50aWZpZXI+CiAgPC9hbHRlcm5hdGVJZGVudGlmaWVycz4KICA8cmVsYXRlZElkZW50aWZpZXJzPgogICAgPHJlbGF0ZWRJZGVudGlmaWVyIHJlbGF0ZWRJZGVudGlmaWVyVHlwZT0iRE9JIiByZWxhdGlvblR5cGU9IklzVmVyc2lvbk9mIj4xMC41MjgxL3plbm9kby4zNzU3MjgzPC9yZWxhdGVkSWRlbnRpZmllcj4KICAgIDxyZWxhdGVkSWRlbnRpZmllciByZWxhdGVkSWRlbnRpZmllclR5cGU9IlVSTCIgcmVsYXRpb25UeXBlPSJJc1BhcnRPZiI+aHR0cHM6Ly96ZW5vZG8ub3JnL2NvbW11bml0aWVzL2NvdmlkLTE5PC9yZWxhdGVkSWRlbnRpZmllcj4KICAgIDxyZWxhdGVkSWRlbnRpZmllciByZWxhdGVkSWRlbnRpZmllclR5cGU9IlVSTCIgcmVsYXRpb25UeXBlPSJJc1BhcnRPZiI+aHR0cHM6Ly96ZW5vZG8ub3JnL2NvbW11bml0aWVzL3Jlc2VhcmNoc3F1aXJyZWxlbmdpbmVlcnM8L3JlbGF0ZWRJZGVudGlmaWVyPgogICAgPHJlbGF0ZWRJZGVudGlmaWVyIHJlbGF0ZWRJZGVudGlmaWVyVHlwZT0iVVJMIiByZWxhdGlvblR5cGU9IklzUGFydE9mIj5odHRwczovL3plbm9kby5vcmcvY29tbXVuaXRpZXMvemVub2RvPC9yZWxhdGVkSWRlbnRpZmllcj4KICA8L3JlbGF0ZWRJZGVudGlmaWVycz4KICA8cmlnaHRzTGlzdD4KICAgIDxyaWdodHMgcmlnaHRzVVJJPSJodHRwOi8vY3JlYXRpdmVjb21tb25zLm9yZy9saWNlbnNlcy9ieS80LjAvbGVnYWxjb2RlIj5DcmVhdGl2ZSBDb21tb25zIEF0dHJpYnV0aW9uIDQuMCBJbnRlcm5hdGlvbmFsPC9yaWdodHM+CiAgICA8cmlnaHRzIHJpZ2h0c1VSST0iaW5mbzpldS1yZXBvL3NlbWFudGljcy9vcGVuQWNjZXNzIj5PcGVuIEFjY2VzczwvcmlnaHRzPgogIDwvcmlnaHRzTGlzdD4KICA8ZGVzY3JpcHRpb25zPgogICAgPGRlc2NyaXB0aW9uIGRlc2NyaXB0aW9uVHlwZT0iQWJzdHJhY3QiPiZsdDtwJmd0O0xpbmtlZCBDT1ZJRC0xOSBEYXRhIGRlcml2ZWQgZnJvbSZsdDsvcCZndDsKCiZsdDtwJmd0OyZsdDtzdHJvbmcmZ3Q7Um9iZXJ0IEtvY2ggSW5zdGl0dXRlJmx0Oy9zdHJvbmcmZ3Q7Jmx0Oy9wJmd0OwoKJmx0O3AmZ3Q7dXNpbmcgdGhlIENPVklELTE5IE9udG9sb2d5Jmx0Oy9wJmd0OwoKJmx0O3AmZ3Q7Jmx0O2EgaHJlZj0iaHR0cHM6Ly9kb2kub3JnLzEwLjUyODEvemVub2RvLjM3NTc4MjgiJmd0OzEwLjUyODEvemVub2RvLjM3NTc4MjgmbHQ7L2EmZ3Q7Jmx0Oy9wJmd0OwoKJmx0O3AmZ3Q7ZGV2ZWxvcGVkIGZvciB0aGUgTGlua2VkIENPVklELTE5IERhdGEmYW1wO25ic3A7RGFzaGJvYXJkOiZhbXA7bmJzcDsmbHQ7YSBocmVmPSJodHRwOi8vY292aWQxOWRhdGEubGluay8iJmd0O2h0dHA6Ly9jb3ZpZDE5ZGF0YS5saW5rJmx0Oy9hJmd0OyZsdDsvcCZndDsKCiZsdDtwJmd0OyZhbXA7bmJzcDsmbHQ7L3AmZ3Q7CgombHQ7cCZndDtUaGlzIGZpbGVzIGluY2x1ZGUgZGF0YSBmb3ImbHQ7L3AmZ3Q7CgombHQ7dWwmZ3Q7CgkmbHQ7bGkmZ3Q7Y292aWQxOV9ya2kqLnR0bCAtIHNpbmdsZSBDT1ZJRC0xOSBjYXNlcyBwZXIgZGF5LCBjb2xsZWN0ZWQgYnkgdGhlIFJLSQoJJmx0O3VsJmd0OwoJCSZsdDtsaSZndDtodHRwczovL3d3dy5hcmNnaXMuY29tL2hvbWUvaXRlbS5odG1sP2lkPWRkNDU4MGM4MTAyMDQwMTlhN2I4ZWIzZTBiMzI5ZGQ2Jmx0Oy9saSZndDsKCQkmbHQ7bGkmZ3Q7JmFtcDtxdW90O2NvbmZpcm1lZCZhbXA7cXVvdDsgaXMgY2FsY2F1bGF0ZWQgYnkgdGhlIGNvbHVtbiAmYW1wO3F1b3Q7UmVmZGF0dW0mYW1wO3F1b3Q7Jmx0Oy9saSZndDsKCSZsdDsvdWwmZ3Q7CgkmbHQ7L2xpJmd0OwoJJmx0O2xpJmd0O2NvdmlkMTlfcmtpX2N1bS50dGwgLSBDT1ZJRC0xOSBjYXNlcyBwZXIgZGF5IGZvciBHZXJtYW55LCBjb2xsZWN0ZWQgYnkgdGhlIFJLSSZsdDsvbGkmZ3Q7CgkmbHQ7bGkmZ3Q7Y292aWQxOV9ya2lfZnMudHRsIC0gQ09WSUQtMTkgY2FzZXMgcGVyIGRheSBmb3IgdGhlIGZlZGVyYWwgc3RhdGVzIGluIEdlcm1hbnksIGNvbGxlY3RlZCBieSB0aGUgUktJJmx0Oy9saSZndDsKJmx0Oy91bCZndDsKCiZsdDtwJmd0O1RoaXMgUkRGIGZpbGVzIGFyZSBiYXNlZCBvbiB0aGUmYW1wO25ic3A7TlBHRU8gQ29yb25hIEh1YiAyMDIwJmx0Oy9wJmd0OwoKJmx0O3VsJmd0OwoJJmx0O2xpJmd0O2h0dHBzOi8vb3BlbmRhdGEuYXJjZ2lzLmNvbS9kYXRhc2V0cy9kZDQ1ODBjODEwMjA0MDE5YTdiOGViM2UwYjMyOWRkNl8wLmdlb2pzb24mbHQ7L2xpJmd0OwoJJmx0O2xpJmd0O2h0dHBzOi8vbnBnZW8tY29yb25hLW5wZ2VvLWRlLmh1Yi5hcmNnaXMuY29tL2RhdGFzZXRzL2RkNDU4MGM4MTAyMDQwMTlhN2I4ZWIzZTBiMzI5ZGQ2XzAvZGF0YSZsdDsvbGkmZ3Q7CiZsdDsvdWwmZ3Q7PC9kZXNjcmlwdGlvbj4KICA8L2Rlc2NyaXB0aW9ucz4KPC9yZXNvdXJjZT4=","url":"https://zenodo.org/record/3763274","contentUrl":null,"metadataVersion":0,"schemaVersion":null,"source":"mds","isActive":true,"state":"findable","reason":null,"viewCount":0,"viewsOverTime":[],"downloadCount":0,"downloadsOverTime":[],"referenceCount":0,"citationCount":0,"citationsOverTime":[],"partCount":0,"partOfCount":0,"versionCount":0,"versionOfCount":0,"created":"2020-04-23T12:14:14.000Z","registered":"2020-04-23T12:14:15.000Z","published":"2020","updated":"2020-04-23T12:14:15.000Z"},"relationships":{"client":{"data":{"id":"cern.zenodo","type":"clients"}},"media":{"data":{"id":"10.5281/zenodo.3763274","type":"media"}},"references":{"data":[]},"citations":{"data":[]},"parts":{"data":[]},"partOf":{"data":[]},"versions":{"data":[]},"versionOf":{"data":[]}}}}')
        return zenodo["metadata"], datacite["data"]["attributes"]
