/**
 * Sistem Layanan Fotokopi Mandiri (ITK-Print)
 * Mengimplementasikan Enkapsulasi Mutlak dan Custom Validation
 */

class Dokumen(val nama: String, val jumlahHalaman: Int)

class Pelanggan(val nama: String, saldoAwal: Double) {
    // Enkapsulasi: Saldo tidak bisa diubah langsung dari luar (private set)
    var saldo: Double = saldoAwal
        private set

    fun kurangiSaldo(jumlah: Double): Boolean {
        if (jumlah <= saldo) {
            saldo -= jumlah
            return true
        }
        return false
    }

    fun topUp(jumlah: Double) {
        if (jumlah > 0) {
            saldo += jumlah
            println("[TopUp] Berhasil menambah saldo. Saldo sekarang: Rp$saldo")
        }
    }
}

class MesinPrint(var stokKertas: Int, var levelTinta: Int) {
    private val hargaPerLembar: Double = 500.0

    // Fungsi utama sebagai "Jalur Resmi" sesuai Aturan Bisnis
    fun prosesCetak(pelanggan: Pelanggan, dokumen: Dokumen) {
        println("\n--- Memulai Proses Cetak: ${dokumen.nama} ---")
        
        val totalBiaya = dokumen.jumlahHalaman * hargaPerLembar

        // 1. Validasi Ketersediaan Kertas
        if (stokKertas < dokumen.jumlahHalaman) {
            println("[ERROR] Gagal: Stok kertas tidak cukup! (Sisa: $stokKertas lembar)")
            return
        }

        // 2. Validasi Tinta (Asumsi 1 halaman butuh 1 unit tinta)
        if (levelTinta < dokumen.jumlahHalaman) {
            println("[ERROR] Gagal: Level tinta terlalu rendah!")
            return
        }

        // 3. Validasi Saldo Pelanggan
        if (pelanggan.saldo < totalBiaya) {
            println("[ERROR] Gagal: Saldo tidak mencukupi! (Butuh: Rp$totalBiaya, Saldo: Rp${pelanggan.saldo})")
            return
        }

        // Eksekusi jika semua validasi lolos
        val suksesPotongSaldo = pelanggan.kurangiSaldo(totalBiaya)
        if (suksesPotongSaldo) {
            stokKertas -= dokumen.jumlahHalaman
            levelTinta -= dokumen.jumlahHalaman
            println("[SUKSES] Dokumen '${dokumen.nama}' berhasil dicetak.")
            println("[INFO] Biaya: Rp$totalBiaya | Sisa Saldo: Rp${pelanggan.saldo}")
            println("[INFO] Sisa Kertas: $stokKertas | Sisa Tinta: $levelTinta")
        }
    }
}

fun main() {
    // Instansiasi Objek
    val mesin = MesinPrint(stokKertas = 10, levelTinta = 100)
    val userAndi = Pelanggan("Andi", 2000.0) // Saldo awal 2000
    
    val docSkripsi = Dokumen("Skripsi_Final.pdf", 15)
    val docTugas = Dokumen("Tugas_Matkul.pdf", 3)

    // --- SIMULASI GAGAL 1: Saldo Kurang ---
    // (Harga 3 lembar = 1500, saldo 2000 masih cukup, tapi mari coba yang 15 halaman)
    println(">>> Simulasi 1: Mencoba cetak dokumen besar (Saldo/Kertas mungkin kurang)")
    mesin.prosesCetak(userAndi, docSkripsi) 

    // --- SIMULASI SUKSES ---
    println("\n>>> Simulasi 2: Mencoba cetak dokumen kecil (Saldo cukup)")
    mesin.prosesCetak(userAndi, docTugas)

    // --- SIMULASI GAGAL 2: Stok Kertas Habis ---
    // Setelah cetak 3 lembar, sisa kertas adalah 7. Kita coba cetak 8 lembar.
    val docLaporan = Dokumen("Laporan.pdf", 8)
    println("\n>>> Simulasi 3: Mencoba cetak melebihi stok kertas")
    mesin.prosesCetak(userAndi, docLaporan)

    // --- PEMBUKTIAN ENKAPSULASI ---
    // userAndi.saldo = 1000000.0 // ERROR: Cannot assign to 'saldo' because it is private in 'Pelanggan'
    // mesin.hargaPerLembar = 10.0 // ERROR: Property is private/val
}