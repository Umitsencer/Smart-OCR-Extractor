import cv2
import numpy as np
import os

class ImagePreprocessor:
    """
    Senior Level Image Preprocessing:
    OCR başarısını artırmak için görselleri temizler, hizalar ve normalize eder.
    """
    def __init__(self, output_dir="outputs/processed"):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def clean_image(self, image_path):
        """Görseli gri tonlama, gürültü silme ve thresholding işlemlerinden geçirir."""
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Görsel yüklenemedi: {image_path}")

        # 1. Grayscale: Renk karmaşasından kurtul
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 2. Denoising: Noktasal gürültüleri temizle
        denoised = cv2.fastNlMeansDenoising(gray, h=10)

        # 3. Adaptive Thresholding: Yazıları arka plandan net bir şekilde ayır
        # (Özellikle market fişlerindeki gölgeleri temizlemek için kritiktir)
        thresh = cv2.adaptiveThreshold(
            denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY, 11, 2
        )

        # Temizlenmiş halini kaydet (Debug/Görselleştirme için)
        base_name = os.path.basename(image_path)
        output_path = os.path.join(self.output_dir, f"clean_{base_name}")
        cv2.imwrite(output_path, thresh)
        
        return thresh

if __name__ == "__main__":
    # Test Amaçlı Çalıştırma
    preprocessor = ImagePreprocessor()
    try:
        # aday_1_fatura.png üzerinde test et
        result = preprocessor.clean_image("aday_1_fatura.png")
        print("[BAŞARILI] Görsel ön-işlemeden geçti ve 'outputs/processed' altına kaydedildi.")
    except Exception as e:
        print(f"[HATA] {e}")
