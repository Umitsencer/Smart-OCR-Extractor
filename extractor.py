import re
import easyocr
import json

class DataExtractor:
    """
    Stabil ve Hızlı Data Extraction:
    EasyOCR kullanarak Türkçe dökümanlardan veri ayıklar.
    """
    def __init__(self, lang_list=['tr', 'en']):
        # EasyOCR motorunu başlat (Türkçe ve İngilizce)
        self.reader = easyocr.Reader(lang_list, gpu=False, verbose=False)
        
        # Regex Kalıpları (Gelişmiş binlik ayırıcı ve anahtar kelime desteği)
        self.patterns = {
            "tckn": r"\b[1-9][0-9]{10}\b",
            "vkn": r"\b[0-9]{10}\b",
            "tarih": r"(\d{2}[./-]\d{2}[./-]\d{4})",
            # Binlik ayırıcılı (.,) ve kuruşlu tutarları yakalar, 'TOPLAM' kelimesine öncelik verir
            "tutar": r"(?:TOPLAM|TUTAR|GENEL|ÖDENECEK).*?(\d{1,3}(?:[.,]\d{3})*[.,]\d{2})\s*(?:TL|TRY|₺|tl|TL|Tl)",
        }

    def extract_text(self, img_input):
        """Görselden metni çıkarır ve birleştirir"""
        # Detail=0 sadece metni döndürür
        results = self.reader.readtext(img_input, detail=0)
        return " ".join(results)

    def parse_data(self, text):
        """Ham metinden yapısal verileri ayıklar"""
        extracted_data = {
            "tckn": None,
            "vkn": None,
            "tarih": None,
            "tutar": None,
            "ham_metin": text
        }

        # Standart veriler (TCKN, VKN, Tarih)
        for key in ["tckn", "vkn", "tarih"]:
            match = re.search(self.patterns[key], text, re.IGNORECASE)
            if match:
                extracted_data[key] = match.group(0).strip()

        # Tutar Ayıklama (Özel Mantık: En son ve en büyük tutarı bulmaya çalışır)
        tutar_matches = re.findall(self.patterns["tutar"], text, re.IGNORECASE)
        if tutar_matches:
            # Genellikle faturanın en altındaki tutar gerçek toplamdır
            extracted_data["tutar"] = f"{tutar_matches[-1]} TL"

        return extracted_data
