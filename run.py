#!/usr/bin/env python
from address_app.app import create_app

if __name__ == "__main__":
    app = create_app(db_name='address_book', testing=False)

    app.run(debug=True)
