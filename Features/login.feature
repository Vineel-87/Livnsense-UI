Feature: Vicas Login Functionality Testing.

  @Tester
  Scenario:Login page Loads with required UI elements
    Given the user navigates to the VICAS login page
    Then the heading "Welcome to VICAS" should be displayed
    And the username input field should be visible
    And the Sign In button should be visible and disabled

  @Tester
  Scenario: Sign In button is enabled only when both username and password are entered
    Given the user is on the login page
    When the user enters a valid username in the username field
    And user enters a valid password in the password field
    Then Sign In button should bLoe enabled


  @Tester
  Scenario: Login attempt with multiple credentials from CSV file
     Given the user is on the login page
     When the user reads username and password combinations from "credentials.csv"
     Then the system should attempt to log in with each set
     And verify whether login is successful or shows an error