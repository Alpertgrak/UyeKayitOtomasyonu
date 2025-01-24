import pyodbc

# Veritabanı bağlantı bilgileri
SERVER = 'ALPERTGRAK' # MSSQL Sunucu Adı
DATABASE = 'KutuphaneDB1' # Veritabanı Adı

# Veritabanına bağlanmak için bağlantı dizesini döndürür
def get_connection():
    """
    Veritabanına bağlanır ve bağlantı nesnesini döndürür.
    """

    connection = pyodbc.connect(
        f'DRIVER={{SQL Server}};'
        f'SERVER={SERVER};'
        f'DATABASE={DATABASE};'
        'Trusted_Connection=yes;' # Windows kimlik doğrulaması kullanılır
    )
    return connection