Feature: Post-Login Navigation and Incident Filtering on Autoliv Dashboard

  @Updated
  Scenario:
    Given the user has logged into the Autoliv dashboard
    Then the Autoliv logo should be visible at the top left
    When the user clicks the project dropdown
    And selects "AIB" from the list
    Then the "AIB" project should be loaded successfully

  @Updated
  Scenario:Auto liv DashBoard - AIB Project Validation
    Given the user has logged into the Autoliv dashboard
    When the "AIB" project is successfully loaded
    Then the following elements should be visible:
      """
      - Overall Analytics section
      - Overall Distribution section
      """
    Then the Overall Distribution section should show no incidents
    Then the Incident Distribution section should display all safety components



