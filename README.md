# Gemini 画像生成
[Gemini を使った画像生成](https://ai.google.dev/gemini-api/docs/image-generation?hl=ja)

## 入力JSON
prompt.json

## 機能
### 1. Image Generation
```
> uv run imagegen.py s01
```
入力データ例
```json
    "s01":{
        "image":"none",
        "aspect":"1:1",
        "text":"Create a picture of a nano banana dish in a fancy restaurant with a Gemini theme"
    },
    "s04":{
        "image":"kitty.jpeg",
        "text":"Create a picture of my cat eating a nano-banana in a fancy restaurant with a Gemini theme"
    },
```


### 2. Video Generation
```
> uv run videogen.py v01
```
入力データ例
```json
    "v01":{
        "image":"none",
        "aspect":"16:9",
        "resolution":"720p",
        "duration":"4",
        "text":"A close up of two people staring at a cryptic drawing on a wall, torchlight flickering.A man murmurs, 'This must be it. That's the secret code.' The woman looks at him and whispering excitedly, 'What did you find?'"
    },
    "v02":{
        "image":"airport.png",
        "aspect":"16:9",
        "resolution":"720p",
        "duration":"4",
        "text":"雪の降る飛行場。飛行機のタラップにむかって、雪だるまが飛び跳ねながら進んでいる"
    }
```


