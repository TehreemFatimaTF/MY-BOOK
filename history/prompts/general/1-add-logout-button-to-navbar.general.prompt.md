---
id: 1
title: Add Logout Button to Navbar
stage: general
date: 2025-12-31
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: 001-book-rag-chatbot
user: user
command: "Add a Logout button to the navbar in docusaurus.config.js. When a user clicks it while reading a book, they should be logged out and redirected to the login page."
labels: ["navbar", "authentication", "logout", "docusaurus"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - src/theme/Navbar/index.js
  - docusaurus.config.js
tests: []
---

## Summary

### Prompt Text
Add a Logout button to the navbar in docusaurus.config.js. When a user clicks it while reading a book, they should be logged out and redirected to the login page.

### Response Text
Added logout functionality to the navbar by updating the custom Navbar component in src/theme/Navbar/index.js. The logout button was already present in the UI, but I enhanced the logout functionality to properly trigger the login modal after logout. The implementation now dispatches a 'showLoginModal' event after the user is logged out, ensuring they are prompted to log in again when reading a book.

### Changes Made

1. Updated src/theme/Navbar/index.js to modify the handleLogout function
2. The function now dispatches a 'showLoginModal' event after successful logout
3. This ensures users are prompted to log in again after logging out while reading a book

### Outcome
The logout button in the navbar now properly logs out the user and triggers the login modal, fulfilling the requirement to redirect users to the login page after logout.