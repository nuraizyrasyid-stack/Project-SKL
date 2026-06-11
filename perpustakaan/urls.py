from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    
    path('buku/', views.buku_list, name='buku_list'),
    path('buku/tambah/', views.buku_tambah, name='buku_tambah'),
    path('buku/detail/<int:buku_id>/', views.buku_detail, name='buku_detail'),
    path('buku/edit/<int:pk>/', views.buku_edit, name='buku_edit'),
    path('buku/hapus/<int:pk>/', views.buku_hapus, name='buku_hapus'),
    path('siswa/', views.siswa_list, name='siswa_list'),
    path('siswa/tambah/', views.siswa_tambah, name='siswa_tambah'),
    path('siswa/detail/<int:pk>/', views.siswa_detail, name='siswa_detail'),
    path('siswa/edit/<int:pk>/', views.siswa_edit, name='siswa_edit'),
    path('siswa/hapus/<int:pk>/', views.siswa_hapus, name='siswa_hapus'),
    path('peminjaman/', views.peminjaman_list, name='peminjaman_list'),
    path('peminjaman/tambah/', views.peminjaman_tambah, name='peminjaman_tambah'),
    path('peminjaman/kembalikan/<int:pk>/', views.peminjaman_kembalikan, name='peminjaman_kembalikan'),
]