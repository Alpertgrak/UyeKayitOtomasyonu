# Arayüz

import tkinter as tk  # tkinter modülünü import eder,GUI oluşturmak için kullanılır.
from tkinter import ttk, \
    messagebox  # ttk,tkinter'in gelişmilş widget'larını sağlar.messagebox,op-up mesaj kutuları için kullalır.
import re  # re modülü,düzenli ifadeerl (regex)ile metin üzerinde arama,değiştirme vb. işlemler yapmak için kullanılır.
from VT_Sorgulari import \
    Uye  # VT_Sorgulari.py dosyasındaki Uye sınıfı import eder.Bu sınıf,veritabanı işlemleri(ekleme,güncelleme,silme vb.)içerir.


class MainApp:
    def __init__(self, root):
        """
        Uygulamanın ana arayüzünü ve bileşenlerini tanımlar.
        """

        self.root = root
        self.root.title('Üye Yönetim Sistemi-Görsel Programlama')  # başlık
        self.root.geometry('1000x600')  # Uygulama boyutu
        self.root.configure(bg='#f4f4f4')  # Arka plan rengi açık gri yap

        # üye bilgileri çerçevesi
        frame_ust = ttk.LabelFrame(root, text="Üye Bilgileri", padding=(10, 10))
        frame_ust.grid(row=0, column=0, padx=10, pady=10, sticky="ew")  # üye bilgileri için alan

        # giriş alanları(TCKimlikNo,Ad,Soyad,CepTel,Eposta)
        ttk.Label(frame_ust, text='TCKimlikNo:').grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.tckimlik_entry = ttk.Entry(frame_ust)
        self.tckimlik_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_ust, text='Ad:').grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.ad_entry = ttk.Entry(frame_ust)
        self.ad_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame_ust, text='Soyad:').grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.soyad_entry = ttk.Entry(frame_ust)
        self.soyad_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(frame_ust, text='Meslek:').grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.meslek_entry = ttk.Entry(frame_ust)
        self.meslek_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(frame_ust, text='Cep Telefonu:').grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.ceptel_entry = ttk.Entry(frame_ust)
        self.ceptel_entry.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(frame_ust, text='Eposta:').grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.eposta_entry = ttk.Entry(frame_ust)
        self.eposta_entry.grid(row=5, column=1, padx=5, pady=5)

        ttk.Label(frame_ust, text='Adres:').grid(row=6, column=0, padx=5, pady=5, sticky="w")
        self.adres_entry = ttk.Entry(frame_ust)
        self.adres_entry.grid(row=6, column=1, padx=5, pady=5)

        # işlem butonlaru(ekle,bul,güncelle,sil,sil,listele)
        frame_butonlar = ttk.Frame(root, padding=(10, 10))
        frame_butonlar.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        ttk.Button(frame_butonlar, text="Ekle", command=self.ekle).grid(row=0, column=0, padx=10, pady=10)
        ttk.Button(frame_butonlar, text="Bul", command=self.bul).grid(row=0, column=1, padx=10, pady=10)
        self.guncelle_btn = ttk.Button(frame_butonlar, text="Güncelle", command=self.guncelle, state='disabled')
        self.guncelle_btn.grid(row=0, column=2, padx=10, pady=10)
        self.sil_btn = ttk.Button(frame_butonlar, text="Sil", command=self.sil, state='disabled')
        self.sil_btn.grid(row=0, column=3, padx=10, pady=10)
        ttk.Button(frame_butonlar, text="Listele", command=self.listele).grid(row=0, column=4, padx=10, pady=10)

        # listeleme alanı(treewiew)
        frame_liste = ttk.LabelFrame(root, text="Üye Listesi", padding=(10, 10))
        frame_liste.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        self.tree = ttk.Treeview(frame_liste,
                                 columns=("UyeID", "TCKimlikNo", "Ad", "Soyad", "Meslek", "CepTel", "Eposta", "Adres"),
                                 show="headings")
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(frame_liste, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")

        # treewiew sütun başlıkları
        self.tree.heading("UyeID", text="Üye ID")
        self.tree.heading("TCKimlikNo", text="TC Kimlik No")
        self.tree.heading("Ad", text="Ad")
        self.tree.heading("Soyad", text="Soyad")
        self.tree.heading("Meslek", text="Meslek")
        self.tree.heading("CepTel", text="Cep Telefonu")
        self.tree.heading("Eposta", text="E-posta")
        self.tree.heading("Adres", text="Adres")

        # treewiew sütun genişliklerini manuel olarak ayarlıyoruz
        self.tree.column("UyeID", width=100, anchor="center")
        self.tree.column("TCKimlikNo", width=150, anchor="center")
        self.tree.column("Ad", width=150, anchor="w")
        self.tree.column("Soyad", width=150, anchor="w")
        self.tree.column("Meslek", width=150, anchor="w")
        self.tree.column("CepTel", width=150, anchor="center")
        self.tree.column("Eposta", width=200, anchor="w")
        self.tree.column("Adres", width=200, anchor="w")

        root.grid_rowconfigure(2, weight=1)  # listeleme alanı için esneklik sağlıyoruz

        root.grid_columnconfigure(0, weight=1)  # listeleme alanı için esneklik sağlıyoruz
        frame_liste.grid_rowconfigure(0, weight=1)  # treewiew alanı için esneklik sağlıyoruz
        frame_liste.grid_columnconfigure(0, weight=1)  # treewiew sutünları giriş alanına aktar

        self.tree.bind("<<TreeviewSelect>>", self.kayit_secildi)

    def ekle(self):
        """
        Yeni üyeler ekler
        """
        tckimlik = self.tckimlik_entry.get()
        ad = self.ad_entry.get()
        soyad = self.soyad_entry.get()
        meslek = self.meslek_entry.get()
        ceptel = self.ceptel_entry.get()
        eposta = self.eposta_entry.get()
        adres = self.adres_entry.get()

        # TC Kimlik No ve Ceptel formatı kontrolü
        if not self.gecerli_tckimlik(tckimlik):
            messagebox.showerror("Hata", "Geçersiz TC Kimlik Numarası. 11 haneli olmalıdır")
            return
        if not self.gecerli_ceptel(ceptel):
            messagebox.showerror("Hata", "Geçersiz cep telefonu numarası. +90 ile başlayan ve 10 haneli olmalıdır.")
            return
        try:
            Uye.ekle(tckimlik, ad, soyad, meslek, ceptel, eposta, adres)  # Veritabanı ekleme işlemi
            messagebox.showinfo("Başarı", "Üye başarıyla eklendi.")
            self.temizle()
            self.listele()  # Listeyi güncelle
        except Exception as e:
            messagebox.showerror("Hata", str(e))

    def gecerli_tckimlik(self, tckimlik):
        """
        TC Kimlik Numarasının geçerli olup olmadığını kontrol eder (11 haneli ve rakam olabilir).
        """
        return tckimlik.isdigit() and len(tckimlik) == 11

    def gecerli_ceptel(self, ceptel):
        """
        Cep Telefonunun geçerli olup olmadığını kontrol eder (+90 ile başlayacak ve 10 rakam içermeli)
        """
        return bool(re.match(r"^\+90\d{10,15}$", ceptel))

    def gecerli_eposta(self, eposta):

        if '@' not in eposta or '.' not in eposta:
            return "Geçersiz e-posta adresi: '@' ve '.' karakterleri eksik."
        if eposta.index('@') > eposta.index('.'):
            return "Geçersiz e-posta adresi: '@' karakteri '.' karakterinden önce olamaz."
        return True

    def bul(self):
        """
        TC Kimlik Numarasına göre üye arar ve giriş alanlarını doldurur.
        """
        uye = Uye.bul(self.tckimlik_entry.get())  # Veritabanına arama yapıyoruz
        if uye:
            # Giriş alanlarını bulduğumuz üye bilgileriyle dolduruyoruz
            self.ad_entry.delete(0, tk.END)
            self.ad_entry.insert(0, uye[2])
            self.soyad_entry.delete(0, tk.END)
            self.soyad_entry.insert(0, uye[3])
            self.meslek_entry.delete(0, tk.END)
            self.meslek_entry.insert(0, uye[4])
            self.ceptel_entry.delete(0, tk.END)
            self.ceptel_entry.insert(0, uye[5])
            self.eposta_entry.delete(0, tk.END)
            self.eposta_entry.insert(0, uye[6])
            self.adres_entry.delete(0, tk.END)
            self.adres_entry.insert(0, uye[7])

            self.guncelle_btn.config(state='normal')  # Güncelle butonunu aktif yapıyoruz
            self.sil_btn.config(state='normal')  # Sil butonunu aktif yapıyoruz
        else:
            messagebox.showinfo("Bilgi", "Üye Bulunamadı.")  # Eğer üye bulunamazsa bilgi veriyoruz

    def guncelle(self):
        try:
            selected_item = self.tree.selection()[0]
            selected_data = self.tree.item(selected_item, 'values')
            Uye.guncelle(
                selected_data[0],
                self.tckimlik_entry.get(),
                self.ad_entry.get(),
                self.soyad_entry.get(),
                self.meslek_entry.get(),
                self.ceptel_entry.get(),
                self.eposta_entry.get(),
                self.adres_entry.get()
            )

        except Exception as e:
            messagebox.showerror("Hata", f"Güncelleme Başarısız{(e)}")

    def sil(self):
        """
        Seçilen üyenin kaydını siler.
        """
        try:
            Uye.sil(self.tckimlik_entry.get())  # Veritabanında silme işlemi
            messagebox.showinfo("Başarı", "Üye başarıyla silindi.")
            self.temizle()
            self.listele()  # Listeyi Güncelle
        except Exception as e:
            messagebox.showerror("Hata", f"Silme işlemi başarısız: {e}")

    def listele(self):
        """
        Tüm üyeleri listeler.
        """
        for row in self.tree.get_children():  # Önceden eklenmiş tüm verileri temizle
            self.tree.delete(row)
        uyeler = Uye.listele()  # Veritabanındaki tüm verileri listele
        for uye in uyeler:
            # Veriyi düzgün formatta Treeview'e ekleriz
            self.tree.insert("", tk.END, values=(
            str(uye[0]), str(uye[1]), str(uye[2]), str(uye[3]), str(uye[4]), str(uye[5]), str(uye[6]), str(uye[7])))

    def temizle(self):
        """
        Tüm giriş alanlarını temizler ve butonları devre dışı bırakır.
        """
        self.tckimlik_entry.delete(0, tk.END)
        self.ad_entry.delete(0, tk.END)
        self.soyad_entry.delete(0, tk.END)
        self.meslek_entry.delete(0, tk.END)
        self.ceptel_entry.delete(0, tk.END)
        self.eposta_entry.delete(0, tk.END)
        self.adres_entry.delete(0, tk.END)
        self.guncelle_btn.config(state='disabled')
        self.sil_btn.config(state='disabled')

    def kayit_secildi(self, event):
        """
        Treeview'dan seçilen kaydı giriş alanlarına doldurur
        """
        try:
            selected_item = self.tree.selection()[0]  # Seçilen kaydı alıyoruz
            selected_data = self.tree.item(selected_item, 'values')  # Kaydın verilerini alıyoruz
            # Verileri giriş alanlarına yerleştiriyoruz
            self.tckimlik_entry.delete(0, tk.END)
            self.tckimlik_entry.insert(0, selected_data[1])
            self.ad_entry.delete(0, tk.END)
            self.ad_entry.insert(0, selected_data[2])
            self.soyad_entry.delete(0, tk.END)
            self.soyad_entry.insert(0, selected_data[3])
            self.meslek_entry.delete(0, tk.END)
            self.meslek_entry.insert(0, selected_data[4])
            self.ceptel_entry.delete(0, tk.END)
            self.ceptel_entry.insert(0, selected_data[5])
            self.eposta_entry.delete(0, tk.END)
            self.eposta_entry.insert(0, selected_data[6])
            self.adres_entry.delete(0, tk.END)
            self.adres_entry.insert(0, selected_data[7])

            self.guncelle_btn.config(state='normal')  # Güncelle ve sil butonlarını aktif yapıyoruz
            self.sil_btn.config(state='normal')
        except IndexError:
            pass  # Eğer seçim yapılmamışsa herhangi bir işlem yapmayalım


if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
