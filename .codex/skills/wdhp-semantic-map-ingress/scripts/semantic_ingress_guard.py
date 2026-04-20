from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.legacy_semantic_map.semantic_ingress_guard import main


if __name__ == "__main__":
    main()
