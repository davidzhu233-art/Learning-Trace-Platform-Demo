# 学迹通 Learning Trace Platform

A web-based learning analytics dashboard that transforms raw quiz response data into actionable insights — for both teachers and students.

## The Problem

Most learning analytics tools focus on teachers. Student-facing dashboards typically show performance scores but leave students with **data and no direction**. Learning Trace Platform bridges this gap by giving both teachers and students meaningful, actionable feedback.

## What It Does

Upload a CSV of student quiz responses and the platform generates two dedicated portals:

**Teacher Portal**
- Visual charts and heatmaps of class-wide and individual performance
- Identifies at-risk students based on learning data
- Enables timely intervention before students fall behind
- AI-generated teaching strategies tailored to class performance patterns

**Student Portal**
- Helps students recognise their own at-risk status
- Explains contributing factors behind their performance
- Provides clear, encouraging steps to improve
- AI-generated personalised learning suggestions

## AI Feedback Engine

Integrated **DeepSeek LLM** to generate teaching strategies and learning suggestions for both portals. Prompt design is grounded in Ryan et al. (2021), prioritising:
- Task-focused feedback
- Comparison with students' own prior progress
- Clear and encouraging actionable steps

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python |
| Frontend / Dashboard | Streamlit |
| Data Visualisation | Plotly |
| AI Feedback | DeepSeek LLM API |
| Data Input | CSV (item-level quiz response logs) |

## Screenshots

*(Coming soon)*

## Academic Context

Developed as part of **TDLL7355 — AI-Powered Learning Analytics System Design Workshop**, MSc Technology, Design and Leadership for Learning, The University of Hong Kong (HKU), March 2026.

## References

Ryan, R. M., et al. (2021). Feedback framework applied to AI-generated instructional recommendations and student encouragement.
