import os
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
from EnvSettings import EnvSettings
from SamplePrompts import SamplePrompts
from JSONHelper import JSONHelper
import argparse


def main(id:str, input_json_file:str = 'prompts.json'):
    # APIキーの環境変数, 入出力ディレクトリ、出力ファイル名の設定
    env_settings = EnvSettings(True)
    env_settings.get_api_key(var_name = "GEMINI_API_KEY")
    input_dir = env_settings.get_absolute_path("_input")
    output_dir = env_settings.get_absolute_path("_output")
    output_filename = env_settings.get_filename(prefix="tti", ext="png")

    # Geminiクライアントを初期化
    client = genai.Client()
    aspect_ratio = "4:3"  # 画像のアスペクト比を指定（例: "4:3", "1:1", "16:9"など）
    
    # 1. 入力プロンプトにSamplePromptsクラスを使用する場合：
    sample_prompts = SamplePrompts()
    index = 14  # 使用するプロンプトのインデックスを指定
    prompt = sample_prompts.prompts[index]  # 生成したいプロンプトを選択
    
    # 2. 入力プロンプトにJSONファイルを使用する場合
    json_helper = JSONHelper()
    #id = 's13'
    prompt_dict = json_helper.LoadFromFile(input_json_file)
    prompt = prompt_dict[id]
    
    if prompt is None:
        return
    
    #print(index, prompt.text)
    pimage = prompt['image']
    ptext = prompt['text']
    print(pimage, ptext)
    
    if pimage == "none":
        contents = [ptext]
        
    elif(type(pimage) is str):
        image_path = os.path.join(input_dir, pimage)
        image = Image.open(image_path)
        contents = [image, ptext]
        
    elif(type(pimage) is list):
        contents = []
        for image_file in pimage:
            # 画像が指定されている場合、画像を読み込んでBase64エンコードする
            image_path = os.path.join(input_dir, image_file)
            image = Image.open(image_path)
            contents.append(image)
        contents.append(ptext)
        
    else:
        contents = [ptext]
        

    response = client.models.generate_content(
        model="gemini-2.5-flash-image",
        contents=contents,
        config=types.GenerateContentConfig(
            image_config=types.ImageConfig(
                aspect_ratio=aspect_ratio,
            )
        )
    )

    for part in response.candidates[0].content.parts:
        if part.text is not None:
            print(part.text)
        elif part.inline_data is not None:
            image = Image.open(BytesIO(part.inline_data.data))
            image.save(os.path.join(output_dir, output_filename))
        
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('i', default='s01', help='JSON entry') 
    parser.add_argument('--f', default='prompts.json', help='Input JSON file name') 
    args = parser.parse_args()
    print(args.f, args.i)
    
    main(args.i, args.f)