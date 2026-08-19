"""Build every page into the local WordPress DB, then refresh the snapshot."""
import runpy, os
here = os.path.dirname(__file__)
for m in ("build_home", "build_students", "build_companies", "build_secondary", "build_extra", "build_jobs", "build_preview"):
    print(f"→ {m}")
    runpy.run_path(os.path.join(here, m + ".py"), run_name="__main__")
print("done.")
