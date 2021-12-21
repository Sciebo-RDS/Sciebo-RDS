Feature: Upload a file

  As a user
  I would like to upload a file
  So that I can store it in owncloud

  Background:
    Given user "Alice" has been created with default attributes and without skeleton files

  @smokeTest
  @issue-1049
  Scenario: simple upload of a file with the size greater than the size of quota
    Given the quota of user "Alice" has been set to "10 MB"
    And user "Alice" has logged in using the webUI
    And the user has browsed to the files page
    And a file with the size of "30000000" bytes and the name "big-video.mp4" has been created locally
    When the user uploads a created file "big-video.mp4" using the webUI
    Then file "big-video.mp4" should not be listed on the webUI
    And the error message with header 'File upload failed…' should be displayed on the webUI
    #And a error message should be displayed on the webUI with the text matching
    #  | /^Not enough free space, you are uploading (\d+(.\d+)?) MB but only (\d+(.\d+)?) MB is left$/ |
