"""
Temperature Playground — AI for Product Managers
Same prompt at 5 temperatures. See creativity vs consistency.
"""

import gradio as gr
import os

# ── Cached Responses ──────────────────────────────────────────────────────────
# 3 prompts × 5 temperatures × 3 responses each

CACHED = {
    "Write a one-sentence product description for noise-canceling headphones.": {
        0.0: [
            "Experience crystal-clear audio with our premium noise-canceling headphones, designed to block out distractions and deliver immersive sound quality.",
            "Experience crystal-clear audio with our premium noise-canceling headphones, designed to block out distractions and deliver immersive sound quality.",
            "Experience crystal-clear audio with our premium noise-canceling headphones, designed to block out distractions and deliver immersive sound quality.",
        ],
        0.3: [
            "Experience crystal-clear audio with our premium noise-canceling headphones, engineered to block distractions and deliver immersive sound.",
            "Enjoy uninterrupted, immersive audio with our premium noise-canceling headphones that block out the world around you.",
            "Experience pristine audio quality with our noise-canceling headphones, designed to eliminate distractions and deliver pure sound.",
        ],
        0.7: [
            "Block the world out and tune into pure, uninterrupted sound with our advanced noise-canceling headphones.",
            "Your personal sound sanctuary — our noise-canceling headphones transform any environment into your private listening room.",
            "From busy commutes to open offices, our noise-canceling headphones create a cocoon of crystal-clear audio wherever you go.",
        ],
        1.0: [
            "Silence becomes your superpower — these headphones don't just cancel noise, they create your personal concert hall anywhere in the world.",
            "Wrap yourself in a blanket of pure sound while the chaos of the world melts away with our revolutionary noise-canceling technology.",
            "Imagine pressing pause on every sound except the one you chose — that's the magic of our noise-canceling headphones.",
        ],
        1.5: [
            "Your ears deserve a vacation from reality — step into a dimension where only music exists and the noisy universe respectfully shuts up.",
            "Like a force field made of silence and bass drops, these headphones banish noise to the shadow realm while your playlist ascends.",
            "Noise-canceling? More like reality-editing earphones that rewrite the sonic script of your entire existence in high fidelity.",
        ],
    },
    "Write a customer support reply to someone whose order is late.": {
        0.0: [
            "I sincerely apologize for the delay with your order. I've looked into this and can see it's currently in transit. I'm escalating this to our shipping team for priority handling, and I'll send you an updated tracking link within the next 2 hours. Thank you for your patience.",
            "I sincerely apologize for the delay with your order. I've looked into this and can see it's currently in transit. I'm escalating this to our shipping team for priority handling, and I'll send you an updated tracking link within the next 2 hours. Thank you for your patience.",
            "I sincerely apologize for the delay with your order. I've looked into this and can see it's currently in transit. I'm escalating this to our shipping team for priority handling, and I'll send you an updated tracking link within the next 2 hours. Thank you for your patience.",
        ],
        0.3: [
            "I sincerely apologize for the delay with your order. I've looked into this and can see it's in transit. I'm escalating to our shipping team for priority handling and will send an updated tracking link within 2 hours.",
            "I'm sorry for the inconvenience with your delayed order. I've checked the status and am escalating this for priority handling. You'll receive an updated tracking link within the next 2 hours.",
            "I apologize for the delay with your order. I've reviewed your shipment status and am prioritizing this with our logistics team. Expect an updated tracking link within 2 hours.",
        ],
        0.7: [
            "I'm really sorry about the delay — I know how frustrating that is. I've flagged your order for priority handling and our shipping team is on it. I'll personally follow up with an updated tracking link within the next couple of hours.",
            "Thank you for reaching out, and I apologize for the wait. I've just escalated your order to our express handling team. You should see movement on your tracking within 24 hours, and I'll check back with you personally.",
            "I completely understand your frustration with this delay. I want to make this right — I've pushed your order to the front of the queue and I'm adding a 15% credit to your account for the inconvenience.",
        ],
        1.0: [
            "Oh no, that's definitely not the experience we want you to have! I've grabbed your order details and I'm personally making sure it gets fast-tracked. Expect an update from me within the hour — and I'm throwing in free express shipping on your next order as a 'sorry about that!'",
            "I hear you, and you have every right to be frustrated. Here's what I'm doing right now: 1) Pinging the warehouse directly, 2) Upgrading your shipping to priority, 3) Adding a $10 credit because waiting is the worst. I'll be back with tracking details shortly.",
            "First off — I'm sorry. Late orders are no fun. I've already escalated this to our shipping ninja team (yes, that's their real name) and they're tracking down your package as we speak. Hang tight, update incoming within the hour!",
        ],
        1.5: [
            "Okay so your order went on an unauthorized vacation and WE ARE NOT HAPPY ABOUT IT EITHER. I've deployed our top package-hunting agents and attached a GPS satellite to your shipment metaphorically. Free stuff incoming to apologize for this adventure your order decided to have!",
            "Your package appears to have gotten lost in the narrative arc of its own hero's journey but I'm writing the ending where it arrives YESTERDAY. Escalating with the fury of a thousand customer service reps. Stand by for redemption!",
            "I apologize profusely in seventeen languages! Your order has been given a stern talking-to and is now being escorted by our finest courier pigeons. But seriously — I've flagged it for emergency delivery and you're getting a surprise discount because this is ridiculous.",
        ],
    },
    "Explain what an API is to a non-technical person in 2 sentences.": {
        0.0: [
            "An API is like a waiter in a restaurant — it takes your request to the kitchen (another software system) and brings back what you ordered. It's the standard way different software applications communicate with each other without needing to know how each one works internally.",
            "An API is like a waiter in a restaurant — it takes your request to the kitchen (another software system) and brings back what you ordered. It's the standard way different software applications communicate with each other without needing to know how each one works internally.",
            "An API is like a waiter in a restaurant — it takes your request to the kitchen (another software system) and brings back what you ordered. It's the standard way different software applications communicate with each other without needing to know how each one works internally.",
        ],
        0.3: [
            "An API is like a waiter in a restaurant — it takes your request to the kitchen (another system) and brings back what you ordered. It lets different software talk to each other without needing to know how the other works.",
            "An API acts as a messenger between different software systems, carrying requests and responses back and forth. Think of it like a universal translator that lets apps communicate even if they're built completely differently.",
            "An API is a set of rules that lets two pieces of software talk to each other — like a common language between apps. When you check the weather on your phone, an API is fetching that data from a weather service behind the scenes.",
        ],
        0.7: [
            "Think of an API like a power outlet in your wall — you don't need to understand the electrical grid to plug in your phone and charge it. Similarly, an API lets one piece of software use another's capabilities without knowing (or caring) how it works under the hood.",
            "An API is basically a menu at a restaurant — it shows you what you can order (data or services) and how to ask for it, without requiring you to go into the kitchen yourself. Every time you use an app that pulls in data from somewhere else, an API is the invisible go-between making it happen.",
            "Imagine you're at a drive-through window — you speak into the box, and food magically appears without you entering the kitchen. An API works the same way: it's the window between two software systems, letting them exchange information through a simple, standardized conversation.",
        ],
        1.0: [
            "Picture two people who speak different languages sitting in a room with a brilliant interpreter between them — that interpreter is the API, translating requests and responses so both sides understand each other perfectly. In the tech world, this invisible translator is why your weather app knows tomorrow's forecast and your banking app knows your balance.",
            "An API is like a diplomatic embassy between two software countries — it has strict protocols for what information can be requested and shared, keeping things orderly and secure. Every time you log into something with your Google account or see a map embedded in a website, you're witnessing API diplomacy in action.",
            "Think of an API as the USB port of the software world — a standardized connection point that lets completely different things work together seamlessly. Just as you can plug any USB device into any USB port, APIs let any app connect to any service that speaks the same digital language.",
        ],
        1.5: [
            "An API is basically software's version of a secret handshake combined with a Rosetta Stone and a really efficient postal service that delivers packages at the speed of electrons. It's the reason your phone can simultaneously know the weather in Tokyo, your bank balance, and where the nearest pizza place is.",
            "Imagine if every building in the world had a magical window where you could shout requests and get answers from the building's brain — that's an API, except the windows are invisible and the shouting happens at light speed through the internet's plumbing system.",
            "An API is the invisible bridge troll of the internet — except instead of asking riddles, it checks if you have the right password and then hands you exactly the data treasure you requested from the castle of another application across the digital moat.",
        ],
    },
}

PROMPTS = list(CACHED.keys())
TEMPERATURES = [0.0, 0.3, 0.7, 1.0, 1.5]


def try_live_api(prompt, temperature):
    """Try OpenAI API if available."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return None
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        responses = []
        for _ in range(3):
            r = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=150
            )
            responses.append(r.choices[0].message.content.strip())
        return responses
    except Exception:
        return None


def generate_responses(prompt_choice, custom_prompt):
    prompt = custom_prompt.strip() if custom_prompt.strip() else prompt_choice
    if not prompt:
        return "Please select or enter a prompt."

    md = f"## Prompt: *\"{prompt}\"*\n\n"

    for temp in TEMPERATURES:
        md += f"### Temperature {temp}\n\n"

        # Try live API, then cached
        if prompt in CACHED and temp in CACHED[prompt]:
            responses = CACHED[prompt][temp]
            source = "cached"
        else:
            live = try_live_api(prompt, temp)
            if live:
                responses = live
                source = "live"
            else:
                md += "*[No cached response for this prompt. Deploy with OPENAI_API_KEY for live responses.]*\n\n"
                continue

        for i, r in enumerate(responses):
            md += f"**Response {i+1}:** {r}\n\n"

        # Variation analysis
        if len(set(responses)) == 1:
            md += "**Variation:** None — identical every time ✅\n\n"
        elif len(set(responses)) == len(responses):
            md += f"**Variation:** High — all {len(responses)} responses are different 🎨\n\n"
        else:
            md += "**Variation:** Moderate — some responses overlap ⚖️\n\n"

        md += "---\n\n"

    # Recommendation
    md += "## Recommendation\n\n"
    md += "| Use Case | Recommended Temperature |\n"
    md += "|----------|------------------------|\n"
    md += "| Factual Q&A, data extraction, classification | **0** |\n"
    md += "| Customer support, summaries | **0.3** |\n"
    md += "| Marketing copy, brainstorming | **0.7–1.0** |\n"
    md += "| Experimental/creative only | **1.0+** |\n"

    return md


# ── Gradio UI ─────────────────────────────────────────────────────────────────

with gr.Blocks(title="Temperature Playground", theme=gr.themes.Soft(primary_hue="blue")) as demo:
    gr.Markdown(
        "# Temperature Playground\n"
        "Same prompt at 5 different temperatures. See how creativity and consistency change.\n"
        "**Temperature is a product decision, not just an engineering parameter.**"
    )

    prompt_dd = gr.Dropdown(
        choices=PROMPTS,
        value=PROMPTS[0],
        label="Select a Prompt"
    )
    custom_prompt = gr.Textbox(
        label="Or enter your own (requires OPENAI_API_KEY)",
        placeholder="Type a custom prompt...",
        lines=2
    )

    run_btn = gr.Button("Generate at All Temperatures", variant="primary")
    output = gr.Markdown()

    run_btn.click(generate_responses, [prompt_dd, custom_prompt], [output])
    demo.load(generate_responses, [prompt_dd, custom_prompt], [output])

    gr.Markdown("---\n*Part of the AI for Product Managers course by Data Trainers LLC*")

if __name__ == "__main__":
    demo.launch()
