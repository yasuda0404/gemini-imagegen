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
        # 05
        self.prompts.append(Prompt("none", "Create a modern, minimalist logo for a coffee shop called 'The Daily Grind'. The text should be in a clean, bold, sans-serif font. The design should feature a simple, stylized icon of a a coffee bean seamlessly integrated with the text. The color scheme is black and white"))
        # 06
        self.prompts.append(Prompt("none", "A high-resolution, studio-lit product photograph of a minimalist ceramic coffee mug in matte black, presented on a polished concrete surface. The lighting is a three-point softbox setup designed to create soft, diffused highlights and eliminate harsh shadows. The camera angle is a slightly elevated 45-degree shot to showcase its clean lines. Ultra-realistic, with sharp focus on the steam rising from the coffee. Square image."))
        # 07
        self.prompts.append(Prompt("none", "A minimalist composition featuring a single, delicate red maple leaf positioned in the bottom-right of the frame. The background is a vast, empty off-white canvas, creating significant negative space for text. Soft, diffused lighting from the top left. Square image."))
        # 08
        self.prompts.append(Prompt("none", "A single comic book panel in a gritty, noir art style with high-contrast black and white inks. In the foreground, a detective in a trench coat stands under a flickering streetlamp, rain soaking his shoulders. In the background, the neon sign of a desolate bar reflects in a puddle. A caption box at the top reads \"The city was a tough place to keep secrets.\" The lighting is harsh, creating a dramatic, somber mood. Landscape."))
        # 09
        self.prompts.append(Prompt("cat.png", "Using the provided image of my cat, please add a small, knitted wizard hat on its head. Make it look like it's sitting comfortably and not falling off."))
        # 10
        self.prompts.append(Prompt("living_room.png", "Using the provided image of a living room, change only the blue sofa to be a vintage, brown leather chesterfield sofa. Keep the rest of the room, including the pillows on the sofa and the lighting, unchanged."))
        # 11
        self.prompts.append(Prompt("city.png", "Transform the provided photograph of a modern city street at night into the artistic style of Vincent van Gogh's 'Starry Night'. Preserve the original composition of buildings and cars, but render all elements with swirling, impasto brushstrokes and a dramatic palette of deep blues and bright yellows."))
        # 12
        self.prompts.append(Prompt(["dress.png","model.png"], "Create a professional e-commerce fashion photo. Take the blue floral dress from the first image and let the woman from the second image wear it. Generate a realistic, full-body shot of the woman wearing the dress, with the lighting and shadows adjusted to match the outdoor environment."))
        # 13
        self.prompts.append(Prompt(["dress.png","tomoko.jpg"], "Create a professional e-commerce fashion photo. Take the blue floral dress from the first image and let the woman from the second image wear it. Generate a realistic, full-body shot of the woman wearing the dress, with the lighting and shadows adjusted to match the outdoor environment."))
        # 14
        self.prompts.append(Prompt(["woman.jpg","logo.png"], "Take the first image of the woman with brown hair, blue eyes, and a neutral expression. Add the logo from the second image onto her black t-shirt. Ensure the woman's face and features remain completely unchanged. The logo should look like it's naturally printed on the fabric, following the folds of the shirt."))
        
