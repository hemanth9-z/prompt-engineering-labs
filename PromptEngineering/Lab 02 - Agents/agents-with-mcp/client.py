import asyncio
from openai import OpenAI

# 🔑 CONFIG
client = OpenAI(
    api_key="<<<put-your-key-here>>>",
    base_url="https://models.inference.ai.azure.com"
)

MODEL = "gpt-4o"

# ✅ Import NEW tools
from server import (
    get_inventory,
    get_sales,
    get_revenue_per_product,
    get_total_revenue,
    get_top_products,
    get_low_stock_products,
    get_restock_recommendations,
    get_clearance_products
)


async def run_client():
    print("🚀 Advanced Inventory Agent Started")

    system_prompt = """
You are a smart business analytics assistant.

Available tools:
- get_inventory
- get_sales
- get_revenue_per_product
- get_total_revenue
- get_top_products
- get_low_stock_products
- get_restock_recommendations
- get_clearance_products

Rules:
- Use tools when needed
- You can call multiple tools
- Combine results intelligently
- Always give business insights

Tool format:
CALL_TOOL: tool_name

When ready, give final answer.
"""

    while True:
        user_input = input("\nUSER: ")

        if user_input.lower() == "quit":
            break

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ]
        )

        reply = response.choices[0].message.content.strip()
        print("\nMODEL:", reply)

        tool_history = []

        # 🔁 Multi-tool loop
        while "CALL_TOOL:" in reply:
            tool_name = reply.split("CALL_TOOL:")[1].strip().split()[0]

            print(f"\n🔧 Calling {tool_name}")

            # Tool mapping
            if tool_name == "get_inventory":
                data = get_inventory()

            elif tool_name == "get_sales":
                data = get_sales()

            elif tool_name == "get_revenue_per_product":
                data = get_revenue_per_product()

            elif tool_name == "get_total_revenue":
                data = get_total_revenue()

            elif tool_name == "get_top_products":
                data = get_top_products()

            elif tool_name == "get_low_stock_products":
                data = get_low_stock_products()

            elif tool_name == "get_restock_recommendations":
                data = get_restock_recommendations()

            elif tool_name == "get_clearance_products":
                data = get_clearance_products()

            else:
                print("❌ Unknown tool:", tool_name)
                break

            print("📊 TOOL RESULT:", data)

            tool_history.append(f"{tool_name}: {data}")

            # Send back to model
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input},
                    {"role": "assistant", "content": reply},
                    {
                        "role": "user",
                        "content": f"""
Tool results so far:
{chr(10).join(tool_history)}

If more data needed → call another tool.
Else → give final answer with insights.
"""
                    }
                ]
            )

            reply = response.choices[0].message.content.strip()
            print("\nMODEL:", reply)

        print("\n✅ FINAL ANSWER:\n", reply)


if __name__ == "__main__":
    asyncio.run(run_client())