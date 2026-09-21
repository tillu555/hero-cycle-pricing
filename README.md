# Hero Cycles - Bicycle Configuration and Dynamic Pricing System

## Project Overview

This project is a prototype for managing bicycle configurations and dynamic component pricing.

A bicycle consists of multiple components such as frames, brakes, handles, seats, and tyres. The system allows users to select components, enter quantities, maintain historical prices, and automatically calculate the total bicycle price.

The project is designed to replace manual Excel-based configuration and pricing management with a structured application.

## Features

- Component management
- Component type management
- User management
- Historical component price management
- Date-based price lookup
- Quantity validation
- Component availability validation
- Component-wise price calculation
- Total bicycle price calculation
- Bicycle configuration creation
- Configuration finalization
- Automated testing

## Project Structure

```text
hero-cycle-pricing/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   └── services.py
│
├── tests/
│   └── test_pricing.py
│
├── .gitignore
├── README.md
└── requirements.txt
