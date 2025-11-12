# Video Generator
# by A.Y. 2025/10/28
import os
from google import genai
from google.genai import types
from EnvSettings import EnvSettings
from SamplePrompts import SamplePrompts
from JSONHelper import JSONHelper
import argparse
import time


def get_image_object(image_name:str|None, input_dir:str):
    if (image_name == "none" or image_name is None):
        print("Image None")
        return None
    else:
        print(f"Image: {image_name}")
        image_path = os.path.join(input_dir, image_name)
        return types.Image.from_file(location=image_path)

def main(id: str, input_json_file: str = "prompts.json"):
    # APIキーの環境変数, 入出力ディレクトリ、出力ファイル名の設定
    env_settings = EnvSettings(True)
    env_settings.get_api_key(var_name="GEMINI_API_KEY")
    input_dir = env_settings.get_absolute_path("_input")
    output_dir = env_settings.get_absolute_path("_output")
    output_filename = env_settings.get_filename(prefix="tx", ext="txt")

    # Geminiクライアントを初期化
    client = genai.Client()

    # 【旧】入力プロンプトにSamplePromptsクラスを使用する場合：
    sample_prompts = SamplePrompts()
    index = 14  # 使用するプロンプトのインデックスを指定
    prompt = sample_prompts.prompts[index]  # 生成したいプロンプトを選択

    # 【新】入力プロンプトにJSONファイルを使用する場合
    json_helper = JSONHelper()
    # id = 's13'
    prompt_dict = json_helper.LoadFromFile(input_json_file)
    prompt = prompt_dict[id]


    # テキストプロンプト
    if prompt is None:
        return
    ptext:str = prompt.get("prompt")
    
    # モデル
    model:str|None = prompt.get(
        "model", "gemini-2.5-flash"
    )
    # システムプロンプト
    system_instruction:str|None = prompt.get(
        "system_instruction", None
    )
    # 参照画像
    pimage:str = prompt.get(
        "image", None
    )
    image = get_image_object(pimage, input_dir)
    print(f'type(image): {type(image)}')
    
    # ハイパーパラメータ
    temperature:float|None = prompt.get(
        "temperature", None
    )
    top_p:float|None = prompt.get(
        "top_p", None
    )
    top_k:float|None = prompt.get(
        "top_k", None
    )
    
    print('All params:', model, ptext, pimage, temperature)
    
    # 参照画像無し・有りの場合のcontentsの記述
    if image is not None:
        contents = [image, ptext]
    else:
        contents = [ptext]
    
    start_time = time.perf_counter()        # 計算開始時刻
    
    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature = temperature,
            top_p=top_p,
            top_k=top_k
        )
    )

    # 計算時間の表示
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f"Calculation time: {elapsed_time:.2f} sec.")
    
    # レスポンス・テキストの保存
    print(response.text)
    output_path = os.path.join(output_dir, output_filename)
    with open( output_path , "w", encoding="utf-8") as f:
        f.write(response.text)
        print("Generated video saved to", output_filename)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("i", default="s01", help="JSON entry")
    parser.add_argument("--f", default="prompts.json", help="Input JSON file name")
    args = parser.parse_args()
    print(args.f, args.i)

    main(args.i, args.f)
