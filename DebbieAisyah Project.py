from datetime import datetime, timedelta

# Inisialisasi data
buku = {
    'B001': {'judul': 'Alastair Owns Me', 'penulis': 'Nisaafatm', 'stok': 3},
    'B002': {'judul': 'Alaska', 'penulis': 'Nisaafatm', 'stok': 2},
    'B003': {'judul': 'Abraxas', 'penulis': 'Nur Alisa', 'stok': 1},
    'B004': {'judul': 'Dia Angkasa', 'penulis': 'Nurwina Sari', 'stok': 4}
}
anggota = {}
peminjaman = {}
denda_per_hari = 2000
batas_hari_pinjam = 7

def syarat_peminjaman():
    print("\n=== SYARAT PEMINJAMAN ===")
    print("1. Harus terdaftar sebagai anggota")
    print("2. Maksimal peminjaman 2 buku")
    print("3. Durasi peminjaman maksimal 7 hari")
    print("4. Denda keterlambatan Rp 2.000/hari")
    print("5. Kerusakan/kehilangan buku akan dikenakan denda")

def daftar_anggota(id_anggota, nama, alamat):
    if id_anggota not in anggota:
        anggota[id_anggota] = {
            'nama': nama,
            'alamat': alamat,
            'buku_dipinjam': []
        }
        print(f"Anggota dengan ID {id_anggota} berhasil didaftarkan")
    else:
        print("ID Anggota sudah terdaftar!")

def lihat_anggota():
    print("\n=== DAFTAR ANGGOTA ===")
    if not anggota:
        print("Belum ada anggota terdaftar")
        return
    for id_anggota, data in anggota.items():
        print(f"ID: {id_anggota}")
        print(f"Nama: {data['nama']}")
        print(f"Alamat: {data['alamat']}")
        print(f"Buku dipinjam: {', '.join(data['buku_dipinjam'])}")
        print("-" * 30)

def tambah_buku(id_buku, judul, penulis, stok):
    if id_buku not in buku:
        buku[id_buku] = {
            'judul': judul,
            'penulis': penulis,
            'stok': stok
        }
        print(f"Buku {judul} berhasil ditambahkan")
    else:
        print("ID Buku sudah ada!")

def edit_buku(id_buku, judul, penulis, stok):
    if id_buku in buku:
        buku[id_buku] = {
            'judul': judul,
            'penulis': penulis,
            'stok': stok
        }
        print(f"Buku dengan ID {id_buku} berhasil diupdate")
    else:
        print("ID Buku tidak ditemukan!")

def hapus_buku(id_buku):
    if id_buku in buku:
        del buku[id_buku]
        print(f"Buku dengan ID {id_buku} berhasil dihapus")
    else:
        print("ID Buku tidak ditemukan!")

def lihat_buku():
    print("\n=== DAFTAR BUKU ===")
    for id_buku, data in buku.items():
        print(f"ID: {id_buku}")
        print(f"Judul: {data['judul']}")
        print(f"Penulis: {data['penulis']}")
        print(f"Stok: {data['stok']}")
        print("-" * 30)

def hitung_denda(tanggal_pinjam, tanggal_kembali):
    """Menghitung denda keterlambatan pengembalian buku."""
    try:
        tgl_pinjam = datetime.strptime(tanggal_pinjam, '%Y-%m-%d')
        tgl_kembali = datetime.strptime(tanggal_kembali, '%Y-%m-%d')
        batas_kembali = tgl_pinjam + timedelta(days=batas_hari_pinjam)
        
        if tgl_kembali <= batas_kembali:
            return 0
        else:
            hari_terlambat = (tgl_kembali - batas_kembali).days
            return hari_terlambat * denda_per_hari
    except ValueError:
        print("Format tanggal tidak valid! Gunakan format YYYY-MM-DD")
        return None

def pinjam_buku(id_anggota, id_buku, tanggal_pinjam):
    if id_anggota not in anggota:
        print("Anggota tidak ditemukan!")
        return
    if id_buku not in buku:
        print("Buku tidak ditemukan!")
        return
    if len(anggota[id_anggota]['buku_dipinjam']) >= 2:
        print("Anggota sudah meminjam maksimal buku!")
        return
    if buku[id_buku]['stok'] <= 0:
        print("Stok buku habis!")
        return
    
    try:
        # Validasi format tanggal
        datetime.strptime(tanggal_pinjam, '%Y-%m-%d')
    except ValueError:
        print("Format tanggal tidak valid! Gunakan format YYYY-MM-DD")
        return

    # Proses peminjaman
    peminjaman[f"{id_anggota}-{id_buku}"] = {
        'tanggal_pinjam': tanggal_pinjam,
        'tanggal_kembali': None,
        'status': 'Dipinjam',
        'denda': 0
    }
    buku[id_buku]['stok'] -= 1
    anggota[id_anggota]['buku_dipinjam'].append(id_buku)
    
    # Tampilkan informasi batas pengembalian
    tgl_pinjam = datetime.strptime(tanggal_pinjam, '%Y-%m-%d')
    batas_kembali = tgl_pinjam + timedelta(days=batas_hari_pinjam)
    print("Peminjaman berhasil!")
    print(f"Batas pengembalian: {batas_kembali.strftime('%Y-%m-%d')}")

def kembalikan_buku(id_anggota, id_buku, tanggal_kembali):
    kode_pinjam = f"{id_anggota}-{id_buku}"
    if kode_pinjam not in peminjaman:
        print("Data peminjaman tidak ditemukan!")
        return

    # Hitung denda
    tanggal_pinjam = peminjaman[kode_pinjam]['tanggal_pinjam']
    denda = hitung_denda(tanggal_pinjam, tanggal_kembali)
    
    if denda is None:
        return
    
    # Proses pengembalian
    peminjaman[kode_pinjam]['tanggal_kembali'] = tanggal_kembali
    peminjaman[kode_pinjam]['status'] = 'Dikembalikan'
    peminjaman[kode_pinjam]['denda'] = denda
    buku[id_buku]['stok'] += 1
    anggota[id_anggota]['buku_dipinjam'].remove(id_buku)

    print("Pengembalian berhasil!")
    if denda > 0:
        print(f"Denda keterlambatan: Rp {denda:,}")
    else:
        print("Tidak ada denda keterlambatan")

def lihat_peminjaman():
    print("\n=== DAFTAR PEMINJAMAN ===")
    if not peminjaman:
        print("Belum ada data peminjaman")
        return
    for kode, data in peminjaman.items():
        id_anggota, id_buku = kode.split('-')
        print(f"Anggota: {anggota[id_anggota]['nama']}")
        print(f"Buku: {buku[id_buku]['judul']}")
        print(f"Tanggal Pinjam: {data['tanggal_pinjam']}")
        print(f"Tanggal Kembali: {data['tanggal_kembali'] if data['tanggal_kembali'] else 'Belum dikembalikan'}")
        print(f"Status: {data['status']}")
        if data['status'] == 'Dikembalikan' and 'denda' in data:
            print(f"Denda: Rp {data['denda']:,}")
        print("-" * 30)

def menu_petugas():
    while True:
        print("\n=== MENU PETUGAS ===")
        print("1. Tambah Buku")
        print("2. Edit Buku")
        print("3. Hapus Buku")
        print("4. Lihat Daftar Buku")
        print("5. Lihat Daftar Anggota")
        print("6. Lihat Peminjaman")
        print("7. Kembali")
        
        pilihan = input("Pilih menu (1-7): ")
        
        if pilihan == '1':
            id_buku = input("Masukkan ID Buku: ")
            judul = input("Masukkan Judul: ")
            penulis = input("Masukkan Penulis: ")
            stok = int(input("Masukkan Stok: "))
            tambah_buku(id_buku, judul, penulis, stok)
        elif pilihan == '2':
            id_buku = input("Masukkan ID Buku: ")
            judul = input("Masukkan Judul Baru: ")
            penulis = input("Masukkan Penulis Baru: ")
            stok = int(input("Masukkan Stok Baru: "))
            edit_buku(id_buku, judul, penulis, stok)
        elif pilihan == '3':
            id_buku = input("Masukkan ID Buku: ")
            hapus_buku(id_buku)
        elif pilihan == '4':
            lihat_buku()
        elif pilihan == '5':
            lihat_anggota()
        elif pilihan == '6':
            lihat_peminjaman()
        elif pilihan == '7':
            break
        else:
            print("Pilihan tidak valid!")

def menu_peminjam():
    while True:
        print("\n=== MENU PEMINJAM ===")
        print("1. Daftar Anggota")
        print("2. Lihat Daftar Buku")
        print("3. Pinjam Buku")
        print("4. Kembalikan Buku")
        print("5. Lihat Syarat Peminjaman")
        print("6. Kembali")
        
        pilihan = input("Pilih menu (1-6): ")
        
        if pilihan == '1':
            id_anggota = input("Masukkan ID Anggota: ")
            nama = input("Masukkan Nama: ")
            alamat = input("Masukkan Alamat: ")
            daftar_anggota(id_anggota, nama, alamat)
        elif pilihan == '2':
            lihat_buku()
        elif pilihan == '3':
            id_anggota = input("Masukkan ID Anggota: ")
            id_buku = input("Masukkan ID Buku: ")
            tanggal_pinjam = input("Masukkan Tanggal Pinjam (YYYY-MM-DD): ")
            pinjam_buku(id_anggota, id_buku, tanggal_pinjam)
        elif pilihan == '4':
            id_anggota = input("Masukkan ID Anggota: ")
            id_buku = input("Masukkan ID Buku: ")
            tanggal_kembali = input("Masukkan Tanggal Kembali (YYYY-MM-DD): ")
            kembalikan_buku(id_anggota, id_buku, tanggal_kembali)
        elif pilihan == '5':
            syarat_peminjaman()
        elif pilihan == '6':
            break
        else:
            print("Pilihan tidak valid!")

def main():
    while True:
        print("\n=== SISTEM PERPUSTAKAAN ===")
        print("1. Menu Petugas")
        print("2. Menu Peminjam")
        print("3. Keluar")
        
        pilihan = input("Pilih menu (1-3): ")
        
        if pilihan == '1':
            menu_petugas()
        elif pilihan == '2':
            menu_peminjam()
        elif pilihan == '3':
            print("Terima kasih telah menggunakan sistem perpustakaan!")
            break
        else:
            print("Pilihan tidak valid!")

if __name__ == "__main__":
    main()