import cv2
import numpy as np
import argparse

def downscale_image(image_path, output_path=None):
    """
    画像を1/4サイズにダウンスケールする関数
    
    Parameters:
    -----------
    image_path : str
        入力画像のパス
    output_path : str, optional
        出力画像のパス。Noneの場合、'downscaled_' + 元のファイル名
    
    Returns:
    --------
    bool : 処理が成功したかどうか
    """
    try:
        # 画像の読み込み
        img = cv2.imread(image_path)
        if img is None:
            print(f"Error: Could not read image at {image_path}")
            return False
            
        # 元の画像サイズを取得
        height, width = img.shape[:2]
        print(f"Original size: {width}x{height}")
        
        # 新しいサイズを計算（1/4）
        new_width = width // 2
        new_height = height // 2
        
        # リサイズ実行
        # INTER_AREA is preferred for downscaling
        resized_img = cv2.resize(img, (new_width, new_height), 
                               interpolation=cv2.INTER_AREA)
        
        # 出力パスの設定
        if output_path is None:
            import os
            filename = os.path.basename(image_path)
            dirname = os.path.dirname(image_path)
            output_path = os.path.join(dirname, 'downscaled_' + filename)
        
        # 画像の保存
        cv2.imwrite(output_path, resized_img)
        
        print(f"New size: {new_width}x{new_height}")
        print(f"Saved to: {output_path}")
        return True
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Downscale an image to 1/4 of its original size')
    parser.add_argument('image_path', help='Path to the input image')
    parser.add_argument('--output', '-o', help='Path for the output image (optional)')
    
    args = parser.parse_args()
    downscale_image(args.image_path, args.output)

if __name__ == "__main__":
    main()