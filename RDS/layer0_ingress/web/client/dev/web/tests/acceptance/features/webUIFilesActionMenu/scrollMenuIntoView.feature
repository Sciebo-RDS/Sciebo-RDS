Feature: scroll menu of actions that can be done on a file into view
  As a user
  I want to see the whole menu of actions that can be done on a file
  So that I can manage and work with my files

  Background:
    Given user "Alice" has been created with default attributes and without skeleton files
    And user "Alice" has logged in using the webUI
    And the user has browsed to the files page

  @skip
  Scenario: scroll the file actions menu into view
    When the user creates so many files/folders that they do not fit in one browser page
    Then the files action menu should be completely visible after opening it using the webUI
