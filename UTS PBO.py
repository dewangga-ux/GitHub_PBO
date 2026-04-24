class Dokumen:
    def __init__(self, nama, jumlah_halaman):
        self.nama = nama
        self.jumlah_halaman = jumlah_halaman

class Pelanggan:
    def __init__(self, nama, saldo_awal):
        self.nama = nama
        # Enkapsulasi: Menggunakan __ untuk mensimulasikan private property
        self.__saldo = float(saldo_awal)

    @property
    def saldo(self):
        """Getter untuk melihat saldo tanpa bisa mengubahnya secara langsung"""
        return self.__saldo

    def kurangi_saldo(self, jumlah):
        """Fungsi internal untuk validasi pemotongan saldo"""
        if jumlah <= self.__saldo:
            self.__saldo -= jumlah
            return True
        return False

    def top_up(self, jumlah):
        if jumlah > 0:
            self.__saldo += jumlah
            print(f"[TopUp] Berhasil menambah saldo. Saldo sekarang: Rp{self.__saldo}")

class MesinPrint:
    def __init__(self, stok_kertas, level_tinta):
        self.stok_kertas = stok_kertas
        self.level_tinta = level_tinta
        self.__harga_per_lembar = 500.0

    def proses_cetak(self, pelanggan, dokumen):
        print(f"\n--- Memulai Proses Cetak: {dokumen.nama} ---")
        
        total_biaya = dokumen.jumlah_halaman * self.__harga_per_lembar

        # 1. Validasi Ketersediaan Kertas
        if self.stok_kertas < dokumen.jumlah_halaman:
            print(f"[ERROR] Gagal: Stok kertas tidak cukup! (Sisa: {self.stok_kertas} lembar)")
            return

        # 2. Validasi Tinta
        if self.level_tinta < dokumen.jumlah_halaman:
            print("[ERROR] Gagal: Level tinta terlalu rendah!")
            return

        # 3. Validasi Saldo Pelanggan
        if pelanggan.saldo < total_biaya:
            print(f"[ERROR] Gagal: Saldo tidak mencukupi! (Butuh: Rp{total_biaya}, Saldo: Rp{pelanggan.saldo})")
            return

        # Eksekusi jika semua validasi lolos
        sukses_potong_saldo = pelanggan.kurangi_saldo(total_biaya)
        if sukses_potong_saldo:
            self.stok_kertas -= dokumen.jumlah_halaman
            self.level_tinta -= dokumen.jumlah_halaman
            print(f"[SUKSES] Dokumen '{dokumen.nama}' berhasil dicetak.")
            print(f"[INFO] Biaya: Rp{total_biaya} | Sisa Saldo: Rp{pelanggan.saldo}")
            print(f"[INFO] Sisa Kertas: {self.stok_kertas} | Sisa Tinta: {self.level_tinta}")

# --- Simulasi Main ---
if __name__ == "__main__":
    # Instansiasi Objek
    mesin = MesinPrint(stok_kertas=10, level_tinta=100)
    user_andi = Pelanggan("Andi", 2000.0)
    
    doc_skripsi = Dokumen("Skripsi_Final.pdf", 15)
    doc_tugas = Dokumen("Tugas_Matkul.pdf", 3)

    # --- SIMULASI GAGAL 1: Saldo/Kertas Kurang ---
    print(">>> Simulasi 1: Mencoba cetak dokumen besar")
    mesin.proses_cetak(user_andi, doc_skripsi) 

    # --- SIMULASI SUKSES ---
    print("\n>>> Simulasi 2: Mencoba cetak dokumen kecil")
    mesin.proses_cetak(user_andi, doc_tugas)

    # --- SIMULASI GAGAL 2: Stok Kertas Habis ---
    doc_laporan = Dokumen("Laporan.pdf", 8)
    print("\n>>> Simulasi 3: Mencoba cetak melebihi stok kertas")
    mesin.proses_cetak(user_andi, doc_laporan)

    # --- PEMBUKTIAN ENKAPSULASI ---
    # print(user_andi.__saldo) # Ini akan menyebabkan AttributeError
    # user_andi.saldo = 1000000.0 # Ini akan menyebabkan AttributeError/Error karena tidak ada setter