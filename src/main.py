import sys
from pathlib import Path

# Memastikan direktori src dan root dapat diimpor dengan lancar
CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

try:
    from .exceptions import (
        KosError,
        TarifInvalidError,
        ListrikInvalidError,
        DurasiKontrakInvalidError,
        TagihanLunasError,
    )
    from .kamar import Kamar, KamarStandar, KamarAC
    from .kontrak import Penghuni, Kontrak
except ImportError:
    from exceptions import (
        KosError,
        TarifInvalidError,
        ListrikInvalidError,
        DurasiKontrakInvalidError,
        TagihanLunasError,
    )
    from kamar import Kamar, KamarStandar, KamarAC
    from kontrak import Penghuni, Kontrak


def separator(judul):
    print(f"\n{'=' * 20} {judul} {'=' * 20}")


def main():
    separator("SKENARIO 1: ALUR NORMAL (HAPPY PATH)")
    # Menunjukkan alur tanpa error: blok try -> blok else -> blok finally
    kontrak_aktif = None
    try:
        print("[TRY] Memproses pembuatan data kos dan transaksi...")
        penghuni = Penghuni("Ayu Lestari")
        standar = KamarStandar.dari_nomor("A01")
        ac = KamarAC("A02")
        ac.kwh = 80  # Penggunaan listrik valid

        kontrak_aktif = Kontrak(penghuni, ac, "November 2026", 6)
        tagihan = kontrak_aktif.tagihan[0]

        print(f"  - {penghuni}")
        print(f"  - Kamar Terpilih : {ac} (Total: Rp{ac.hitung_tarif():,})")
        print(f"  - Kamar Lain     : {standar} (Total: Rp{standar.hitung_tarif():,})")
        print(f"  - Status Tagihan : {tagihan}")

        print("  - Melakukan pembayaran tagihan pertama...")
        tagihan.bayar()
        print(f"  - Status Akhir   : {tagihan}")

    except KosError as err:
        print(f"[EXCEPT] Terjadi kesalahan sistem kos: {err}")
    else:
        print("[ELSE] Transaksi berhasil tanpa pengecualian (tidak ada error).")
    finally:
        print("[FINALLY] Blok pembersihan / pencatatan log Skenario 1 selesai dijalankan.")

    separator("SKENARIO 2: ATURAN BISNIS 1 - TARIF TIDAK VALID")
    # Aturan 1: Tarif kamar harus bilangan positif (> 0)
    try:
        print("[TRY] Mencoba membuat Kamar dengan tarif tidak valid (Rp -500.000)...")
        _ = Kamar("X99", -500_000)
    except TarifInvalidError as err:
        print(f"[EXCEPT - TarifInvalidError] Berhasil tertangkap: {err}")
    except KosError as err:
        print(f"[EXCEPT - KosError] Error umum: {err}")
    else:
        print("[ELSE] Kamar berhasil dibuat (seharusnya tidak tercapai).")
    finally:
        print("[FINALLY] Validasi tarif kamar selesai diperiksa.")

    separator("SKENARIO 3: ATURAN BISNIS 2 - PEMAKAIAN LISTRIK NEGATIF")
    # Aturan 2: Pemakaian kWh tidak boleh bernilai negatif (< 0)
    try:
        print("[TRY] Mencoba menetapkan pemakaian listrik negatif (-15 kWh)...")
        kamar_uji = KamarAC("B01")
        kamar_uji.kwh = -15
    except ListrikInvalidError as err:
        print(f"[EXCEPT - ListrikInvalidError] Berhasil tertangkap: {err}")
    except KosError as err:
        print(f"[EXCEPT - KosError] Error umum: {err}")
    else:
        print("[ELSE] Pemakaian kWh berhasil diubah (seharusnya tidak tercapai).")
    finally:
        print("[FINALLY] Validasi kWh listrik selesai diperiksa.")

    separator("SKENARIO 4: ATURAN BISNIS 3 - DURASI KONTRAK KURANG DARI 1 BULAN")
    # Aturan 3: Durasi kontrak minimal 1 bulan
    try:
        print("[TRY] Mencoba membuat kontrak dengan durasi 0 bulan...")
        penghuni_uji = Penghuni("Budi")
        kamar_uji = KamarStandar("B02")
        _ = Kontrak(penghuni_uji, kamar_uji, "Desember 2026", 0)
    except DurasiKontrakInvalidError as err:
        print(f"[EXCEPT - DurasiKontrakInvalidError] Berhasil tertangkap: {err}")
    except KosError as err:
        print(f"[EXCEPT - KosError] Error umum: {err}")
    else:
        print("[ELSE] Kontrak berhasil dibuat (seharusnya tidak tercapai).")
    finally:
        print("[FINALLY] Validasi durasi kontrak selesai diperiksa.")

    separator("SKENARIO 5: ATURAN BISNIS 4 - PEMBAYARAN TAGIHAN LUNAS")
    # Aturan 4: Tagihan yang sudah lunas tidak boleh dibayar kembali
    try:
        print("[TRY] Mencoba membayar kembali tagihan yang sudah lunas pada Skenario 1...")
        if kontrak_aktif and kontrak_aktif.tagihan:
            tagihan_lunas = kontrak_aktif.tagihan[0]
            print(f"  - Status saat ini: {tagihan_lunas}")
            tagihan_lunas.bayar()  # Pembayaran kedua kalinya
        else:
            print("  - Kontrak aktif tidak tersedia.")
    except TagihanLunasError as err:
        print(f"[EXCEPT - TagihanLunasError] Berhasil tertangkap: {err}")
    except KosError as err:
        print(f"[EXCEPT - KosError] Error umum: {err}")
    else:
        print("[ELSE] Tagihan berhasil dibayar ulang (seharusnya tidak tercapai).")
    finally:
        print("[FINALLY] Operasi pembayaran tagihan selesai diperiksa.")

    separator("RINGKASAN TOTAL OBJEK")
    print(f"Total objek Kamar yang berhasil dibuat: {Kamar.jumlah_dibuat}")


if __name__ == "__main__":
    main()
