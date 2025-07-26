import streamlit as st
import json
import os
import uuid

st.set_page_config(page_title="Kirana B2B App")
st.title("🛍️ Kirana B2B Marketplace")

# Create data files if they don't exist
if not os.path.exists("products.json"):
    with open("products.json", "w") as f:
        json.dump([], f)

if not os.path.exists("orders.json"):
    with open("orders.json", "w") as f:
        json.dump([], f)

# Login
role = st.sidebar.selectbox("Login as", ["Distributor", "Kirana Store"])
username = st.sidebar.text_input("Your Name")

if st.sidebar.button("Login"):
    if username:
        st.session_state["username"] = username
        st.session_state["role"] = role
        st.experimental_rerun()

# Dashboard
if "username" in st.session_state:
    username = st.session_state["username"]
    role = st.session_state["role"]

    st.sidebar.success(f"Logged in as {username} ({role})")

    if role == "Distributor":
        st.header("📦 Distributor Dashboard")
        name = st.text_input("Product Name")
        price = st.number_input("Price", min_value=1)
        qty = st.number_input("Quantity", min_value=1)

        if st.button("Add Product"):
            with open("products.json", "r") as f:
                products = json.load(f)

            new_product = {
                "id": str(uuid.uuid4()),
                "name": name,
                "price": price,
                "qty": qty,
                "distributor": username
            }

            products.append(new_product)

            with open("products.json", "w") as f:
                json.dump(products, f, indent=4)

            st.success("Product added.")

    elif role == "Kirana Store":
        st.header("🛒 Kirana Store Dashboard")

        with open("products.json", "r") as f:
            products = json.load(f)

        for p in products:
            st.write(f"{p['name']} - ₹{p['price']} (Qty: {p['qty']})")
            if st.button(f"Order {p['name']}", key=p["id"]):
                with open("orders.json", "r") as f:
                    orders = json.load(f)

                orders.append({
                    "buyer": username,
                    "product": p["name"],
                    "price": p["price"]
                })

                with open("orders.json", "w") as f:
                    json.dump(orders, f, indent=4)

                st.success("Order placed successfully.")
