@ocis-issue-1277 @ocis-issue-2260
Feature: Sharing folders with internal groups with different roles and permissions
  As a user
  I want to set different permissions on shared folders with groups
  So that I can control the access on those folders by other users on the group

  Background:
    Given the setting "shareapi_auto_accept_share" of app "core" has been set to "no"
    And the administrator has set the default folder for received shares to "Shares"
    And these users have been created with default attributes and without skeleton files:
      | username |
      | Alice    |
      | Brian    |
      | Carol    |
    And these groups have been created:
      | groupname |
      | grp1      |
    And user "Alice" has been added to group "grp1"
    And user "Brian" has been added to group "grp1"

  @issue-1837
  Scenario Outline: share a folder with multiple users with different roles and permissions
    Given group "grp2" has been created
    And user "Alice" has created folder "simple-folder"
    And user "Brian" has been added to group "grp2"
    And user "Alice" has logged in using the webUI
    When the user opens the share dialog for folder "simple-folder" using the webUI
    And the user opens the share creation dialog in the webUI
    And the user selects the following collaborators for the share as "<role>" with "<extra-permissions>" permissions:
      | collaborator | type  |
      | grp1         | group |
      | Carol King   | user  |
      | grp2         | group |
    And the user removes "grp1" as a collaborator from the share
    And the user removes "Alice Hansen" as a collaborator from the share
    And the user shares with the selected collaborators
    And user "Brian" accepts the share "simple-folder" offered by user "Alice" using the sharing API
    And user "Carol" accepts the share "simple-folder" offered by user "Alice" using the sharing API
    Then custom permissions "<displayed-permissions>" should be set for user "grp2" for folder "simple-folder" on the webUI
    And custom permissions "<displayed-permissions>" should be set for user "Carol King" for folder "simple-folder" on the webUI
    And group "grp2" should be listed as "<displayed-role>" in the collaborators list for folder "simple-folder" on the webUI
    And user "Carol King" should be listed as "<displayed-role>" in the collaborators list for folder "simple-folder" on the webUI
    And user "Brian" should have received a share with these details:
      | field       | value                 |
      | uid_owner   | Alice                 |
      | share_with  | grp2                  |
      | file_target | /Shares/simple-folder |
      | item_type   | folder                |
      | permissions | <actual-permissions>  |
    And user "Carol" should have received a share with these details:
      | field       | value                 |
      | uid_owner   | Alice                 |
      | share_with  | Carol                 |
      | file_target | /Shares/simple-folder |
      | item_type   | folder                |
      | permissions | <actual-permissions>  |
    But group "grp1" should not be listed in the collaborators list on the webUI
    And as "Alice" folder "/Shares/simple-folder" should not exist
    Examples:
      | role                 | displayed-role       | extra-permissions             | displayed-permissions  | actual-permissions           |
      | Viewer               | Viewer               | ,                             | ,                      | read, share                  |
      | Editor               | Editor               | ,                             | ,                      | all                          |
      | Advanced permissions | Advanced permissions | ,                             | ,                      | read                         |
      | Advanced permissions | Viewer               | share                         | ,                      | read, share                  |
      | Advanced permissions | Advanced permissions | delete, update, create        | delete, update, create | read, delete, update, create |
      | Advanced permissions | Editor               | share, delete, update, create | ,                      | all                          |
