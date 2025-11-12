# Video Generator
# by A.Y. 2025/10/28
import os
import re
from google import genai
from google.genai import types
from EnvSettings import EnvSettings
from SamplePrompts import SamplePrompts
from JSONHelper import JSONHelper
import argparse
import time
import base64
from PIL import Image as PILImage # Pillowライブラリをインポート
from mutagen.mp4 import MP4

def get_image_object(image_name:str|None, input_dir:str):
    if (image_name == "none" or image_name is None):
        print("Image None")
        return None
    else:
        print(f"Image: {image_name}")
        image_path = os.path.join(input_dir, image_name)
        return types.Image.from_file(location=image_path)

def get_video_object(video_name:str|None, input_dir):
    if (video_name == "none" or video_name is None):
        print("Video None")
        return None
    else:
        print(f"Video: {video_name}")
        path = os.path.join(input_dir, video_name)
        return types.Video.from_file(location=path)

def embed_operation_name_to_mp4(mp4_path: str, operation_name: str):
    """
    MP4 の ©cmt(コメント) タグに operation.name を保存する。
    Finder/プロパティ/多くのプレーヤーで参照可能。
    """
    mp4 = MP4(mp4_path)
    # 既存コメントを壊さず追記したい場合は以下でマージしても良い
    note = f"Gemini Operation: {operation_name}"
    mp4["\xa9cmt"] = note
    mp4.save()
    print(f"✅ Embedded operation.name into MP4 metadata: {note}")

def read_operation_name_from_mp4(video_name: str, input_dir:str) -> str|None:
    """
    MP4の ©cmt(コメント) から operation.name を抽出する。
    - 期待形式: "Gemini Operation: operations/XXXX..."
    - 「operations/...」だけが入っている場合にも対応
    """
    mp4_path = os.path.join(input_dir, video_name)
    mp4 = MP4(mp4_path)

    # コメントの取り出し（mutagenは値がlistのことがある）
    raw_val = mp4.tags.get("\xa9cmt")
    if not raw_val:
        #raise ValueError("MP4 comment(©cmt) not found. operation.name が埋め込まれていません。")
        print("MP4 comment(©cmt) not found. operation.name が埋め込まれていません。")
        return None
    
    if isinstance(raw_val, list):
        text = " ".join(str(v) for v in raw_val if v)
    else:
        text = str(raw_val)

    text = text.strip()

    # 1) "Gemini Operation: operations/xxxx" 形式を優先抽出
    m = re.search(r"operations\/[A-Za-z0-9\-\._]+", text)
    path = os.path.join("models/veo-3.1-generate-preview", m.group(0))
    if m:
        return path

    # 2) プレフィックス付きのとき
    OPNAME_PREFIX = "op_name"
    embed_operation_name_to_mp4
    if text.startswith(OPNAME_PREFIX):
        cand = text[len(OPNAME_PREFIX):].strip()
        if cand:
            return cand

    # 3) そのまま operations/... が入っていないが、有効そうな文字列があれば返す（最終手段）
    if text:
        return text

    print("コメントから operation.name を抽出できませんでした。")
    return None


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
    ptext = prompt.get("prompt")
    model = prompt.get(
        "model", "veo-3.1-generate-preview"
    )
    # 画像入力
    pimage = prompt.get(
        "image", None
    )
    image = get_image_object(pimage, input_dir)
    print(f'type(image): {type(image)}')
    
    # 動画メタデータからoperation_nameを取り出す
    video_name = prompt.get(
        "video", None
    )
    if video_name is not None:
        op_name = read_operation_name_from_mp4(video_name, input_dir)
    else:
        # 動画operation_name入力
        op_name = prompt.get(
            "video_op_name", None
        )
    
    if (op_name is not None):
        print(f"op_name:{op_name}")
        op = client.operations.get(types.GenerateVideosOperation(name=op_name))
        video = op.response.generated_videos[0]
    else:
        video = None   
    print(f'type(video): {type(video)}')
    
    if(video is not None):
        num_of_video = 1
    else:
        num_of_video = None
    
    negative_prompt = prompt.get(
        "negative_prompt", None
    )
    aspect_ratio = prompt.get(
        "aspect", None
    )  # 画像のアスペクト比を指定（例: "16:9" or "9:16"）
    resolution = prompt.get(
        "resolution", None
    )
    duration_seconds = prompt.get(
        "duration", None
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
        if (image is not None):
            last_frame = get_image_object(slast_frame, input_dir)
        else:
            last_frame = None
        print(f'type(last_frame): {type(last_frame)}')
    
    print('All params:', ptext, pimage, op_name, num_of_video, aspect_ratio, resolution, ref_images, slast_frame, negative_prompt)
    
    # 参照画像の作成
    # refs = None
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
        print(f'len(refs):{len(refs)}')
    else:
        refs = None
        print('refs is None')
    
    start_time = time.perf_counter()        # 計算開始時刻
    
    operation = client.models.generate_videos(
        model=model,
        prompt=ptext,
        image=image,
        video=video,
        config=types.GenerateVideosConfig(
            aspect_ratio=aspect_ratio,
            resolution=resolution,
            duration_seconds=duration_seconds,
            reference_images=refs,
            last_frame=last_frame,
            number_of_videos=num_of_video,
            negative_prompt=negative_prompt
        )
    )
    """
    operation = client.models.generate_videos(
        model=model,
        prompt=ptext,
        video=video,
        config=types.GenerateVideosConfig(
            number_of_videos=num_of_video,
            resolution=resolution
        )
    )
    """

    # Poll the operation status until the video is ready.
    while not operation.done:
        print("Waiting for video generation to complete...")
        time.sleep(10)
        operation = client.operations.get(operation)
        
    # 計算時間の表示
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f"Calculation time: {elapsed_time:.2f} sec.")
    
    # ビデオデータの保存
    video = operation.response.generated_videos[0]
    client.files.download(file=video.video)
    output_path = os.path.join(output_dir, output_filename)
    video.video.save(output_path)
    print("Generated video saved to", output_filename)
    
    # オペレーション名の埋め込み
    op_name = operation.name    # operation name 後に動画を拡張する際に必要
    print(f"operation name:{op_name}")
    embed_operation_name_to_mp4(output_path, op_name)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("i", default="s01", help="JSON entry")
    parser.add_argument("--f", default="prompts.json", help="Input JSON file name")
    args = parser.parse_args()
    print(args.f, args.i)

    main(args.i, args.f)
