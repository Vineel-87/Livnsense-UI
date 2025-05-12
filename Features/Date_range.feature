Feature:Incident Date Range Filtering


  Background:
    Given I am viewing the Autoliv incident Dashboard

  @Tested
  Scenario:
    When I open the calender icon selection dialog
    Then I should see the time period options:


  Scenario: Verify default date range selection
    When I open the calendar icon selection dialog
    Then I should see "Today" option selected by default
    And the date input field should display today's date










