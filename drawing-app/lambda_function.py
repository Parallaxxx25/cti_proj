import json
import boto3
import urllib.request
import urllib.error
import base64
from datetime import datetime
import os
import traceback

s3_client = boto3.client("s3")


def lambda_handler(event, context):
    """
    AWS Lambda function for direct sketch-to-image generation
    """
    try:
        # ===== FIX: Handle ALL possible event formats =====
        print("=== RAW EVENT ===")
        print(json.dumps(event, default=str))

        # Initialize body as None
        body = None

        # Case 1: API Gateway with body field (most common)
        if isinstance(event, dict) and "body" in event:
            print("Case 1: API Gateway format with 'body' field")
            body_content = event["body"]

            if isinstance(body_content, str):
                # Body is JSON string, parse it
                try:
                    body = json.loads(body_content)
                    print("Successfully parsed JSON body string")
                except json.JSONDecodeError as e:
                    print(f"JSON decode error: {e}")
                    return error_response(f"Invalid JSON: {str(e)}", 400)
            elif isinstance(body_content, dict):
                # Body is already a dict
                body = body_content
                print("Body is already a dict")
            else:
                print(f"Unexpected body type: {type(body_content)}")
                return error_response("Invalid body format", 400)

        # Case 2: Direct invocation (test event)
        elif isinstance(event, dict) and "imageData" in event:
            print("Case 2: Direct invocation format")
            body = event

        # Case 3: Event is the body itself
        elif isinstance(event, dict):
            print("Case 3: Event is the body")
            body = event

        else:
            print(f"Unexpected event type: {type(event)}")
            return error_response("Invalid event format", 400)

        # ===== Validate body =====
        if body is None:
            print("ERROR: body is None")
            return error_response("No request body", 400)

        if not isinstance(body, dict):
            print(f"ERROR: body is not a dict, it's {type(body)}")
            return error_response("Body must be an object", 400)

        print(f"Body keys: {list(body.keys())}")

        # ===== Extract data =====
        image_data = body.get("imageData")
        style = body.get("style", "realistic")

        print(f"imageData exists: {image_data is not None}")
        print(f"imageData type: {type(image_data)}")
        print(f"imageData length: {len(image_data) if image_data else 0}")
        print(f"style: {style}")

        # Get API key
        api_key = os.environ.get("GEMINI_API_KEY")

        if not api_key:
            print("ERROR: GEMINI_API_KEY not set")
            return error_response("GEMINI_API_KEY not configured", 500)

        # ===== Validate imageData =====
        if not image_data:
            print("ERROR: imageData is empty or missing")
            print(f"Full body received: {json.dumps(body, default=str)}")
            return error_response("No image data provided", 400)

        if not isinstance(image_data, str):
            print(f"ERROR: imageData is not a string, it's {type(image_data)}")
            return error_response("imageData must be a string", 400)

        if len(image_data) < 10:
            print(f"ERROR: imageData too short: {len(image_data)} chars")
            return error_response("imageData is too short", 400)

        # ===== Process imageData =====
        mime_type = "image/png"

        if image_data.startswith("data:image"):
            print("Removing data URL prefix...")
            parts = image_data.split(",")
            if len(parts) == 2:
                mime_type = image_data.split(";")[0].split(":")[1]
                image_data = parts[1]
                print(f"Extracted mime type: {mime_type}")
                print(f"New imageData length: {len(image_data)}")
            else:
                print("ERROR: Invalid data URL format")
                return error_response("Invalid data URL format", 400)

        print(f"Processing sketch with style: {style}, mime: {mime_type}")

        # ===== Generate image =====
        print("Generating image with Gemini...")
        generated_image_base64, prompt_used = generate_image_from_sketch(
            api_key, image_data, style, mime_type
        )

        if not generated_image_base64:
            print("ERROR: Image generation failed")
            return error_response("Failed to generate image", 500)

        print("Image generated successfully")

        # Upload to S3
        s3_url = upload_to_s3(generated_image_base64, style)

        # ===== Return success =====
        response_data = {
            "success": True,
            "data": {
                "prompt": prompt_used,
                "imageBase64": f"data:image/png;base64,{generated_image_base64}",
                "s3Url": s3_url,
                "style": style,
            },
        }

        print("Returning success response")
        return {
            "statusCode": 200,
            "headers": cors_headers(),
            "body": json.dumps(response_data),
        }

    except Exception as e:
        print(f"EXCEPTION: {str(e)}")
        traceback.print_exc()
        return error_response(str(e), 500)


def generate_image_from_sketch(api_key, sketch_data, style, mime_type):
    """Generate image using Gemini 2.5 Flash Image Preview"""
    try:
        style_prompts = {
            "realistic": "photorealistic, highly detailed, professional photography, natural lighting, 8k quality",
            "anime": "anime style, vibrant colors, Japanese animation aesthetic, cel-shaded, manga inspired",
            "cartoon": "cartoon style, bold colors, playful illustration, animated feel, exaggerated features",
            "oil-painting": "oil painting style, classical art, textured brushstrokes, rich colors, artistic masterpiece",
            "watercolor": "watercolor painting, soft washes, delicate colors, artistic, painted on paper texture",
            "sketch": "detailed pencil sketch, hand-drawn, artistic line work, shading and hatching, graphite drawing",
            "3d-render": "3D rendered, computer graphics, smooth surfaces, professional CGI, octane render, unreal engine",
            "pixel-art": "pixel art style, retro gaming aesthetic, 8-bit or 16-bit graphics, pixelated, sprite art",
            "cyberpunk": "cyberpunk style, neon lights, futuristic, sci-fi aesthetic, dark with bright accents, technological",
            "fantasy": "fantasy art style, magical atmosphere, ethereal, epic illustration, mystical and enchanting",
        }

        style_desc = style_prompts.get(style, "high quality artistic style")
        full_prompt = f"Transform this sketch into a beautiful image, {style_desc}, masterpiece quality, professional artwork"

        print(f"Using prompt: {full_prompt}")

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image-preview:generateContent?key={api_key}"

        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [
                        {"text": full_prompt},
                        {
                            "inlineData": {
                                "mimeType": mime_type,
                                "data": sketch_data,
                            }
                        },
                    ],
                }
            ],
            "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]},
            "safetySettings": [
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
                },
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
                },
            ],
        }

        data_bytes = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data_bytes, method="POST")
        req.add_header("Content-Type", "application/json")

        try:
            with urllib.request.urlopen(req, timeout=90) as response:
                response_body = response.read().decode("utf-8")
                data = json.loads(response_body)

                if "candidates" in data and len(data["candidates"]) > 0:
                    parts = data["candidates"][0].get("content", {}).get("parts", [])

                    # Find image part
                    image_part = next(
                        (
                            p
                            for p in parts
                            if "inlineData" in p
                            and p["inlineData"].get("mimeType", "").startswith("image/")
                        ),
                        None,
                    )

                    if image_part:
                        image_base64 = image_part["inlineData"].get("data")
                        if image_base64:
                            print(f"Generated image size: {len(image_base64)} chars")
                            return image_base64, full_prompt

                print("No image in API response")
                print(f"Response: {json.dumps(data, indent=2)}")
                return None, full_prompt

        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8")
            print(f"Gemini API error {e.code}: {error_body}")
            return None, full_prompt

    except Exception as e:
        print(f"Error generating image: {str(e)}")
        traceback.print_exc()
        return None, ""


def upload_to_s3(image_base64, style):
    """Upload to S3 with pre-signed URL"""
    bucket_name = os.environ.get("S3_BUCKET_NAME")

    if not bucket_name:
        print("S3_BUCKET_NAME not configured, skipping upload")
        return None

    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"generated-images/drawing_{timestamp}_{style}.png"

        image_bytes = base64.b64decode(image_base64)

        s3_client.put_object(
            Bucket=bucket_name, Key=filename, Body=image_bytes, ContentType="image/png"
        )

        # Generate pre-signed URL (1 hour)
        s3_url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": filename},
            ExpiresIn=3600,
        )

        print(f"Uploaded to S3: {filename}")
        return s3_url

    except Exception as e:
        print(f"S3 upload failed: {str(e)}")
        return None


def error_response(message, status_code):
    """Return error response"""
    return {
        "statusCode": status_code,
        "headers": cors_headers(),
        "body": json.dumps({"success": False, "error": message}),
    }


def cors_headers():
    """CORS headers"""
    return {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type,x-api-key,Authorization",
        "Access-Control-Allow-Methods": "POST,OPTIONS",
    }
