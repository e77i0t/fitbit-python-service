Feature: Grab a user's data from the FitBit API

@smoke @regression
Scenario Outline: Successfully pull user health data for the first time
    Given I have a valid token for a user
    When I request the most recent health data
    Then I should be able to get the most recent profile data
    And I should be able to get the most recent user general activities data
    And I should be able to get the most recent user detailed activities data
    And I should be able to get the most recent user detailed activities data
    And I should update the run history
    And I should create data files with the latest run history

Scenario Outline: Successfully pull user health data, multiple times
    Given I have a valid token for a user
    When I request the most recent health data
    Then I should be able to get the most recent profile data
    And I should be able to get the most recent user general activities data
    And I should be able to get the most recent user detailed activities data
    And I should be able to get the most recent user detailed activities data
    And I should update the run history
    And I should create data files with the latest run history

Scenario Outline: Gracefully handle Fitbit Rate Limiting
    Given I have a valid token for a user
    When I request the most recent health data
    Then I should be able to get the most recent profile data
    And I should be able to get the most recent user general activities data
    And I should be able to get the most recent user detailed activities data
    And I should be able to get the most recent user detailed activities data
    And I should update the run history
    And I should create data files with the latest run history

Scenario Outline: Gracefully handle Fitbit API Errors
    Given I have a valid token for a user
    When I request the most recent health data
    Then I should be able to get the most recent profile data
    And I should be able to get the most recent user general activities data
    And I should be able to get the most recent user detailed activities data
    And I should be able to get the most recent user detailed activities data
    And I should update the run history
    And I should create data files with the latest run history
