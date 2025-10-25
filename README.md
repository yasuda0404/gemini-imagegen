# Gemini 画像生成
[Gemini を使った画像生成](https://ai.google.dev/gemini-api/docs/image-generation?hl=ja)

## 機能
1. Text-to-Image
2. Image-to-Image

## SamplePrompts.py
1. Text-to-Image
```
self.prompts.append(Prompt("none", "Create a picture of a nano banana dish in a fancy restaurant with a Gemini theme"))
```

2. Image-to-Image
```
self.prompts.append(Prompt("kitty.jpeg", "Create a picture of my cat eating a nano-banana in a fancy restaurant with a Gemini theme"))
```