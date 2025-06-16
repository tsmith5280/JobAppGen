# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]
- Planned: Job Coach assistant module
- Planned: Matchmaking algorithm based on job and user profiles
- Planned: Smart job recommendation UI integration

## [0.3.0] - 2025-06-05
### Added
- Live data fetching for dashboard components (`StatsOverview`, `ApplicationList`) from the FastAPI backend.
- Centralized backend business logic into a new `core/services` directory, improving separation of concerns.
- A flexible, per-page layout system on the frontend (`getLayout` pattern) to support distinct views for the dashboard, login, and setup pages.

### Changed
- **Refactored `applications` and `profile` modules to use a clean Router-Service pattern, making the API "thin" and the services "thick".**
- **Replaced client-side `localStorage` job saving with a robust backend API call, ensuring data persistence.**
- Reorganized all frontend components into `features/`, `layout/`, and `ui/` directories for improved maintainability and discoverability.
- Standardized all Supabase client interactions in the backend to be consistently `async` and use dependency injection.

### Fixed
- Resolved multiple critical TypeScript errors related to component props and page layouts.
- Corrected `.gitignore` to properly exclude `__pycache__`, `.env`, and other generated files from source control.
- Removed redundant API utility files (`profile_api.py`, `applications_api.py`) after consolidating their logic into the new service layer.

## [0.2.1] - 2025-06-04
### Added
- Resume upload now connects to backend parser with parsed output shown on dashboard
- Manual profile editing supported alongside automatic resume parsing
- Job save functionality stores entries in `localStorage` for demo tracking
- Toast notifications (via Sonner) added for job save confirmation
- Dashboard displays saved job list dynamically with timestamps

### Changed
- Cleaned up `dashboard.tsx` to separate profile, resume, and job logic clearly
- Updated `tsconfig.json` to support `@/core/*` alias resolution for shared logic

### Fixed
- Handled fetch error states for resume parsing and resume generation calls
- Resolved `localStorage` reference crash during SSR by checking `window` existence

## [0.2.0] - ...
## [0.1.0] - ...

---

> 💡 Add new entries above this line as the project progresses.