from ninja_extra import NinjaExtraAPI

api = NinjaExtraAPI(
    title="Book Store API",
    description="Book Store API for renting books and notifying available/returned books in a store",
    urls_namespace="store",
)
api.auto_discover_controllers()
