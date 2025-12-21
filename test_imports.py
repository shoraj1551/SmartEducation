import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

print("Testing Imports...")

try:
    from bson import ObjectId
    print("SUCCESS: from bson import ObjectId")
except ImportError as e:
    print(f"FAILURE: from bson import ObjectId - {e}")
except Exception as e:
    print(f"FAILURE: from bson import ObjectId (Unknown) - {e}")

try:
    from app.services.library_service import LibraryService
    print("SUCCESS: from app.services.library_service import LibraryService")
except ImportError as e:
    print(f"FAILURE: LibraryService Import - {e}")
except Exception as e:
    print(f"FAILURE: LibraryService Import (Unknown) - {e}")

try:
    from app.routes.user_routes import user_bp
    print("SUCCESS: from app.routes.user_routes import user_bp")
except ImportError as e:
    print(f"FAILURE: User Route Import - {e}")
except Exception as e:
    print(f"FAILURE: User Route Import (Unknown) - {e}")
