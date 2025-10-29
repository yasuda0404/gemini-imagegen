# Video Generator
# by A.Y. 2025/10/28
import os
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
from EnvSettings import EnvSettings
from SamplePrompts import SamplePrompts
from JSONHelper import JSONHelper
import argparse
import time
import base64
from PIL import Image as PILImage # Pillowライブラリをインポート

def get_image_object(image_name:str|None, input_dir):
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
    output_filename = env_settings.get_filename(prefix="ttv", ext="mp4")

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

    if prompt is None:
        return

    # 入力値の取得
    model="veo-3.1-generate-preview"
    ptext = prompt.get("prompt")
    pimage = prompt.get(
        "image", None
    )
    image = get_image_object(pimage, input_dir)
    print(f'type(image): {type(image)}')
    negative_prompt = prompt.get(
        "negative_prompt", None
    )
    aspect_ratio = prompt.get(
        "aspect", "16:9"
    )  # 画像のアスペクト比を指定（例: "16:9" or "9:16"）
    resolution = prompt.get(
        "resolution", "720p"
    )
    duration_seconds = prompt.get(
        "duration", "4"
    )
    ref_images = prompt.get(
        "ref_images", None
    )
    slast_frame = prompt.get(
        "last_frame", None
    )
    if(slast_frame is None):
        last_frame = None
    else:
        last_frame = get_image_object(slast_frame, input_dir)
        print(f'type(last_frame): {type(last_frame)}')
    
    print(ptext, pimage, aspect_ratio, resolution, ref_images, slast_frame, negative_prompt)
    
    # 参照画像の作成
    refs = None
    if (type(ref_images) is list):
        refs = []
        for ref_image in ref_images:
            image_path = os.path.join(input_dir, ref_image)
            _ref_image = types.Image.from_file(location=image_path)
            _ref_asset = types.VideoGenerationReferenceImage(
                image=_ref_image, # Generated separately with Nano Banana
                reference_type="asset"
            )
            refs.append(_ref_asset)

    
    start_time = time.perf_counter()        # 計算開始時刻
    operation = client.models.generate_videos(
        model=model,
        prompt=ptext,
        image=image,
        config=types.GenerateVideosConfig(
            aspect_ratio=aspect_ratio,
            resolution=resolution,
            duration_seconds=duration_seconds,
            reference_images=refs,
            last_frame=last_frame,
            negative_prompt=negative_prompt
        )
    )
        

    # Poll the operation status until the video is ready.
    while not operation.done:
        print("Waiting for video generation to complete...")
        time.sleep(10)
        operation = client.operations.get(operation)
        
    # 計算時間の表示
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f"Calculation time: {elapsed_time:.2f} sec.")
    
    # Download the video.
    video = operation.response.generated_videos[0]
    client.files.download(file=video.video)
    video.video.save(os.path.join(output_dir, output_filename))
    print("Generated video saved to", output_filename)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("i", default="s01", help="JSON entry")
    parser.add_argument("--f", default="prompts.json", help="Input JSON file name")
    args = parser.parse_args()
    print(args.f, args.i)

    main(args.i, args.f)
