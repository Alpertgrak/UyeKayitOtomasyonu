--create database KutuphaneDB4

--KutuphaneDB veritaban�n� kullan�r.
use KutuphaneDB4

----uye taplosu olu�turur.
create table uye(
	UyeID INT IDENTITY (1,1) PRIMARY KEY,		--Otomatik artan benzersiz ID
	TCKimlikNo NVARCHAR(11) NOT NULL UNIQUE,	--TCkimlik numaras� benzersiz ve zorunlu
	Ad NVARCHAR(50) NOT NULL,					--�yenin Ad�(zorunlu)
	Soyad NVARCHAR(50) NOT NULL,				--�yenin Soyad�(zorunlu)
	Meslek NVARCHAR(50) NOT NULL,
	CepTel NVARCHAR(15) NOT NULL,				--Cep telefonu rakam i�ermeli ve zorunlu
	Eposta NVARCHAR(50) NOT NULL,				--Eposta Adresi
	Adres NVARCHAR(50) NOT NULL,
	--Ceptel i�in k�s�tlama(+90 ile ba�layacak ve 10 rakam olacak)
	CONSTRAINT chk_CepTel CHECK(
		CepTel LIKE '+90%' AND LEN(CepTel) = 13 AND ISNUMERIC(SUBSTRING(CepTel,4,LEN(CepTel)))=1),
	--TCKimlik no i�in k�s�tlama(11 haneli rakam)
	CONSTRAINT chk_TCKimlikNo CHECK(LEN(TCKimlikNo) = 11 AND ISNUMERIC(TCKimlikNo)=1),
	CONSTRAINT chk_Eposta CHECK(
		CHARINDEX('@', Eposta) > 1 AND 
		CHARINDEX('.', Eposta, CHARINDEX('@', Eposta)) > CHARINDEX('@', Eposta) + 1)
);
