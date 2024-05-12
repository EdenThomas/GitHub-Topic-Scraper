import os
import time

def extract_star_count(repo_stars):
    repo_stars = repo_stars.strip()
    if repo_stars[-1] == 'k':
        return int(float(repo_stars[:-1]) * 1000)
    return int(repo_stars)

def file_needs_update(filepath, days=7):
    if not os.path.exists(filepath):
        return True
    last_modified = os.path.getmtime(filepath)
    return (time.time() - last_modified) / 86400 > days