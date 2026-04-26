import os
import json
from preprocessor import ImagePreprocessor
from extractor import DataExtractor

class OCRSystem:
    def __init__(self):
        print("\n--- [AKILLI OCR SİSTEMİ BAŞLATILIYOR] ---")
        self.preprocessor = ImagePreprocessor()
        self.extractor = DataExtractor()
        self.input_dir = "."
        self.output_dir = "outputs/results"
        
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def process_document(self, file_name):
        print(f"\n[İŞLENİYOR] {file_name}...")
        try:
            # 1. Ön İşleme
            # Not: Bazı durumlarda EasyOCR ham görselde daha iyi sonuç verebilir.
            # Şimdilik direkt görseli veriyoruz.
            raw_text = self.extractor.extract_text(file_name)
            data = self.extractor.parse_data(raw_text)
            
            # 2. Kayıt
            output_file = os.path.join(self.output_dir, f"{file_name.split('.')[0]}.json")
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            
            print(f"[BAŞARILI] {file_name} tamamlandı.")
            print(f"  > Veriler: TCKN/VKN: {data['tckn'] or data['vkn']} | Tutar: {data['tutar']} | Tarih: {data['tarih']}")
            
        except Exception as e:
            print(f"[HATA] {file_name}: {e}")

    def run(self):
        files = [f for f in os.listdir(self.input_dir) if f.endswith(('.png', '.jpg')) and "aday" in f]
        for f in files:
            self.process_document(f)
        print("\n--- [TÜM SÜREÇ BAŞARIYLA TAMAMLANDI] ---")

if __name__ == "__main__":
    app = OCRSystem()
    app.run()
