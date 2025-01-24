# VT_SORGULAR

import pyodbc
from config import get_connection  # config.py'den get_connection fonksyonunu alıyoruz


class Uye:
    @staticmethod
    def connect_db():
        """
        veritabanına bağlanr ve bağlantı nesnesi döndürür.
        """
        connection = get_connection()  # config.py'dengelen bağlantı fonksiyonunu kullanıyoruz.
        return connection  # bağlantı nesnesini döndürür.

    @staticmethod
    def ekle(TCKimlikNo, Ad, Soyad, Meslek, CepTel, Eposta, Adres):
        """
        Yeni bir üye ekler

        parametreler:
        -TCKimlikNo(str):Üyenin tc kimlik no
        -Ad(str):Üyenin adı
        -Soyad(str):Üyenin Soyadı
        -CepTel(str):Üyenin cep telefonu
        -Eposta(str):Üyenin e-posta adresi
        """
        conn = Uye.connect_db()
        cursor = conn.cursor()

        try:
            # önce tckimlik numarası kayıtlımı kontrol et.
            cursor.execute("SELECT COUNT(*) FROM uye WHERE TCKimlikNo=?", (TCKimlikNo))
            count = cursor.fetchone()[0]

            if count > 0:
                raise ValueError("Bu TC Kimlik Numarası Zaten Kayıtlı.")

            # eğer kayıtlı değilse ekle.
            cursor.execute(
                "INSERT INTO uye (TCKimlikNo,Ad,Soyad,Meslek,CepTel,Eposta,Adres) VALUES(?,?,?,?,?,?,?)",
                (TCKimlikNo, Ad, Soyad, Meslek, CepTel, Eposta, Adres)
            )
            conn.commit()
        except pyodbc.Error as e:
            error_message = str(e)
            if "chk_CepTel" in error_message:
                raise ValueError(
                    "Cep telefonu formatı hatalı! Lütfen yalnızca rakam girin ve 10-15 haneli olduğundan emin olun.")
            elif "TCKimlikNo" in error_message:
                raise ValueError("TCKimlik Numarası geçersiz veya zaten kayıtlı.")
            elif "chk_Eposta" in error_message:
                raise ValueError("E-posta adresi geçersiz! Lütfen '@' ve '.' karakterlerini doğru şekilde kullanın.")
            else:
                raise ValueError(f'Veeritabanı hatası: {e}')
        finally:
            conn.close()

    @staticmethod
    def guncelle(UyeID, TCKimlikNo, Ad, Soyad, Meslek, Ceptel, Eposta, Adres):
        """
        tc kimlik numarasına göre bilgileri günceller

        parametreler:
        -TCKimlikNo (str):Güncellenecek üyenin TC Kimlik Numarası
        -Ad (str): Yeni ad
        -Soyad (str): Yeni Soyad
        -CepTel(str):Yeni cep telefonu
        -Eposta (str):Yeni e-posta adresi
        """
        conn = Uye.connect_db()
        cursor = conn.cursor()

        try:
            # Güncelleme işlemi
            cursor.execute(
                "UPDATE uye SET TCKimlikNo=?,Ad=?, Soyad=?, Meslek=?, CepTel=?, Eposta=?, Adres=? WHERE UyeID=?",
                (TCKimlikNo, Ad, Soyad, Meslek, Ceptel, Eposta, Adres, UyeID)
            )
            conn.commit()

            # Güncelleme sonrası veri kontrolü
            cursor.execute(
                "SELECT * FROM uye WHERE TCKimlikNo=?",
                (TCKimlikNo,)
            )
            result = cursor.fetchone()

            if result:
                print("Güncellenen Kayıt: ", result)
            else:
                raise ValueError("Veritabanında bu TC Kimlik Numarası ile kayıt bulunamadı.")

        except pyodbc.Error as e:
            error_message = str(e)
            if "chk_CepTel" in error_message:
                raise ValueError(
                    "Cep telefonu formatı hatalı! Lütfen yalnızca rakam girin ve 10-15 haneli olduğundan emin olun.")
            elif "TCKimlikNo" in error_message:
                raise ValueError("TCKimlik numarası geçersiz veya zaten kayıtlı.")
            elif "chk_Eposta" in error_message:
                raise ValueError("E-posta adresi geçersiz! Lütfen '@' ve '.' karakterlerini doğru şekilde kullanın.")
            else:
                raise ValueError(f'Güncelleme Hatası: {e}')
        finally:
            conn.close()

    @staticmethod
    def sil(TCKimlikNo):
        """
        Tc kimlik numarasına göre üye siler:

        Parametreler:
        TCKimlikNo(str):Silinecek üyenin TcKimlikNumarası
        """

        conn = Uye.connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM uye WHERE TCKimlikNo=?", (TCKimlikNo))
            conn.commit()
        except pyodbc.Error as e:
            raise ValueError(f"Silme Hatası:{e}")
        finally:
            conn.close()

    @staticmethod
    def listele():
        """
        Tüm Üyeleri listeler

        Geri Dönüş:
        -list[truple]: Tüm üyeler bilgilerini içeren bir liste
        """
        conn = Uye.connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM uye")
            return cursor.fetchall()  # tüm kayıtrları döndürür
        finally:
            conn.close()

    @staticmethod
    def bul(TCKimlikNo):
        """
        TC kimlik numarasına göre üye arar.

        parametreler:
        -TCKimlikNo(str): Aranacak üyenin TC Kimlik numarası

        Geri Dönüş:
        tuple:Eğer üye bulunursa, üye bilgilerini içeren bir truple döndürür.

        - None: eğer üye bulunmazsa None döndürür.
        """
        conn = Uye.connect_db()
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM uye WHERE TCKimlikNo=?", (TCKimlikNo,))
            uye = cursor.fetchone()  # Sadece bir sonuç döndürürlür.
            return uye  # eğer üye varsa,bilgilerini döndür.
        finally:
            conn.close()
