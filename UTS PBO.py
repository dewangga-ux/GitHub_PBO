class Dokumen:
    def __init__(self, nama, jumlah_halaman):
        self.nama = nama
        self.jumlah_halaman = jumlah_halaman

class Pelanggan:
    def __init__(self, nama, saldo_awal):
        self.nama = nama
        self.__saldo = float(saldo_awal)

    @property
    def saldo(self):
        return self.__saldo

    def kurangi_saldo(self, jumlah):
        if jumlah <= self.__saldo:
            self.__saldo -= jumlah
            return True
        return False

class MesinPrint:
    def __init__(self, stok_kertas):
        self.stok_kertas = stok_kertas
        self.__harga_per_lembar = 500.0

    def proses_cetak(self, pelanggan, dokumen):
        total_biaya = dokumen.jumlah_halaman * self.__harga_per_lembar
        
        print(f"--- Transaksi: {pelanggan.nama} mencetak {dokumen.nama} ---")

        # 1. Validasi Saldo
        if pelanggan.saldo < total_biaya:
            print(f"Gagal: Saldo Rp{pelanggan.saldo} tidak cukup untuk biaya Rp{total_biaya}")
            return

        # 2. Proses Pembayaran (Pemotongan Saldo)
        sukses = pelanggan.kurangi_saldo(total_biaya)
        
        if sukses:
            self.stok_kertas -= dokumen.jumlah_halaman
            print(f"Pembayaran Berhasil! Saldo terpotong: Rp{total_biaya}")
            print(f"Sisa Saldo {pelanggan.nama}: Rp{pelanggan.saldo}")
            print(f"Sisa Kertas Mesin: {self.stok_kertas}")

# --- Eksekusi Pembayaran ---
if __name__ == "__main__":
    mesin = MesinPrint(stok_kertas=50)
    andi = Pelanggan("Andi", 5000.0)
    tugas = Dokumen("Tugas_Python.pdf", 4) # Biaya: 4 * 500 = 2000

    mesin.proses_cetak(andi, tugas)