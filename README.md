


# Anonim Çocuk Ses Verisi Toplama Platformu

AiNALab, 2–7 yaş arası çocuklardan anonim ses verisi toplayan,
KVKK / GDPR / COPPA uyumlu, ölçeklenebilir bir veri toplama platformudur.

Sistem; ses dosyalarını doğrudan Azure Blob Storage’a yüklerken backend’i:

- Ham ses trafiğinden tamamen izole eder

- Retry durumlarına karşı idempotent kılar

  Yalnızca metadata ve durum bilgisi saklar

milyonlarca kayıt ölçeğinde çalışacak şekilde tasarlanmıştır.

## Projenin Temel Hedefleri

- Backend üzerinden ham ses verisi geçmemesi

- Retry’larda aynı kaydın tekrar üretilmemesi

- PII (kişisel veri) hiçbir seviyede toplanmaması

- Denetlenebilir, temiz ve akademik olarak savunulabilir mimari

- Pipeline ve annotation fazlarına evrimleşebilir yapı

## Teknoloji Yığını
|Katman                         |Teknoloji                    |
|-------------------------------|-----------------------------|
|    Backend	FastAPI           |      (Python 3.11)          |
|    Validation                 |       Pydantic              |
|    Database                   |       MongoDB               |
|    Storage                    |       Azure Blob Storage    |
	
	

