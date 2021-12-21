@api @issue-ocis-1012
# after fixing all issues delete these Scenarios and use the one from oC10 core
Feature: OPTIONS request

  Background:
    Given user "Alice" has been created with default attributes and without skeleton files

  Scenario: send OPTIONS request to webDav endpoints using the TUS protocol with valid username and wrong password
    When user "Alice" requests these endpoints with "OPTIONS" including body "doesnotmatter" using password "invalid" about user "Alice"
      | endpoint                          |
      | /remote.php/webdav/               |
      | /remote.php/dav/files/%username%/ |
    Then the following headers should not be set
      | header        |
      | Tus-Resumable |
      | Tus-Version   |
      | Tus-Extension |

  Scenario: send OPTIONS requests to webDav endpoints using valid password and username of different user
    Given user "Brian" has been created with default attributes and without skeleton files
    When user "Brian" requests these endpoints with "OPTIONS" including body "doesnotmatter" using the password of user "Alice"
      | endpoint                          |
      | /remote.php/webdav/               |
      | /remote.php/dav/files/%username%/ |
    Then the following headers should not be set
      | header        |
      | Tus-Resumable |
      | Tus-Version   |
      | Tus-Extension |
