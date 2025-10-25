from collections import namedtuple

class SamplePrompts:

    prompts = []
    
    def __init__(self):
        # 名前付きタプル
        Prompt = namedtuple("Prompt", ["image","text"])
        # 00
        self.prompts.append(Prompt("none", "Create a picture of a nano banana dish in a fancy restaurant with a Gemini theme"))
        # 01
        self.prompts.append(Prompt("none", "A photorealistic close-up portrait of an elderly Japanese ceramicist with deep, sun-etched wrinkles and a warm, knowing smile. He is carefully inspecting a freshly glazed tea bowl. The setting is his rustic, sun-drenched workshop with pottery wheels and shelves of clay pots in the background. The scene is illuminated by soft, golden hour light streaming through a window, highlighting the fine texture of the clay and the fabric of his apron. Captured with an 85mm portrait lens, resulting in a soft, blurred background (bokeh). The overall mood is serene and masterful."))
        # 02
        self.prompts.append(Prompt("none", "A kawaii-style sticker of a happy red panda wearing a tiny bamboo hat. It's munching on a green bamboo leaf. The design features bold, clean outlines, simple cel-shading, and a vibrant color palette. The background must be white."))
        # 03
        self.prompts.append(Prompt("kitty.jpeg", "Create a picture of my cat eating a nano-banana in a fancy restaurant with a Gemini theme"))
        # 04
        self.prompts.append(Prompt("kitty.jpeg", "宇宙服を着た子猫が、宇宙船のコックピットで、地球を背景に窓の外を見つめている様子を描いてください。子猫は好奇心旺盛な表情で、宇宙服のヘルメットが少し大きめに見えます。コックピット内には未来的な計器やスクリーンが配置されており、窓の外には美しい青い地球と星空が広がっています。全体的に明るく希望に満ちた雰囲気で、子猫の冒険心を感じさせるイラストにしてください。"))
