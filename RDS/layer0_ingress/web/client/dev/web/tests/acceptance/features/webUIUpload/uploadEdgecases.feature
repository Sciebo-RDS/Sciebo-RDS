Feature: File Upload

  As a QA engineer
  I would like to test uploads of all kind of funny filenames via the WebUI

  These tests are written in a way that multiple file names are tested in one scenario
  that is not academically correct but saves a lot of time

  Background:
    Given user "Alice" has been created with default attributes and without skeleton files
    And user "Alice" has logged in using the webUI
    And the user browses to the files page


  Scenario: simple upload of a file that does not exist before
    When the user uploads file "new-'single'quotes.txt" using the webUI
    Then file "new-'single'quotes.txt" should be listed on the webUI
    And as "Alice" the content of "new-'single'quotes.txt" should be the same as the content of local file "new-'single'quotes.txt"

    When the user uploads file "new-strängé filename (duplicate #2 &).txt" using the webUI
    Then file "new-strängé filename (duplicate #2 &).txt" should be listed on the webUI
    And as "Alice" the content of "new-strängé filename (duplicate #2 &).txt" should be the same as the content of local file "new-strängé filename (duplicate #2 &).txt"

    When the user uploads file "zzzz-zzzz-will-be-at-the-end-of-the-folder-when-uploaded.txt" using the webUI
    Then file "zzzz-zzzz-will-be-at-the-end-of-the-folder-when-uploaded.txt" should be listed on the webUI
    And as "Alice" the content of "zzzz-zzzz-will-be-at-the-end-of-the-folder-when-uploaded.txt" should be the same as the content of local file "zzzz-zzzz-will-be-at-the-end-of-the-folder-when-uploaded.txt"

  @smokeTest @ocisSmokeTest
  Scenario Outline: upload a new file into a sub folder
    Given user "Alice" has created folder "<folder-to-upload-to>"
    And the user has browsed to the files page
    And a file with the size of "3000" bytes and the name "0" has been created locally
    When the user opens folder "<folder-to-upload-to>" using the webUI
    And the user uploads a created file "0" using the webUI
    Then file "0" should be listed on the webUI
    And as "Alice" the content of "<folder-to-upload-to>/0" should be the same as the content of local file "0"
    When the user uploads file "new-'single'quotes.txt" using the webUI
    Then file "new-'single'quotes.txt" should be listed on the webUI
    And as "Alice" the content of "<folder-to-upload-to>/new-'single'quotes.txt" should be the same as the content of local file "new-'single'quotes.txt"
    When the user uploads file "new-strängé filename (duplicate #2 &).txt" using the webUI
    Then file "new-strängé filename (duplicate #2 &).txt" should be listed on the webUI
    And as "Alice" the content of "<folder-to-upload-to>/new-strängé filename (duplicate #2 &).txt" should be the same as the content of local file "new-strängé filename (duplicate #2 &).txt"
    When the user uploads file "zzzz-zzzz-will-be-at-the-end-of-the-folder-when-uploaded.txt" using the webUI
    Then file "zzzz-zzzz-will-be-at-the-end-of-the-folder-when-uploaded.txt" should be listed on the webUI
    And as "Alice" the content of "<folder-to-upload-to>/zzzz-zzzz-will-be-at-the-end-of-the-folder-when-uploaded.txt" should be the same as the content of local file "zzzz-zzzz-will-be-at-the-end-of-the-folder-when-uploaded.txt"
    Examples:
      | folder-to-upload-to   |
      | 0                     |
      | 'single'quotes        |
      | strängé नेपाली folder |

  @skip
  Scenario: overwrite an existing file
    When the user uploads overwriting file "'single'quotes.txt" using the webUI and retries if the file is locked
    Then file "'single'quotes.txt" should be listed on the webUI
    And as "Alice" the content of "'single'quotes.txt" should be the same as the content of local file "'single'quotes.txt"

    When the user uploads overwriting file "strängé filename (duplicate #2 &).txt" using the webUI and retries if the file is locked
    Then file "strängé filename (duplicate #2 &).txt" should be listed on the webUI
    And as "Alice" the content of "strängé filename (duplicate #2 &).txt" should be the same as the content of local file "strängé filename (duplicate #2 &).txt"

    When the user uploads overwriting file "zzzz-must-be-last-file-in-folder.txt" using the webUI and retries if the file is locked
    Then file "zzzz-must-be-last-file-in-folder.txt" should be listed on the webUI
    And as "Alice" the content of "zzzz-must-be-last-file-in-folder.txt" should be the same as the content of local file "zzzz-must-be-last-file-in-folder.txt"

  @skip
  Scenario: keep new and existing file
    When the user uploads file "'single'quotes.txt" keeping both new and existing files using the webUI
    Then file "'single'quotes.txt" should be listed on the webUI
    And the content of "'single'quotes.txt" should not have changed
    And file "'single'quotes (2).txt" should be listed on the webUI
    And as "Alice" the content of "'single'quotes (2).txt" should be the same as the content of local file "'single'quotes.txt"

    When the user uploads file "strängé filename (duplicate #2 &).txt" keeping both new and existing files using the webUI
    Then file "strängé filename (duplicate #2 &).txt" should be listed on the webUI
    And the content of "strängé filename (duplicate #2 &).txt" should not have changed
    And file "strängé filename (duplicate #2 &) (2).txt" should be listed on the webUI
    And as "Alice" the content of "strängé filename (duplicate #2 &) (2).txt" should be the same as the content of local file "strängé filename (duplicate #2 &).txt"

    When the user uploads file "zzzz-must-be-last-file-in-folder.txt" keeping both new and existing files using the webUI
    Then file "zzzz-must-be-last-file-in-folder.txt" should be listed on the webUI
    And the content of "zzzz-must-be-last-file-in-folder.txt" should not have changed
    And file "zzzz-must-be-last-file-in-folder (2).txt" should be listed on the webUI
    And as "Alice" the content of "zzzz-must-be-last-file-in-folder (2).txt" should be the same as the content of local file "zzzz-must-be-last-file-in-folder.txt"


  Scenario Outline: upload a big file using difficult names (when chunking in implemented that upload should be chunked)
    Given a file with the size of "30000000" bytes and the name <file-name> has been created locally
    When the user uploads a created file <file-name> using the webUI
    Then file <file-name> should be listed on the webUI
    And as "Alice" the content of <file-name> should be the same as the content of local file <file-name>
    Examples:
      | file-name |
      | "&#"      |
      | "TIÄFÜ"   |


  # upload into "simple-folder" because there is already a folder called "0" in the root
  Scenario: Upload a big file called "0" (when chunking in implemented that upload should be chunked)
    Given user "Alice" has created folder "simple-folder"
    And the user has browsed to the files page
    And a file with the size of "30000000" bytes and the name "0" has been created locally
    When the user opens folder "simple-folder" using the webUI
    And the user uploads a created file "0" using the webUI
    Then file "0" should be listed on the webUI
    And as "Alice" the content of "simple-folder/0" should be the same as the content of local file "0"

  @issue-3015 @issue-ocis-reva-200
  Scenario: Upload a file with the same name as already existing folder
    Given user "Alice" has created folder "new-lorem.txt"
    And the user has reloaded the current page of the webUI
    When the user uploads overwriting file "new-lorem.txt" using the webUI
    Then the following error message should be displayed on the webUI
      """
      File upload failed…
      PUT is not allowed on non-files.
      """
    # Then the following error message should be displayed on the webUI
    #   """
    #   (Any nice error message)
    #   """

  # When this issue is fixed merge with the scenario above
  @issue-3015 @skipOnOC10 @issue-ocis-reva-200
  Scenario: Upload a file with the same name as already existing folder (ocis bug demonstration)
    Given user "Alice" has created folder "new-lorem.txt"
    And the user has reloaded the current page of the webUI
    When the user uploads overwriting file "new-lorem.txt" using the webUI
    Then the following error message should be displayed on the webUI
      """
      File upload failed…
      Unknown error
      """
    # Then the following error message should be displayed on the webUI
    #   """
    #   (Any nice error message)
    #   """
