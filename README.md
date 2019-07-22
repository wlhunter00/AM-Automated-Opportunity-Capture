# AM Automated Opportunity Capture
## Introduction
This is the automated oppourtunity hunter for Alvarez and Marsal's Forensic Technology Services team.
The tool will go out to sites requested by the team, and will scrape information about various
RFPs, RFIs, networking events, and various other opportunities that could result in more projects for the team. After this information is scraped, it is stored in a SQL database, and then a daily report
on the tools findings will be emailed to the team.

#### Process
1. Scrape all RFP sites using the Python library BeautifulSoup.
2. Insert this data into a raw SQL table.
3. Scrape all event sites using their API through python.
4. Insert this data into a raw SQL table.
5. Clean the invidual tables using SQL queries.
6. Insert all indivdual sites into master table and current table.
7. Using Pandas take SQL queries and insert the data in dataframe.
8. Export the dataframes into excel sheets.
9. Attach the excel sheet and email the team the results using Yagmail and HMTL.

## Table of Contents
* [Project Status](#project-status)
  * [To Do](#to-do)
* [Introduction](#introduction)
* [Technologies](#technologies)
* [Installation](#installation)
* [Walkthrough](#Walkthrough)
  * [File Walkthrough](#file-walkthrough)
  * [Functions Walkthrough](#functions-walkthrough)
* [Adding a Site](#adding-a-site)
* [Typical Errors](#typical-errors)

## Project Status
###### **Version 1.2**

Stable build is currently ready. Automated reports sent out daily. Functionality is currently being expanded on.

###### **Recently Added**
Added scraped events from Eventbrite to the daily report.

#### To Do:
- [ ] Correctly spell Opportunity everywhere.
- [ ] Look to implement dictionaries.
- [ ] Make sure there aren't uneeded loops in main script.
- [ ] Scrape 10Times.com using infinite scrolling.
- [ ] Use FBO.gov's API to scrape their RFPs.
- [ ] Create this README.
- [ ] Create Presentation.

## Technologies
Project was created with:
- Python Version: 3.6
  - BeautifulSoup
  - Pyodbc
  - Pandas
  - Yagmail
  - Requests
- Microsoft SQL Server
- HTML

## Installation

## Walkthrough

#### File Walkthrough:

#### Functions Walkthrough:

## Adding a Site

## Typical Errors
