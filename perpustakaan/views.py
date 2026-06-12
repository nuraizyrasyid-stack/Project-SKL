from django.shortcuts import render, redirect
from django.db import connection
from datetime import datetime, timedelta

def dict_fetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def dict_fetchone(cursor):
    columns = [col[0] for col in cursor.description]
    row = cursor.fetchone()
    if row:
        return dict(zip(columns, row))
    return None

def index(request):
    with connection.cursor() as cursor:
        
        cursor.execute("SELECT COALESCE(SUM(stok), 0) FROM buku")
        total_buku = cursor.fetchone()[0]
        
      
        cursor.execute("SELECT COUNT(*) FROM buku")
        total_judul = cursor.fetchone()[0]
        
       
        cursor.execute("SELECT COUNT(*) FROM peminjaman WHERE status = 'Dipinjam'")
        sedang_dipinjam = cursor.fetchone()[0]
        
     
        cursor.execute("SELECT COUNT(*) FROM peminjaman WHERE status = 'Selesai'")
        sudah_dikembalikan = cursor.fetchone()[0]
        
       
        cursor.execute("SELECT judul, stok FROM buku ORDER BY stok DESC LIMIT 6")
        buku_stok = dict_fetchall(cursor)
        
        distribusi_stok = []
        for b in buku_stok:
            persentase = (b['stok'] / total_buku) * 100 if total_buku > 0 else 0
            distribusi_stok.append({
                'judul': b['judul'],
                'stok': b['stok'],
                'persentase': round(persentase)
            })

   
    return render(request, 'index.html', {
        'total_buku': total_buku,
        'total_judul': total_judul,
        'sedang_dipinjam': sedang_dipinjam,
        'sudah_dikembalikan': sudah_dikembalikan,
        'distribusi_stok': distribusi_stok,
    })

def buku_list(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, judul, pengarang, kategori, penerbit, tahun_terbit, rak, stok 
            FROM buku ORDER BY id DESC
        """)
        
        list_buku = dict_fetchall(cursor) 
    
    return render(request, 'buku/buku_list.html', {'list_buku': list_buku})
def buku_tambah(request):
    if request.method == 'POST':
        judul = request.POST.get('judul')
        pengarang = request.POST.get('pengarang')
        kategori = request.POST.get('kategori')
        penerbit = request.POST.get('penerbit')
        tahun = request.POST.get('tahun_terbit')
        rak = request.POST.get('rak')
        stok = request.POST.get('stok')
        deskripsi = request.POST.get('deskripsi')
        isbn = request.POST.get('isbn')
        
        with connection.cursor() as cursor:
           
            cursor.execute("""
                INSERT INTO buku (judul, pengarang, kategori, penerbit, tahun_terbit, rak, stok, deskripsi, isbn)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, [judul, pengarang, kategori, penerbit, tahun, rak, stok, deskripsi, isbn])
            
        return redirect('buku_list')
        
    return render(request, 'buku/buku_tambah.html')

from django.http import Http404

def buku_detail(request, buku_id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, judul, pengarang, kategori, penerbit, tahun_terbit, isbn, rak, stok, deskripsi 
            FROM buku WHERE id = %s
        """, [buku_id])
        
        data = dict_fetchall(cursor)
        if not data:
            raise Http404("Buku tidak ditemukan.")
        
        buku = data[0]
        
    return render(request, 'buku/buku_detail.html', {'buku': buku})

def buku_edit(request, pk):
    if request.method == 'POST':
        judul = request.POST.get('judul')
        pengarang = request.POST.get('pengarang')
        kategori = request.POST.get('kategori')
        penerbit = request.POST.get('penerbit')
        tahun_terbit = request.POST.get('tahun_terbit')
        rak = request.POST.get('rak')
        stok = request.POST.get('stok')
        deskripsi = request.POST.get('deskripsi')
        isbn = request.POST.get('isbn')

        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE buku SET 
                    judul = %s, pengarang = %s, kategori = %s, penerbit = %s,
                    tahun_terbit = %s, rak = %s, stok = %s, deskripsi = %s,  isbn = %s
                WHERE id = %s
            """, [judul, pengarang, kategori, penerbit, tahun_terbit, rak, stok, deskripsi, isbn, pk])
        return redirect('buku_list')
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM buku WHERE id = %s", [pk])
        buku = dict_fetchone(cursor)
    if not buku:
        return redirect('buku_list')
    pilihan_kategori = ['Novel', 'Sejarah', 'Pendidikan']
    pilihan_rak = ['Rak A-01', 'Rak A-02', 'Rak A-03', 'Rak A-04', 'Rak A-05']
    return render(request, 'buku/buku_edit.html', {
        'buku': buku,
        'pilihan_kategori': pilihan_kategori,
        'pilihan_rak': pilihan_rak
    })

def buku_hapus(request, pk):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM buku WHERE id = %s", [pk])
        return redirect('buku_list')
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, judul FROM buku WHERE id = %s", [pk])
        buku = dict_fetchone(cursor)
    if not buku:
        return redirect('buku_list')
    return render(request, 'buku/buku_hapus.html', {'buku': buku})

def siswa_list(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, nama, kelas, nis, is_active FROM siswa ORDER BY id DESC")
        daftar_siswa = dict_fetchall(cursor)
    return render(request, 'siswa/siswa_list.html', {'daftar_siswa': daftar_siswa})

def siswa_tambah(request):
    if request.method == 'POST':
        nama = request.POST.get('nama')
        kelas = request.POST.get('kelas')
        nis = request.POST.get('nis')
        is_active = request.POST.get('is_active') == 'True'
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO siswa (nama, kelas, nis, is_active) 
                VALUES (%s, %s, %s, %s)
            """, [nama, kelas, nis, is_active])
        return redirect('siswa_list')
    return render(request, 'siswa/siswa_form.html')

def siswa_detail(request, pk):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, nama, kelas, nis, is_active FROM siswa WHERE id = %s", [pk])
        siswa = dict_fetchone(cursor)
    if not siswa:
        return redirect('siswa_list')
    return render(request, 'siswa/siswa_detail.html', {'siswa': siswa})

def siswa_edit(request, pk):
    if request.method == 'POST':
        nama = request.POST.get('nama')
        kelas = request.POST.get('kelas')
        nis = request.POST.get('nis')
        is_active = request.POST.get('is_active') == 'True'
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE siswa 
                SET nama = %s, kelas = %s, nis = %s, is_active = %s 
                WHERE id = %s
            """, [nama, kelas, nis, is_active, pk])
        return redirect('siswa_list')
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, nama, kelas, nis, is_active FROM siswa WHERE id = %s", [pk])
        siswa = dict_fetchone(cursor)
    if not siswa:
        return redirect('siswa_list')
    return render(request, 'siswa/siswa_edit.html', {'siswa': siswa})

def siswa_hapus(request, pk):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM siswa WHERE id = %s", [pk])
        return redirect('siswa_list')
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, nama FROM siswa WHERE id = %s", [pk])
        siswa = dict_fetchone(cursor)
    if not siswa:
        return redirect('siswa_list')
    return render(request, 'siswa/siswa_hapus.html', {'siswa': siswa})

def peminjaman_list(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                p.id,
                s.nama AS nama_siswa,
                b.judul AS judul_buku,
                p.tanggal_pinjam,
                p.jatuh_tempo AS tanggal_kembali,
                p.keperluan,
                'Budi Siregar' AS nama_petugas,
                CASE 
                    WHEN p.status = 'Selesai' THEN TRUE 
                    ELSE FALSE 
                END AS status_kembali
            FROM peminjaman p
            LEFT JOIN siswa s ON CAST(p.siswa_id AS VARCHAR) = CAST(s.id AS VARCHAR)
            LEFT JOIN buku b ON CAST(p.buku_id AS VARCHAR) = CAST(b.id AS VARCHAR)
            ORDER BY p.id DESC
        """)
        hasil_query = dict_fetchall(cursor)
        
    return render(request, 'peminjaman/pinjam_list.html', {
        'list_peminjaman': hasil_query,
        'daftar_pinjam': hasil_query
    })
def peminjaman_tambah(request):
    if request.method == 'POST':
        siswa_id = request.POST.get('siswa_id')
        buku_id = request.POST.get('buku_id')
        tanggal_pinjam = request.POST.get('tanggal_pinjam')
        jatuh_tempo = request.POST.get('tanggal_kembali')
        keperluan = request.POST.get('keperluan')
        status = 'Dipinjam'
        
        if siswa_id and buku_id:
            siswa_id = int(siswa_id)
            buku_id = int(buku_id)
            
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO peminjaman (siswa_id, buku_id, tanggal_pinjam, jatuh_tempo, keperluan, status)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, [siswa_id, buku_id, tanggal_pinjam, jatuh_tempo, keperluan, status])
                
                cursor.execute("""
                    UPDATE buku 
                    SET stok = stok - 1 
                    WHERE id = %s
                """, [buku_id])
                
            return redirect('peminjaman_list')

    with connection.cursor() as cursor:
        cursor.execute("SELECT id, nama, kelas, nis FROM siswa WHERE is_active = True ORDER BY nama ASC")
        daftar_siswa = dict_fetchall(cursor)
        
        cursor.execute("SELECT id, judul, stok FROM buku WHERE stok > 0 ORDER BY judul ASC")
        daftar_buku = dict_fetchall(cursor)
        
    tanggal_hari_ini = datetime.now().date()
    tanggal_kembali = tanggal_hari_ini + timedelta(days=7)
    
    
    return render(request, 'peminjaman/pinjam_tambah.html', {
        'daftar_siswa': daftar_siswa,
        'daftar_buku': daftar_buku,
        'hari_ini': tanggal_hari_ini.strftime('%Y-%m-%d'),
        'kembali': tanggal_kembali.strftime('%Y-%m-%d')
    })
def peminjaman_kembalikan(request, pk):
    with connection.cursor() as cursor:
        cursor.execute("SELECT buku_id, status FROM peminjaman WHERE id = %s", [pk])
        peminjaman = dict_fetchone(cursor)
        
        if peminjaman and peminjaman['status'] == 'Dipinjam':
            cursor.execute("UPDATE peminjaman SET status = 'Selesai' WHERE id = %s", [pk])
            cursor.execute("UPDATE buku SET stok = stok + 1 WHERE id = %s", [peminjaman['buku_id']])
            
    return redirect('peminjaman_list')