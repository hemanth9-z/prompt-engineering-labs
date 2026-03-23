import asyncio
from openai import OpenAI

# 🔑 CONFIG
client = OpenAI(
    api_key="<<<<put-your-key-here>>>>",
    base_url="https://models.inference.ai.azure.com"
)

MODEL = "gpt-4o"
# 👉 Import tools locally (stable)
from server import get_inventory_levels, get_weekly_sales


async def run_client():
    print("🚀 MCP (local agent mode) started")
    print("Available tools: get_inventory_levels, get_weekly_sales")

    # 🧠 Strong system prompt
    system_prompt = """
You are an intelligent inventory assistant.

You have access to:
- get_inventory_levels
- get_weekly_sales

Rules:
- If inventory < 10 and weekly sales > 15 → RESTOCK
- If inventory > 20 and weekly sales < 5 → CLEARANCE

IMPORTANT:
- For restocking questions → ALWAYS use BOTH tools
- You may call multiple tools before answering
- DO NOT stop until you have enough data

Tool format:
CALL_TOOL: get_inventory_levels

When you are ready, give a FINAL answer in plain English.
DO NOT call tools after final answer.
"""

    while True:
        user_input = input("\nUSER: ").strip()

        if user_input.lower() == "quit":
            print("👋 Exiting...")
            break

        print("🧠 Thinking...")

        # First model call
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

        # 🔁 AGENT LOOP (multi-tool support)
        while "CALL_TOOL:" in reply:
            tool_name = reply.split("CALL_TOOL:")[1].strip().split()[0]

            if tool_name == "get_inventory_levels":
                data = get_inventory_levels()
            elif tool_name == "get_weekly_sales":
                data = get_weekly_sales()
            else:
                print("❌ Unknown tool:", tool_name)
                break

            print(f"\n🔧 Calling {tool_name}")
            print("📊 TOOL RESULT:", data)

            tool_history.append(f"{tool_name}: {data}")

            # Feed ALL previous tool results
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

If more data is needed, call another tool.
Otherwise, give FINAL answer with recommendations.
"""
                    }
                ]
            )

            reply = response.choices[0].message.content.strip()
            print("\nMODEL:", reply)

        # ✅ FINAL ANSWER (only when no tool call)
        print("\n✅ FINAL ANSWER:\n", reply)


# ▶️ Run
if __name__ == "__main__":
    asyncio.run(run_client())