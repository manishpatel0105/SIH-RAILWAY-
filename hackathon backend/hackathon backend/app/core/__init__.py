"""
Core Package — Cross-Cutting Concerns
=======================================

This package contains modules used across the entire application:
  - exceptions.py → Centralized error hierarchy
  - logging.py    → Structured logging configuration

These are NOT business logic. They are infrastructure that
every other layer (API, services, repositories) depends on.
"""
