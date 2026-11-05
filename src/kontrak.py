try:
    from .exceptions import DurasiKontrakInvalidError, TagihanLunasError
except ImportError:
    from exceptions import DurasiKontrakInvalidError, TagihanLunasError


class Penghuni:
    def __init__(self, nama):
        self.nama = nama

    def __str__(self):
        return f"Penghuni: {self.nama}"


class Tagihan:
    def __init__(self, bulan, total):
        self.bulan = bulan
        self.total = total
        self.lunas = False

    def bayar(self):
        if self.lunas:
            raise TagihanLunasError(self.bulan)
        self.lunas = True

    def __str__(self):
        status = "Lunas" if self.lunas else "Belum Lunas"
        return f"Tagihan {self.bulan}: Rp{self.total:,} ({status})"


class Kontrak:
    def __init__(self, penghuni, kamar, bulan, durasi):
        self.penghuni = penghuni
        self.kamar = kamar
        self.durasi = durasi  # Memanggil setter durasi untuk validasi
        self.tagihan = [Tagihan(bulan, kamar.hitung_tarif())]

    @property
    def durasi(self):
        return self.__durasi

    @durasi.setter
    def durasi(self, nilai):
        if not isinstance(nilai, int) or nilai < 1:
            raise DurasiKontrakInvalidError(nilai)
        self.__durasi = nilai

    def buat_tagihan(self, bulan):
        baru = Tagihan(bulan, self.kamar.hitung_tarif())
        self.tagihan.append(baru)
        return baru
