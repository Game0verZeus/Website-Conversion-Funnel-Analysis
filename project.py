import pandas as pd

# Assuming that the datasets are properly formatted and in the same directory as your script
visits = pd.read_csv('visits.csv', parse_dates=[1])
cart = pd.read_csv('cart.csv', parse_dates=[1])
checkout = pd.read_csv('checkout.csv', parse_dates=[1])
purchase = pd.read_csv('purchase.csv', parse_dates=[1])

# 1. Inspect the DataFrames
print(visits.head())
print(cart.head())
print(checkout.head())
print(purchase.head())

# 2. Combine visits and cart using a left merge
visits_cart = pd.merge(visits, cart, how='left', on='user_id')

# 3. How long is your merged DataFrame
print(len(visits_cart))

# 4. How many of the timestamps are null for the column cart_time?
null_cart_times = visits_cart[visits_cart.cart_time.isnull()].user_id.count()
print(null_cart_times)

# What do these null rows mean?
# These null rows mean that the user visited the website but did not add a t-shirt to their cart.

# 5. What percent of users who visited Cool T-Shirts Inc. ended up not placing a t-shirt in their cart?
percent_no_cart = float(null_cart_times) / len(visits_cart)
print(percent_no_cart)

# 6. Repeat the left merge for cart and checkout and count null values.
cart_checkout = pd.merge(cart, checkout, how='left', on='user_id')
null_checkout_times = cart_checkout[cart_checkout.checkout_time.isnull()].user_id.count()
percent_no_checkout = float(null_checkout_times) / len(cart_checkout)
print(percent_no_checkout)

# 7. Merge all four steps of the funnel
all_data = visits \
    .merge(cart, how='left', on='user_id') \
    .merge(checkout, how='left', on='user_id') \
    .merge(purchase, how='left', on='user_id')

print(all_data.head())

# 8. What percentage of users proceeded to checkout but did not purchase a t-shirt?
null_purchase_times = all_data[(all_data.checkout_time.notnull()) & (all_data.purchase_time.isnull())].user_id.count()
percent_no_purchase = float(null_purchase_times) / len(all_data[all_data.checkout_time.notnull()])
print(percent_no_purchase)

# 9. Which step of the funnel is weakest?
# Based on the percentage calculated in steps 5, 6, and 8, determine the step with the highest percentage.

# 10. Add a column that is the difference between purchase_time and visit_time
all_data['time_to_purchase'] = all_data.purchase_time - all_data.visit_time

# 11. Examine the results
print(all_data.time_to_purchase)

# 12. Calculate the average time to purchase
average_time_to_purchase = all_data.time_to_purchase.mean()
print(average_time_to_purchase)
