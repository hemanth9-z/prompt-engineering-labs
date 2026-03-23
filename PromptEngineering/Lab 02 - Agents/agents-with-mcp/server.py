import pandas as pd
from mcp.server.fastmcp import FastMCP

# ==============================
# 🚀 MCP SERVER
# ==============================

mcp = FastMCP("Inventory-Analytics")

# ==============================
# 📂 LOAD DATA
# ==============================

try:
    inventory_df = pd.read_csv("inventory.csv")
    sales_df = pd.read_csv("sales.csv")

    # Merge datasets
    df = pd.merge(inventory_df, sales_df, on="Product")

    print("✅ Data loaded successfully")

except Exception as e:
    print("❌ Error loading CSV files:", e)
    df = pd.DataFrame()


# ==============================
# 📦 TOOL 1: Inventory
# ==============================

@mcp.tool()
def get_inventory() -> dict:
    """Returns stock levels for all products"""
    return df.set_index("Product")["Stock"].to_dict()


# ==============================
# 📊 TOOL 2: Sales
# ==============================

@mcp.tool()
def get_sales() -> dict:
    """Returns units sold per product"""
    return df.set_index("Product")["Units_Sold"].to_dict()


# ==============================
# 💰 TOOL 3: Revenue per product
# ==============================

@mcp.tool()
def get_revenue_per_product() -> dict:
    """Returns revenue per product"""
    temp = df.copy()
    temp["Revenue"] = temp["Price"] * temp["Units_Sold"]
    return temp.set_index("Product")["Revenue"].to_dict()


# ==============================
# 📈 TOOL 4: Total revenue
# ==============================

@mcp.tool()
def get_total_revenue() -> float:
    """Returns total revenue for the week"""
    temp = df.copy()
    temp["Revenue"] = temp["Price"] * temp["Units_Sold"]
    return float(temp["Revenue"].sum())


# ==============================
# 🏆 TOOL 5: Top selling products
# ==============================

@mcp.tool()
def get_top_products() -> list:
    """Returns top 3 selling products"""
    temp = df.sort_values(by="Units_Sold", ascending=False)
    return temp["Product"].head(3).tolist()


# ==============================
# 🚨 TOOL 6: Low stock products
# ==============================

@mcp.tool()
def get_low_stock_products() -> list:
    """Returns products with low inventory (<10)"""
    temp = df[df["Stock"] < 10]
    return temp["Product"].tolist()


# ==============================
# 💡 TOOL 7: Restock recommendations
# ==============================

@mcp.tool()
def get_restock_recommendations() -> list:
    """Returns products that need restocking"""
    temp = df[(df["Stock"] < 10) & (df["Units_Sold"] > 10)]
    return temp["Product"].tolist()


# ==============================
# 🔥 TOOL 8: Clearance recommendations
# ==============================

@mcp.tool()
def get_clearance_products() -> list:
    """Returns products that should go on clearance"""
    temp = df[(df["Stock"] > 20) & (df["Units_Sold"] < 5)]
    return temp["Product"].tolist()


# ==============================
# ▶️ RUN SERVER
# ==============================

if __name__ == "__main__":
    print("🚀 MCP Analytics Server Running...")
    mcp.run()