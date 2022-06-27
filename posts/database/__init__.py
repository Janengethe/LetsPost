#!/usr/bin/env python3
"""Instance of Database Storage"""

from posts.database.engine import DBStorage

storage = DBStorage()
storage.reload()
