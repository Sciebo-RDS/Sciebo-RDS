@notToImplementOnOCIS
Feature: Sharing folders with multiple internal users using advanced permissions
  As a user
  I want to set advanced permissions on shared folders with other users
  So that I can control the access on those folders by other collaborators

  Background:
    Given these users have been created with default attributes and without skeleton files:
      | username |
      | Alice    |
      | Brian    |
    And user "Alice" has created folder "simple-folder"
    And user "Alice" has uploaded file "lorem.txt" to "simple-folder/lorem.txt"

  Scenario Outline: share a folder with multiple users using role as advanced permissions role and different extra permissions
    Given these users have been created with default attributes and without skeleton files:
      | username |
      | user0    |
      | Carol    |
      | David    |
    And user "Alice" has logged in using the webUI
    When the user opens the share dialog for folder "simple-folder" using the webUI
    And the user opens the share creation dialog in the webUI
    And the user selects the following collaborators for the share as "<role>" with "<extra-permissions>" permissions:
      | collaborator | type |
      | Regular User | user |
      | Brian Murphy | user |
      | Carol King   | user |
      | David Lopez  | user |
    And the user removes "David Lopez" as a collaborator from the share
    And the user removes "Regular User" as a collaborator from the share
    And the user shares with the selected collaborators
    Then custom permissions "<displayed-permissions>" should be set for user "Brian Murphy" for folder "simple-folder" on the webUI
    And custom permissions "<displayed-permissions>" should be set for user "Carol King" for folder "simple-folder" on the webUI
    And user "Brian Murphy" should be listed as "<displayed-role>" in the collaborators list for folder "simple-folder" on the webUI
    And user "Carol King" should be listed as "<displayed-role>" in the collaborators list for folder "simple-folder" on the webUI
    And user "Brian" should have received a share with these details:
      | field       | value                |
      | uid_owner   | Alice                |
      | share_with  | Brian                |
      | file_target | /simple-folder       |
      | item_type   | folder               |
      | permissions | <actual-permissions> |
    And user "Carol" should have received a share with these details:
      | field       | value                |
      | uid_owner   | Alice                |
      | share_with  | Carol                |
      | file_target | /simple-folder       |
      | item_type   | folder               |
      | permissions | <actual-permissions> |
    But user "Regular User" should not be listed in the collaborators list on the webUI
    And as "user0" folder "simple-folder" should not exist
    And user "David Lopez" should not be listed in the collaborators list on the webUI
    And as "David" folder "simple-folder" should not exist
    Examples:
      | role                 | displayed-role       | extra-permissions     | displayed-permissions | actual-permissions          |
      # | Advanced permissions | Advanced permissions | delete                        | delete                | read, delete                 |
      # | Advanced permissions | Advanced permissions | update                        | update                | read, update                 |
      # | Advanced permissions | Advanced permissions | create                        | create                | read, create                 |
      # | Advanced permissions | Advanced permissions | share, delete                 | share, delete         | read, share, delete          |
      # | Advanced permissions | Advanced permissions | share, update                 | share, update         | read, update, share          |
      # | Advanced permissions | Advanced permissions | share, create                 | share, create         | read, share, create          |
      # | Advanced permissions | Advanced permissions | delete, update                | delete, update        | read, delete, update         |
      # | Advanced permissions | Advanced permissions | delete, create                | delete, create        | read, delete, create         |
      # | Advanced permissions | Advanced permissions | update, create                | update, create        | read, update, create         |
      # | Advanced permissions | Advanced permissions | share, delete, update         | share, delete, update | read, share, delete, update  |
      # | Advanced permissions | Advanced permissions | share, create, delete         | share, create, delete | read, share, delete, create  |
      | Advanced permissions | Advanced permissions | share, update, create | share, update, create | read, share, update, create |
