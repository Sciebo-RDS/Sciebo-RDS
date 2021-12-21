@app-required @notifications-app-required @ocis-reva-issue-14
Feature: Sharing files and folders with internal users
  As a user
  I want to share files and folders with other users
  So that those users can access the files and folders

  Background:
    Given the setting "shareapi_auto_accept_share" of app "core" has been set to "no"
    And the administrator has set the default folder for received shares to "Shares"
    And app "notifications" has been enabled
    And these users have been created with default attributes and without skeleton files:
      | username |
      | Alice    |
      | Brian    |
    And user "Alice" has created folder "simple-folder"
    And user "Alice" has created folder "simple-empty-folder"
    And user "Alice" has uploaded file "data.zip" to "data.zip"
    And user "Alice" has uploaded file "lorem.txt" to "simple-folder/lorem.txt"

  @smokeTest
  Scenario: notifications about new share is displayed when auto-accepting is disabled
    Given user "Alice" has shared folder "simple-folder" with user "Brian"
    And user "Alice" has shared folder "data.zip" with user "Brian"
    When user "Brian" logs in using the webUI
    Then the user should see the notification bell on the webUI
    And the user should see 2 notifications on the webUI with these details
      | title                                      |
      | "Alice Hansen" shared "simple-folder" with you |
      | "Alice Hansen" shared "data.zip" with you      |

  @smokeTest
  Scenario: Notification is gone after accepting a share
    Given user "Alice" has shared folder "simple-folder" with user "Brian"
    And user "Alice" has shared folder "simple-empty-folder" with user "Brian"
    When user "Brian" logs in using the webUI
    And the user accepts all shares displayed in the notifications on the webUI
    Then the user should have no notifications

  @smokeTest
  Scenario: accept an offered share
    Given user "Alice" has shared folder "simple-folder" with user "Brian"
    And user "Alice" has shared folder "simple-empty-folder" with user "Brian"
    When user "Brian" logs in using the webUI
    And the user accepts all shares displayed in the notifications on the webUI
    And the user browses to the folder "Shares" on the files page
    Then folder "simple-folder" should be listed on the webUI
    And folder "simple-empty-folder" should be listed on the webUI
    When the user browses to the shared-with-me page using the webUI
    Then folder "simple-folder" shared by "Alice Hansen" should be in "Accepted" state on the webUI
    And folder "simple-empty-folder" shared by "Alice Hansen" should be in "Accepted" state on the webUI

  @smokeTest
  Scenario: reject an offered share
    Given user "Alice" has shared folder "simple-folder" with user "Brian"
    And user "Alice" has shared folder "simple-empty-folder" with user "Brian"
    When user "Brian" logs in using the webUI
    And the user declines all shares displayed in the notifications on the webUI
    Then folder "Shares" should not be listed on the webUI
    And folder "simple-folder" should not be listed on the webUI
    And folder "simple-empty-folder" should not be listed on the webUI
    When the user browses to the shared-with-me page using the webUI
    Then folder "simple-folder" shared by "Alice Hansen" should be in "Declined" state on the webUI
    And folder "simple-empty-folder" shared by "Alice Hansen" should be in "Declined" state on the webUI

