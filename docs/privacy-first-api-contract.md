# Privacy-First API Contract

AiNA API, en başından itibaren **privacy-by-design** ve
**data minimization** ilkeleriyle tasarlanmıştır.

Bu doküman, AiNA’nın API sözleşmesinin yalnızca teknik bir arayüz değil,
aynı zamanda **etik, hukuki ve akademik bir taahhüt** olduğunu açıklar.

---

## 1. API Contract = Toplanabilecek Verinin Sınırı

AiNA’da:

> **API sözleşmesinde (OpenAPI) tanımlı olmayan hiçbir alan
> backend tarafından kabul edilmez.**

Bu yaklaşım sayesinde:
- Toplanan veri türleri **teknik olarak sınırlandırılmıştır**
- “Sonradan veri ekleme” riski ortadan kaldırılmıştır
- KVKK/GDPR kapsamında **kanıtlanabilir veri minimizasyonu** sağlanır

OpenAPI dokümanı bu nedenle:
- Teknik referans
- Hukuki kanıt
- Akademik metodoloji girdisi

olarak birlikte değerlendirilir.

---

## 2. Kişisel Veri (PII) Toplanmaması

AiNA API:

- İsim
- Soyisim
- E-posta
- Telefon
- IP adresi
- Cihaz kimliği

gibi **doğrudan veya dolaylı tanımlayıcı verileri toplamaz**.

Tüm endpoint’ler yalnızca:
- Oturum bazlı anonim ID’ler
- Yaşla ilişkili, bireyi tanımlamayan demografik bilgiler
- Ses kayıtlarına ait teknik metadata

üzerinden çalışır.

---

## 3. Consent Artifact Yaklaşımı

Kullanıcı onayı, kişisel veri olarak değil,
**bağımsız bir consent artifact** olarak ele alınır.

API sözleşmesinde yer alan alanlar:
- `consent_version`
- `consent_text_hash`
- `consent_accepted_at`
- `jurisdiction`

Bu yapı sayesinde:
- Onay metni değiştiğinde yeni versiyon izlenebilir
- Kimin, neyi, ne zaman kabul ettiği **kişisel veri olmadan**
kanıtlanabilir

---

## 4. Backend Otoritesi İlkesi

API tasarımında:

- Frontend yalnızca **niyet bildirir**
- İş kuralları ve ilerleme durumu **backend otoritesindedir**

Örnek:
- Kayıt tamamlanma sayısı (`ok_count`)
- Bir oturumun “completed” sayılması
- Bir adımın geçerli olup olmadığı

Bu yaklaşım:
- Manipülasyonu önler
- Veri bütünlüğünü korur
- Akademik analizler için güvenilirlik sağlar

---

## 5. Test ve Internal Endpoint’ler

AiNA’da bazı endpoint’ler:
- Şema doğrulama
- Geliştirme testleri

için mevcuttur.

Bu endpoint’ler:
- `include_in_schema = false`
- Public OpenAPI sözleşmesine **dahil edilmez**

Böylece:
- Geliştirme esnekliği korunur
- Public API yüzeyi dar ve güvenli kalır

---

## 6. Sonuç

AiNA API Contract’i:

- Sadece bir teknik doküman değil
- Aynı zamanda bir **etik ve hukuki sınır çizimi**dir

Bu yaklaşım sayesinde AiNA:
- Privacy-first ilkesini söylemde değil, **kod seviyesinde**
uygular
- Akademik çalışmalara ve regülasyonlara
**kanıtlanabilir uyum** sağlar
