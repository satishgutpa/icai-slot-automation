# ICAI Course Slot Automation

Python + Playwright automation system that automatically monitors ICAI AICA Level-2 course slots and sends intelligent consolidated email alerts when seats become available.

---

## Project Objective

This project was built to automate manual monitoring of ICAI AI course registration slots.

The system automatically:

- checks ICAI course pages every 30 minutes
- filters preferred locations
- validates actual seat availability
- ignores invalid/closed registrations
- sends email alerts automatically

---

## Features

✅ Monitors ICAI course registration portal automatically

✅ Filters only Offline batches

✅ Supports preferred locations like:
- Delhi
- Gurgaon
- Gurugram
- Faridabad
- Jaipur
- Jalandhar

✅ Opens individual course detail pages

✅ Validates actual available seats

✅ Avoids false alerts from “Registration Closed” overlays

✅ Sends only ONE consolidated email alert per day

✅ Runs silently in background using Windows Task Scheduler

✅ Fully customizable for other automation workflows

---

## Tech Stack

- Python
- Playwright
- Gmail SMTP
- Windows Task Scheduler

---

## Automation Workflow

Website → Automation → Filtering → Seat Validation → Decision Logic → Email Alert

---

## Installation

### 1. Install Python

Download Python:
https://www.python.org/downloads/

---

### 2. Install Required Libraries

Run:

```bash
pip install playwright
