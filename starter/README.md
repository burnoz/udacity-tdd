# Udatracker Starter Code

This directory contains the starter code for the Udatracker project. The initial structure of directories and files is described below.

```
.
├── backend
│   ├── __init__.py
│   ├── app.py
│   ├── in_memory_storage.py
│   ├── order_tracker.py
│   ├── requirements.txt
│   └── tests
│       ├── __init__.py
│       ├── test_api.py
│       └── test_order_tracker.py
├── frontend
│   ├── css
│   │   └── style.css
│   ├── index.html
│   └── js
│       └── script.js
├── pytest.ini
└── README.md
```

# Reflection
- During the development of this project, most of the errors that showed after executing the tests were related to mismatches between field names in the tests and the actual implementation of the methods (e.g. item_name vs order_name).
- I had to change many of the api responses to comply with the criteria, I'm used to just returning a short message and a status code, but the tests required a more detailed response with the order details.
- A next step I would take would probably be to add persistent storage to the project so that the orders are not lost when the server is restarted as well as a defined list of items that can be ordered and inventory to allow for items to be out of stock (+ proper validation for this).