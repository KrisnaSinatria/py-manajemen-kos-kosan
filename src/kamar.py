try:
    from .exceptions import TarifInvalidError, ListrikInvalidError
except ImportError:
    from exceptions import TarifInvalidError, ListrikInvalidError


class Kamar:
    jumlah_dibuat = 0

    def __init__(self, nomor, tarif):
        self._nomor = nomor
        self.tarif = tarif
        Kamar.jumlah_dibuat += 1

    @property
    def nomor(self):
        return self._nomor

    @property
    def tarif(self):
        return self.__tarif

    @tarif.setter
    def tarif(self, nilai):
        if not self.validasi_angka(nilai) or nilai <= 0:
            raise TarifInvalidError(nilai)
        self.__tarif = nilai

    @staticmethod
    def validasi_angka(nilai):
        return type(nilai) is int and nilai >= 0

    def hitung_tarif(self):
        return self.tarif

    def __str__(self):
        return f"Kamar {self.nomor}"

    def __eq__(self, lain):
        return type(self) is type(lain) and self.nomor == lain.nomor


class KamarStandar(Kamar):
    def __init__(self, nomor):
        super().__init__(nomor, 750_000)

    @classmethod
    def dari_nomor(cls, nomor):
        return cls(nomor)


class KamarDenganListrik(Kamar):
    TARIF_KWH = 1_500

    def __init__(self, nomor, tarif):
        super().__init__(nomor, tarif)
        self.kwh = 0

    @property
    def kwh(self):
        return self.__kwh

    @kwh.setter
    def kwh(self, nilai):
        if not self.validasi_angka(nilai):
            raise ListrikInvalidError(nilai)
        self.__kwh = nilai

    def hitung_tarif(self):
        return super().hitung_tarif() + self.kwh * self.TARIF_KWH


class KamarAC(KamarDenganListrik):
    def __init__(self, nomor):
        super().__init__(nomor, 900_000)
