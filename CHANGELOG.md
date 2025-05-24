# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]
- Planned: Job Coach assistant module
- Planned: Matchmaking algorithm based on job and user profiles
- Planned: Smart job recommendation UI integration

## [0.2.0] - 2025-05-24
### Added
- Full backend restructuring under `backend/` with `core/`, `routers/`, `static/`, and environment separation
- RESTful API routes for `/profile`, `/resume`, `/applications` via FastAPI
- Joblight frontend scaffolded with Next.js, Tailwind CSS, and TypeScript
- Global theme with warm amber and teal color tokens
- Initial `dashboard.tsx` page and `Layout` component system
- `.env` configuration handled securely in backend
- Git hygiene enforced via improved `.gitignore` covering `.env`, build outputs, and dependency caches

### Changed
- Removed all remaining Streamlit dependencies, session logic, and UI calls
- Migrated state/profile persistence logic from `session.py` to Supabase + REST-based calls
- Split `main.py` into modular route handlers and helper services

### Fixed
- Corrected session-based profile fallback to dynamic user authentication
- Resolved broken state calls in former Streamlit logic by removing `st.session_state`
- Eliminated circular imports in `core/utils/` by flattening logic

## [0.1.0] - 2025-05-23
### Added
- Initial application structure and file organization
- User authentication via Supabase (`auth.py`, `auth_header.py`)
- Resume upload and parsing flow (`resume_parser.py`, `main.py`, `profile_api.py`)
- Application tracker UI and logic (`1_Tracker.py`, `applications_api.py`, `tracker_view.py`)
- Resume & cover letter generator interface (`2_Resume_and_Cover.py`, `resume_cover.py`, `generator.py`)
- Profile upload gating logic via dynamic user IDs
- SQL policies for RLS: insert/view/update/delete protections for `applications` and `user_profile`
- Foreign key relationships: `user_profile.user_id` → `auth.users.id`

### Changed
- Updated `user_profile.skills` to use `text[]` array for advanced filtering
- Enhanced database constraints for safer cross-table integrity
- Modularized UI with `core/ui/` and logic separation in `core/utils/`

### Fixed
- Removed fallback test `user_id` from tracker in favor of dynamic session-based ID

---

> 💡 Add new entries above this line as the project progresses.
