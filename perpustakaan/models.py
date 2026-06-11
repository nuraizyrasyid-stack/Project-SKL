from django.db import models

class Buku(models.Model):
    
    judul = models.CharField(max_length=255)
    pengarang = models.CharField(max_length=255)
    kategori = models.CharField(max_length=100)
    penerbit = models.CharField(max_length=255)
    tahun_terbit = models.IntegerField()
    rak = models.CharField(max_length=100)
    stok = models.IntegerField()
    deskripsi = models.TextField()

    class Meta:
        db_table = 'buku'  
    def __str__(self):
        return self.judul


class Siswa(models.Model):
    nama = models.CharField(max_length=255)
    kelas = models.CharField(max_length=100)
    nis = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'siswa'

    def __str__(self):
        return self.nama


class Peminjaman(models.Model):
   
    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE, db_column='siswa_id')
    buku = models.ForeignKey(Buku, on_delete=models.CASCADE, db_column='buku_id')
    tanggal_pinjam = models.DateField()
    jatuh_tempo = models.DateField()
    keperluan = models.TextField()
    status = models.CharField(max_length=50, default='Dipinjam')

    class Meta:
        db_table = 'peminjaman'
