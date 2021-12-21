Feature: Locks
  As a user
  I would like to be able to use locks control deletion of files and folders
  So that I can prevent files and folders being deleted while they are being used by another user

  Background:
    #do not set email, see bugs in https://github.com/owncloud/core/pull/32250#issuecomment-434615887
    Given these users have been created with default attributes and without skeleton files:
      | username       |
      | brand-new-user |
    And user "brand-new-user" has created folder "simple-folder"
    And user "brand-new-user" has created file "simple-folder/lorem.txt"
    And user "brand-new-user" has created file "lorem.txt"
    And user "brand-new-user" has logged in using the webUI

  @issue-5417
  Scenario Outline: deleting a locked file
    Given user "brand-new-user" has locked folder "lorem.txt" setting following properties
      | lockscope | <lockscope> |
    And the user has browsed to the files page
    When the user tries to delete folder "lorem.txt" using the webUI
    Then notifications should be displayed on the webUI with the text
      """
      Error while deleting "lorem.txt" - the file is locked
      """
    When the user reloads the current page of the webUI
    Then file "lorem.txt" should be listed on the webUI
    And file "lorem.txt" should be marked as locked on the webUI
    And file "lorem.txt" should be marked as locked by user "brand-new-user" in the locks tab of the details panel on the webUI
    Examples:
      | lockscope |
      | exclusive |
      | shared    |

  @issue-5417
  Scenario Outline: deleting a file in a locked folder
    Given user "brand-new-user" has locked folder "simple-folder" setting following properties
      | lockscope | <lockscope> |
    And the user has browsed to the files page
    And the user has opened folder "simple-folder"
    When the user tries to delete folder "lorem.txt" using the webUI
    Then notifications should be displayed on the webUI with the text
      """
      Error while deleting "lorem.txt" - the file is locked
      """
    When the user reloads the current page of the webUI
    Then file "lorem.txt" should be listed on the webUI
    When the user browses to the files page
    Then folder "simple-folder" should be marked as locked on the webUI
    And folder "simple-folder" should be marked as locked by user "brand-new-user" in the locks tab of the details panel on the webUI
    Examples:
      | lockscope |
      | exclusive |
      | shared    |

  @issue-core-38912
  Scenario Outline: deleting a file in a public share of a locked folder
    Given user "brand-new-user" has created folder "simple-folder"
    And user "brand-new-user" has created file "simple-folder/lorem.txt"
    And user "brand-new-user" has locked folder "simple-folder" setting following properties
      | lockscope | <lockscope> |
    And user "brand-new-user" has created a public link with following settings
      | path        | simple-folder                |
      | permissions | read, create, delete, update |
    When the public uses the webUI to access the last public link created by user "brand-new-user"
    And the user tries to delete folder "lorem.txt" using the webUI
    Then notifications should be displayed on the webUI with the text
      """
      Error while deleting "lorem.txt" - the file is locked
      """
    When the user reloads the current page of the webUI
    Then file "lorem.txt" should be listed on the webUI
    Examples:
      | lockscope |
      | exclusive |
      | shared    |