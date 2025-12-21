# SmartEducation - E2E Testing Bug Log

This file tracks bugs found during E2E testing on the refactored `refactor/base-optimization` branch.

| ID | Feature | Description | Status | Fix Details |
|----|---------|-------------|--------|-------------|
| 1  | Frontend | Asset paths with query strings (e.g. `?v=4`) were not updated during refactor, causing 404s. | Fixed | Updated regex in replacement command to handle optional query strings. |
| 2  | Frontend | Double pathing in CSS URLs (`/static/css//static/css/styles.css`) due to malformed regex replacement. | Fixed | Applied corrected regex to cleanup malformed paths in all HTML templates. |
| 3  | Backend | 500 Error on Registration: `OTP` model missing `user_id` and `purpose` fields. | Fixed | Added missing fields to `OTP` class in `app/models.py`. |
| 4  | Frontend | Hardcoded `API_BASE_URL` in `script.js`. | Fixed | Changed to relative `/api`. |
| 5  | Frontend | FontAwesome CDN links broken by incorrect prefixing. | Fixed | Restored CDN URLs in all HTML templates. |
