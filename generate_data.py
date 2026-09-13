import os
import random
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

def generate_synthetic_sales_data(num_records=1800, output_path="data/sales_data.csv"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    random.seed(42)
    np.random.seed(42)

    categories = {
        "Technology": {
            "Phones": [("Apple iPhone 15 Pro", 999), ("Samsung Galaxy S24", 849), ("Google Pixel 8", 699), ("OnePlus 12", 649)],
            "Laptops": [("MacBook Air M2", 1199), ("Dell XPS 13", 1099), ("Lenovo ThinkPad X1", 1299), ("HP Spectre x360", 999)],
            "Accessories": [("Sony WH-1000XM5 Headphones", 349), ("Logitech MX Master 3S Mouse", 99), ("Keychron K2 Mechanical Keyboard", 89), ("Anker 100W Fast Charger", 59)],
            "Smart Watches": [("Apple Watch Series 9", 399), ("Samsung Galaxy Watch 6", 299), ("Garmin Venu 3", 449)]
        },
        "Furniture": {
            "Chairs": [("Ergonomic Mesh Office Chair", 249), ("Executive Leather Recliner", 399), ("Steelcase Series 1 Task Chair", 499), ("Gaming Bucket Chair", 199)],
            "Desks": [("Motorized Standing Desk 60x30", 549), ("L-Shaped Corner Workstation", 329), ("Minimalist Solid Wood Desk", 419)],
            "Storage": [("3-Drawer Mobile Filing Cabinet", 149), ("Modular Wooden Bookshelf", 189), ("Steel Storage Credenza", 279)],
            "Lighting": [("Architect LED Desk Lamp", 79), ("Ambient Floor Standing Lamp", 119)]
        },
        "Office Supplies": {
            "Paper & Notebooks": [("Moleskine Executive Journal", 24), ("Premium Copy Paper 5-Pack", 39), ("Spiral Dot Grid Notebook Pack", 19)],
            "Stationery": [("Parker Fountain Pen Set", 65), ("Pilot G2 Gel Pens Bulk Pack", 22), ("Sharpie Highlighters Box", 16)],
            "Binders & Organizers": [("Heavy Duty Ring Binders 6-Pack", 29), ("Desktop Acrylic Organizer", 34), ("Cable Management Tray Kit", 25)],
            "Packaging Supplies": [("Bubble Cushion Wrap Roll", 28), ("Heavy Duty Packing Tape 6-Pack", 21)]
        }
    }

    regions_data = {
        "North": ["New York", "Chicago", "Boston", "Detroit", "Minneapolis"],
        "South": ["Atlanta", "Dallas", "Miami", "Houston", "Austin"],
        "East": ["Philadelphia", "Washington D.C.", "Baltimore", "Pittsburgh", "Richmond"],
        "West": ["Los Angeles", "San Francisco", "Seattle", "Denver", "Phoenix"],
        "Central": ["Kansas City", "Indianapolis", "St. Louis", "Columbus", "Nashville"]
    }

    customer_segments = ["Consumer", "Corporate", "Home Office"]
    segment_weights = [0.52, 0.32, 0.16]

    ship_modes = ["Standard Class", "Second Class", "First Class", "Same Day"]
    ship_weights = [0.60, 0.20, 0.15, 0.05]

    payment_modes = ["Credit Card", "UPI / Instant Transfer", "Debit Card", "Net Banking", "Cash on Delivery"]
    payment_weights = [0.45, 0.25, 0.15, 0.10, 0.05]

    first_names = ["Aarav", "Neha", "Rohan", "Priya", "Vikram", "Ananya", "Rahul", "Pooja", "Arjun", "Kavita",
                   "Michael", "Sarah", "David", "Jessica", "James", "Emily", "Daniel", "Sophia", "Alex", "Olivia"]
    last_names = ["Sharma", "Verma", "Patel", "Singh", "Gupta", "Deshmukh", "Chopra", "Reddy", "Mehta", "Iyer",
                  "Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis", "Wilson", "Taylor", "Anderson"]

    customers = []
    for i in range(1, 250):
        c_name = f"{random.choice(first_names)} {random.choice(last_names)}"
        c_id = f"CUST-{1000 + i}"
        c_seg = np.random.choice(customer_segments, p=segment_weights)
        customers.append((c_id, c_name, c_seg))

    start_date = datetime(2024, 1, 1)
    end_date = datetime(2026, 8, 31)
    total_days = (end_date - start_date).days

    records = []

    for i in range(1, num_records + 1):
        order_id = f"ORD-{20240000 + i}"
        
        day_offset = random.randint(0, total_days)
        order_date = start_date + timedelta(days=day_offset)
        
        ship_days = random.choices([1, 2, 3, 4, 5], weights=[0.1, 0.25, 0.4, 0.2, 0.05])[0]
        ship_date = order_date + timedelta(days=ship_days)

        cust_id, cust_name, segment = random.choice(customers)

        region = random.choice(list(regions_data.keys()))
        city = random.choice(regions_data[region])

        category = random.choice(list(categories.keys()))
        sub_category = random.choice(list(categories[category].keys()))
        product_item = random.choice(categories[category][sub_category])
        product_name, base_price = product_item

        quantity = random.choices([1, 2, 3, 4, 5, 8, 10], weights=[0.45, 0.25, 0.15, 0.07, 0.05, 0.02, 0.01])[0]

        if segment == "Corporate" and random.random() > 0.6:
            quantity = random.randint(3, 12)

        discount = round(random.choices([0.0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30], 
                                        weights=[0.40, 0.20, 0.15, 0.12, 0.08, 0.03, 0.02])[0], 2)

        gross_sales = round(base_price * quantity, 2)
        net_sales = round(gross_sales * (1 - discount), 2)

        if category == "Technology":
            cost_factor = random.uniform(0.65, 0.80)
        elif category == "Furniture":
            cost_factor = random.uniform(0.70, 0.88)
        else:
            cost_factor = random.uniform(0.55, 0.75)

        cost_price = base_price * cost_factor
        total_cost = cost_price * quantity
        profit = round(net_sales - total_cost, 2)
        profit_margin = round((profit / net_sales) * 100, 2) if net_sales > 0 else 0.0

        ship_mode = np.random.choice(ship_modes, p=ship_weights)
        payment_mode = np.random.choice(payment_modes, p=payment_weights)

        csat = random.choices([5, 4, 3, 2, 1], weights=[0.60, 0.25, 0.08, 0.05, 0.02])[0]

        records.append({
            "Order_ID": order_id,
            "Order_Date": order_date.strftime("%Y-%m-%d"),
            "Ship_Date": ship_date.strftime("%Y-%m-%d"),
            "Customer_ID": cust_id,
            "Customer_Name": cust_name,
            "Segment": segment,
            "Region": region,
            "City": city,
            "Category": category,
            "Sub_Category": sub_category,
            "Product_Name": product_name,
            "Quantity": quantity,
            "Base_Price": base_price,
            "Discount": discount,
            "Sales": net_sales,
            "Profit": profit,
            "Profit_Margin_Pct": profit_margin,
            "Ship_Mode": ship_mode,
            "Payment_Mode": payment_mode,
            "Rating": csat
        })

    df = pd.DataFrame(records)
    df["Order_Date"] = pd.to_datetime(df["Order_Date"])
    df = df.sort_values(by="Order_Date").reset_index(drop=True)
    df["Order_Date"] = df["Order_Date"].dt.strftime("%Y-%m-%d")

    df.to_csv(output_path, index=False)
    print(f"Successfully generated {len(df)} sales records saved to {output_path}")
    print(f"Date Range: {df['Order_Date'].min()} to {df['Order_Date'].max()}")
    print(f"Total Sales: ${df['Sales'].sum():,.2f} | Total Profit: ${df['Profit'].sum():,.2f}")
    return df

if __name__ == "__main__":
    generate_synthetic_sales_data()
