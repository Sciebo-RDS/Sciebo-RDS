Feature: create folder
  As a user
  I want to create folders
  So that I can organise my data structure

  Background:
    Given user "Alice" has been created with default attributes and without skeleton files
    And user "Alice" has logged in using the webUI
    And the user has browsed to the files page


  Scenario Outline: Create a folder using special characters
    When the user creates a folder with the name <folder_name> using the webUI
    Then folder <folder_name> should be listed on the webUI
    When the user reloads the current page of the webUI
    Then folder <folder_name> should be listed on the webUI
    Examples:
      | folder_name                |
      | '"somequotes1"'            |
      | "'somequotes2'"            |
      | "\"quote\"d-folders'"      |
      | "^#29][29@({"              |
      | "+-{$(882)"                |
      | "home"                     |
      | "Sample,Folder,With,Comma" |
      | 'सिमप्ले फोल्देर $%#?&@'   |

  @issue-2467 @ocis-reva-issue-106
  Scenario Outline: Create a sub-folder inside a folder with problematic name
    # First try and create a folder with problematic name
    # Then try and create a sub-folder inside the folder with problematic name
    When the user creates a folder with the name <folder> using the webUI
    And the user opens folder <folder> using the webUI
    Then there should be no resources listed on the webUI
    When the user creates a folder with the name "sub-folder" using the webUI
    Then folder "sub-folder" should be listed on the webUI
    When the user reloads the current page of the webUI
    Then folder "sub-folder" should be listed on the webUI
    And as "Alice" folder "sub-folder" should exist inside folder <folder>
    Examples:
      | folder    |
     #| "?&%0"    |
      | "^#2929@" |
      | "home"    |

  @smokeTest @ocis-reva-issue-106
  Scenario Outline: Create a sub-folder inside an existing folder with problematic name
    # Use an existing folder with problematic name to create a sub-folder
    # Uses the folder created by skeleton
    Given user "Alice" has created folder <folder>
    And the user has reloaded the current page of the webUI
    When the user opens folder <folder> using the webUI
    And the user creates a folder with the name "sub-folder" using the webUI
    Then folder "sub-folder" should be listed on the webUI
    When the user reloads the current page of the webUI
    Then folder "sub-folder" should be listed on the webUI
    And as "Alice" folder "sub-folder" should exist inside folder <folder>
    Examples:
      | folder                  |
      | "0"                     |
      | "'single'quotes"        |
      | "strängé नेपाली folder" |
