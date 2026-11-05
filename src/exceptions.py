class KosError(Exception):
    """Base class untuk semua custom exception pada sistem kos-kosan."""
    pass


class TarifInvalidError(KosError):
    """Exception yang dilempar ketika tarif kamar bernilai <= 0 atau tidak valid."""
    def __init__(self, tarif):
        self.tarif = tarif
        super().__init__(f"Tarif kamar tidak valid: {tarif}. Tarif harus berupa bilangan bulat positif (> 0).")


class ListrikInvalidError(KosError):
    """Exception yang dilempar ketika nilai kWh pemakaian listrik negatif."""
    def __init__(self, kwh):
        self.kwh = kwh
        super().__init__(f"Pemakaian listrik tidak valid: {kwh} kWh. Nilai kWh tidak boleh negatif.")


class DurasiKontrakInvalidError(KosError):
    """Exception yang dilempar ketika durasi kontrak sewa kurang dari 1 bulan."""
    def __init__(self, durasi):
        self.durasi = durasi
        super().__init__(f"Durasi kontrak tidak valid: {durasi} bulan. Minimal sewa adalah 1 bulan.")


class TagihanLunasError(KosError):
    """Exception yang dilempar ketika mencoba membayar tagihan yang sudah berstatus lunas."""
    def __init__(self, bulan):
        self.bulan = bulan
        super().__init__(f"Pembayaran gagal: Tagihan bulan {bulan} sudah berstatus lunas.")
