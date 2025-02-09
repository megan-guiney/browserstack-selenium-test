# Browserstack-selenium-test
Basic Browserstack-integrated selenium-python test suite, to be run from jenkins

## Challenge Requirements

- [X] Executes on BrowserStack (you will need to create a free trial)
- The suite must contain a test doing the following:
  - [X] Log into www.bstackdemo.com using these dummy credentials: demouser/testingisfun99
  - [X] Filter the product view to show "Samsung" devices only
  - [X] Favorite the "Galaxy S20+" device by clicking the yellow heart icon
  - [X] Verify that the Galaxy S20+ is listed on the Favorites page
- Run across the following three browsers:
  - [x] Windows 10 Chrome
  - [] macOS Ventura Firefox
  - [] Samsung Galaxy S22
  - [ ] Run in parallel across the 3
- [ ] Be Executed from Jenkins server
- [X] Be uploaded as GitHub Repo
- [ ] Include proof of Jenkins pipeline (screenshots or pipeline code)

# Setup Notes:
- Must be set up in a python 3.8 venv
