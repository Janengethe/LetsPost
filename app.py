#!/usr/bin/python3
"""
Module run
Entry point
"""

from posts import app


if __name__ == "__main__":
	app.run(host="0.0.0.0", port="5000", debug=True)