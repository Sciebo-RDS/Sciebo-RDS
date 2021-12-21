Feature: User Journey 1

  As a user
  I would like to do basic file operations

  Background:
    Given user "Alice" has been created with default attributes and without skeleton files
    And user "Brian" has been created with default attributes and without skeleton files

  @journey
  Scenario: simple upload of a file that does not exist before
    When user "Alice" has logged in using the webUI
    And the user uploads file "new-lorem.txt" using the webUI
    Then no message should be displayed on the webUI
    And file "new-lorem.txt" should be listed on the webUI
    And as "Alice" the content of "new-lorem.txt" should be the same as the content of local file "new-lorem.txt"
    When the user browses to the files page
    And the user downloads file "new-lorem.txt" using the webUI
    Then no message should be displayed on the webUI
    And the user renames file "new-lorem.txt" to "new-lorem2.txt" using the webUI
    And file "new-lorem2.txt" should be listed on the webUI
    And the user deletes file "new-lorem2.txt" using the webUI
    And the user browses to the trashbin page
    And file "new-lorem2.txt" should be listed on the webUI
    And the user restores file "new-lorem2.txt" from the trashbin using the webUI
    And the user browses to the files page
    And file "new-lorem2.txt" should be listed on the webUI
