from config import app
from staff_controller import *

## master routes ##
# Staff Login
app.add_url_rule('/admin', view_func=admin)
app.add_url_rule('/staff', view_func=staff)
app.add_url_rule('/staff/login', view_func=staff_login, methods=["POST"])

# Kitchen Staff Dashboard

# Admin Dashboard
app.add_url_rule('/admin/nav', view_func=admin_nav)
app.add_url_rule('/admin/logout', view_func=admin_logout)
app.add_url_rule('/admin/dash', view_func=admin_dash)
app.add_url_rule('/admin/account', view_func=admin_acc)
app.add_url_rule('/account/edit', view_func=admin_edit)
app.add_url_rule('/admin/create_topping', view_func=create_topping,methods=["POST"])
app.add_url_rule('/admin/update_topping', view_func=update_topping,methods=["POST"])
app.add_url_rule('/admin/create_size', view_func=create_size,methods=["POST"])
app.add_url_rule('/admin/update_size', view_func=update_size,methods=["POST"])
app.add_url_rule('/admin/create_style', view_func=create_style,methods=["POST"])
app.add_url_rule('/admin/update_style', view_func=update_style,methods=["POST"])
app.add_url_rule('/admin/create_order_type', view_func=create_order_type,methods=["POST"])
app.add_url_rule('/admin/update_order_type',view_func=update_order_type,methods=["POST"])

app.add_url_rule('/store/logout', view_func=store_logout)
app.add_url_rule('/store', view_func=store)
