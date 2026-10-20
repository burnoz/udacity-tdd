import pytest
from unittest.mock import Mock
from ..order_tracker import OrderTracker

# --- Fixtures for Unit Tests ---

@pytest.fixture
def mock_storage():
    """
    Provides a mock storage object for tests.
    This mock will be configured to simulate various storage behaviors.
    """
    mock = Mock()
    # By default, mock get_order to return None (no order found)
    mock.get_order.return_value = None
    # By default, mock get_all_orders to return an empty dict
    mock.get_all_orders.return_value = {}
    return mock

@pytest.fixture
def order_tracker(mock_storage):
    """
    Provides an OrderTracker instance initialized with the mock_storage.
    """
    return OrderTracker(mock_storage)

#
# --- TODO: add test functions below this line ---
#

# Provided tests
def test_add_order_successfully(order_tracker, mock_storage):
    order_tracker.add_order("ORD001", "Laptop", 1, "CUST001")
    
    mock_storage.save_order.assert_called_once_with(
        "ORD001",
        {
            "order_id": "ORD001",
            "item_name": "Laptop",
            "quantity": 1,
            "customer_id": "CUST001",
            "status": "pending",
        },
    )

def test_add_order_raises_error_if_exists(order_tracker, mock_storage):
    """Tests that adding an order with a duplicate ID raises a ValueError."""
    # Simulate that the storage finds an existing order
    mock_storage.get_order.return_value = {"order_id": "ORD_EXISTING"}

    with pytest.raises(ValueError, match="Order with ID 'ORD_EXISTING' already exists."):
        order_tracker.add_order("ORD_EXISTING", "New Item", 1, "CUST001")


# get_order_by_id tests
def test_get_order_id_successfully(order_tracker, mock_storage):
    """Tests fetching an existing order by its ID."""
    # Simulate that the storage finds an existing order
    mock_storage.get_order.return_value = {"order_id": "ORD001", "item_name": "Laptop", "quantity": 1, "customer_id": "CUST001", "status": "pending"}

    order = order_tracker.get_order_by_id("ORD001")
    assert order["order_id"] == "ORD001"
    assert order["item_name"] == "Laptop"
    assert order["quantity"] == 1
    assert order["customer_id"] == "CUST001"
    assert order["status"] == "pending"

def test_get_order_id_not_found(order_tracker, mock_storage):
    """Tests that fetching a non-existent order ID returns None."""
    # Simulate that the storage does not find the order
    mock_storage.get_order.return_value = None

    order = order_tracker.get_order_by_id("ORD_NON_EXISTENT")
    assert order is None


# update_order_status tests
def test_update_order_status_successfully(order_tracker, mock_storage):
    """Tests updating the status of an existing order."""
    # Simulate that the storage finds an existing order
    mock_storage.get_order.return_value = {"order_id": "ORD001", "item_name": "Laptop", "quantity": 1, "customer_id": "CUST001", "status": "pending"}

    order_tracker.update_order_status("ORD001", "shipped")

    mock_storage.save_order.assert_called_once_with(
        "ORD001",
        {
            "order_id": "ORD001",
            "item_name": "Laptop",
            "quantity": 1,
            "customer_id": "CUST001",
            "status": "shipped",
        },
    )

def test_update_order_status_not_found(order_tracker, mock_storage):
    """Tests that updating the status of a non-existent order raises a ValueError."""
    # Simulate that the storage does not find the order
    mock_storage.get_order.return_value = None

    with pytest.raises(ValueError, match="Order with ID ORD_NON_EXISTENT not found."):
        order_tracker.update_order_status("ORD_NON_EXISTENT", "shipped")

def test_update_order_status_rejects_invalid_status(order_tracker, mock_storage):
    with pytest.raises(ValueError, match="Status must be pending, processing, or shipped."):
        order_tracker.update_order_status("ORD001", "invalid")


# list_all_orders tests
def test_list_all_orders_successfully(order_tracker, mock_storage):
    """Tests listing all current orders."""
    # Simulate that the storage returns a list of orders
    mock_storage.get_all_orders.return_value = [
        {"order_id": "ORD001", "item_name": "Laptop", "quantity": 1, "customer_id": "CUST001", "status": "pending"},
        {"order_id": "ORD002", "item_name": "Phone", "quantity": 2, "customer_id": "CUST002", "status": "shipped"}
    ]

    orders = order_tracker.list_all_orders()
    assert len(orders) == 2
    assert orders[0]["order_id"] == "ORD001"
    assert orders[1]["order_id"] == "ORD002"


# list_orders_by_status tests
def test_list_orders_by_status_successfully(order_tracker, mock_storage):
    """Tests listing orders filtered by a specific status."""
    # Simulate that the storage returns a list of orders
    mock_storage.get_all_orders.return_value = [
        {"order_id": "ORD001", "item_name": "Laptop", "quantity": 1, "customer_id": "CUST001", "status": "pending"},
        {"order_id": "ORD002", "item_name": "Phone", "quantity": 2, "customer_id": "CUST002", "status": "shipped"},
        {"order_id": "ORD003", "item_name": "Tablet", "quantity": 1, "customer_id": "CUST003", "status": "shipped"}
    ]

    shipped_orders = order_tracker.list_orders_by_status("shipped")
    assert len(shipped_orders) == 2
    assert all(order["status"] == "shipped" for order in shipped_orders)